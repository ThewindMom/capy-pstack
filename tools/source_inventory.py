#!/usr/bin/env python3
"""Audit a local upstream source snapshot without downloading or executing it."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def git_hash(kind: str, data: bytes) -> bytes:
    return hashlib.sha1(kind.encode() + b' ' + str(len(data)).encode() + b'\0' + data).digest()


def tree_hash(root: Path) -> bytes:
    entries = []
    for path in root.iterdir():
        if path.is_symlink():
            raise ValueError(f'Source symlink is not supported: {path}')
        if path.is_dir():
            entries.append((path.name.encode() + b'/', b'40000', path.name.encode(), tree_hash(path)))
        elif path.is_file():
            mode = b'100755' if path.stat().st_mode & 0o111 else b'100644'
            entries.append((path.name.encode(), mode, path.name.encode(), git_hash('blob', path.read_bytes())))
    return git_hash('tree', b''.join(mode + b' ' + name + b'\0' + digest
                                    for _, mode, name, digest in sorted(entries)))


def inventory(source: Path, previous: dict, *, version: str, revision: str, subtree: str) -> dict:
    if not source.is_dir():
        raise ValueError(f'Source directory does not exist: {source}')
    actual = tree_hash(source).hex()
    if actual != subtree:
        raise ValueError(f'Source tree mismatch: expected {subtree}, got {actual}')
    if json.loads((source / '.cursor-plugin/plugin.json').read_text())['version'] != version:
        raise ValueError('Source manifest version does not match requested version')
    destinations = {item['source']: item['destination'] for item in previous['files']}
    files = []
    for path in sorted(source.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(source).as_posix()
        destination = destinations.get(rel)
        if destination is None and rel.startswith('skills/'):
            destination = '.agents/' + rel
        if destination is None:
            raise ValueError(f'New source requires an explicit destination: {rel}')
        files.append({'source': rel, 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                      'destination': destination})
    return {'upstream_repository': 'cursor/plugins', 'revision': revision, 'subtree': subtree,
            'version': version, 'files': files}


def changes(previous: dict, current: dict) -> list[dict]:
    old = {item['source']: item for item in previous['files']}
    new = {item['source']: item for item in current['files']}
    records = []
    for source in sorted(old.keys() | new.keys()):
        before, after = old.get(source), new.get(source)
        if before == after:
            continue
        records.append({'source': source, 'destination': (after or before)['destination'],
                        'status': 'added' if before is None else 'removed' if after is None else 'modified',
                        'before_sha256': before['source_sha256'] if before else None,
                        'after_sha256': after['source_sha256'] if after else None})
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--version', required=True)
    parser.add_argument('--revision', required=True)
    parser.add_argument('--subtree', required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    try:
        destination = ROOT / 'provenance/source.json'
        previous = json.loads(destination.read_text())
        current = inventory(args.source, previous, version=args.version,
                            revision=args.revision, subtree=args.subtree)
        missing = [item['destination'] for item in current['files']
                   if not (ROOT / item['destination']).is_file()]
        if missing:
            raise ValueError(f'Unaccounted native destinations: {missing}')
        if args.write:
            if previous != current:
                update = {'from_version': previous['version'], 'to_version': current['version'],
                          'from_revision': previous['revision'], 'to_revision': current['revision'],
                          'source_subtree': current['subtree'], 'source_files': len(current['files']),
                          'previous_source': previous, 'changes': changes(previous, current)}
                record = ROOT / 'provenance/updates' / (args.version + '.json')
                if record.exists():
                    raise ValueError(f'Update record already exists: {record}')
                record.write_text(json.dumps(update, indent=2) + '\n')
                destination.write_text(json.dumps(current, indent=2) + '\n')
        elif previous != current:
            raise ValueError('Source inventory differs; review native edits before using --write')
        print(json.dumps({'status': 'ok', 'source_files': len(current['files']), 'subtree': current['subtree']}))
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
