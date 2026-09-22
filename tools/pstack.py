#!/usr/bin/env python3
"""Offline installation of the complete, directly usable Capy pstack bundle."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = '.capy-pstack-install.json'
LOCK = '.capy-pstack-install.lock'
RULE = '.capy/rules/pstack-capy.mdc'


class PortError(ValueError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def relative(name: str) -> str:
    if (not isinstance(name, str) or not name or '\\' in name or '\x00' in name
            or name.startswith('/') or any(p in ('', '.', '..', '.git') for p in name.split('/'))):
        raise PortError(f'Unsafe bundle path: {name!r}')
    return name


def guarded(path: Path) -> Path:
    path = Path(os.path.abspath(path))
    for part in (path, *path.parents):
        if part.is_symlink():
            raise PortError(f'Symlink in installation path: {part}')
    return path


def record(path: Path) -> tuple[bytes, int]:
    guarded(path)
    if not path.is_file():
        raise PortError(f'Expected a regular file: {path}')
    return path.read_bytes(), stat.S_IMODE(path.stat().st_mode)


def catalog(root: Path) -> dict:
    value = json.loads(record(root / 'catalog.json')[0])
    if not isinstance(value, dict) or value.get('version') != 1 or not isinstance(value.get('files'), dict):
        raise PortError('Invalid bundle catalog')
    for name, item in value['files'].items():
        relative(name)
        if not isinstance(item, dict) or item.get('mode') not in ('644', '755'):
            raise PortError('Invalid catalog mode')
        data, mode = record(root / name)
        if digest(data) != item.get('sha256') or mode != int(item['mode'], 8):
            raise PortError(f'Bundle differs from catalog: {name}')
    return value


def payload(volume: bool) -> dict[str, tuple[bytes, int]]:
    source = guarded(ROOT / '.agents')
    values = catalog(source)['files']
    wanted = {}
    for name in [*values, 'catalog.json']:
        dest = name if volume else '.agents/' + name
        wanted[dest] = record(source / name)
    if not volume:
        wanted[RULE] = record(ROOT / RULE)
    return wanted


def permitted(name: str, volume: bool) -> bool:
    relative(name)
    if volume:
        return name.startswith(('skills/', 'roles/', 'automations/')) or name in (
            'catalog.json', 'LICENSE', 'NOTICE', 'pstack.models.example.json', 'pstack.model-presets.json')
    return name.startswith('.agents/') and name != '.agents/pstack.models.json' or name == RULE


def load_manifest(target: Path, volume: bool) -> dict:
    path = guarded(target / MANIFEST)
    if not path.exists():
        return {'format': 1, 'volume': volume, 'files': {}}
    value = json.loads(record(path)[0])
    if (not isinstance(value, dict) or value.get('format') != 1 or value.get('volume') is not volume
            or not isinstance(value.get('files'), dict)):
        raise PortError('Invalid installation manifest or scope')
    for name, item in value['files'].items():
        if not permitted(name, volume) or not isinstance(item, dict) or item.get('mode') not in (0o644, 0o755):
            raise PortError('Unsafe installation manifest')
        if not isinstance(item.get('sha256'), str) or len(item['sha256']) != 64:
            raise PortError('Invalid ownership hash')
    return value


def preflight(target: Path, old: dict, wanted: dict) -> None:
    for name in set(old['files']) | set(wanted):
        path = guarded(target / name)
        if name in old['files']:
            data, mode = record(path)
            item = old['files'][name]
            if digest(data) != item['sha256'] or mode != item['mode']:
                raise PortError(f'Locally modified managed file: {name}')
        elif path.exists():
            raise PortError(f'Unmanaged collision: {name}')


def apply(target: Path, wanted: dict, *, volume=False, dry_run=False, uninstall=False) -> dict:
    target = guarded(target)
    old = load_manifest(target, volume)
    if uninstall and not (target / MANIFEST).exists():
        raise PortError('No managed installation to uninstall')
    for name in wanted:
        if not permitted(name, volume):
            raise PortError(f'Forbidden destination: {name}')
    preflight(target, old, wanted)
    changes = {n: item for n, item in wanted.items() if not (target / n).exists() or record(target / n) != item}
    removed = sorted(set(old['files']) - set(wanted))
    report = {'write': sorted(changes), 'remove': removed, 'unchanged': len(wanted) - len(changes)}
    if dry_run:
        return report
    target.mkdir(parents=True, exist_ok=True)
    lock = guarded(target / LOCK)
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise PortError('Installer lock exists; inspect it, never remove a live lock') from exc
    os.close(fd)
    staging = None
    backups = {}
    try:
        if load_manifest(target, volume) != old:
            raise PortError('Ownership changed during preflight')
        preflight(target, old, wanted)
        state = {'format': 1, 'volume': volume, 'files': {
            n: {'sha256': digest(data), 'mode': mode} for n, (data, mode) in sorted(wanted.items())}}
        operations = dict(changes)
        operations.update({n: None for n in removed})
        encoded = (json.dumps(state, indent=2) + '\n').encode()
        previous = record(target / MANIFEST)[0] if (target / MANIFEST).exists() else None
        if uninstall:
            operations[MANIFEST] = None
        elif previous != encoded:
            operations[MANIFEST] = (encoded, 0o644)
        staging = Path(tempfile.mkdtemp(prefix='.capy-pstack-stage-', dir=target))
        for index, (name, item) in enumerate(operations.items()):
            path = guarded(target / name)
            backups[name] = record(path) if path.exists() else None
            if item is None:
                path.unlink()
            else:
                staged = staging / str(index)
                staged.write_bytes(item[0])
                staged.chmod(item[1])
                path.parent.mkdir(parents=True, exist_ok=True)
                guarded(path)
                os.replace(staged, path)
    except BaseException:
        for name, item in reversed(list(backups.items())):
            path = guarded(target / name)
            if item is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(item[0])
                path.chmod(item[1])
        raise
    finally:
        if staging:
            shutil.rmtree(staging)
        lock.unlink(missing_ok=True)
    return report


def doctor(target: Path, volume=False) -> dict:
    target = guarded(target)
    root = target if volume else target / '.agents'
    data = catalog(root)
    if (target / MANIFEST).exists():
        preflight(target, load_manifest(target, volume), {})
    return {'status': 'ok', 'files': len(data['files']),
            'skills': len(list((root / 'skills').glob('*/SKILL.md'))),
            'playbooks': len(list((root / 'skills/poteto-mode/playbooks').glob('*.md'))),
            'upstream_required': False, 'live_capy_verified': False}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('install', 'uninstall', 'doctor'))
    parser.add_argument('--target', type=Path)
    parser.add_argument('--volume', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.command != 'doctor' and args.target is None:
            raise PortError('--target is required for writes')
        target = args.target if args.target is not None else ROOT
        if args.command == 'doctor':
            result = doctor(target, args.volume)
        else:
            result = apply(target, payload(args.volume) if args.command == 'install' else {},
                           volume=args.volume, dry_run=args.dry_run, uninstall=args.command == 'uninstall')
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f'pstack: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
