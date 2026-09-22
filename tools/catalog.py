#!/usr/bin/env python3
"""Refresh or check the self-contained native bundle inventory after deliberate edits."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def inventory(root: Path) -> dict:
    records = {}
    for p in sorted(root.rglob('*')):
        rel = p.relative_to(root)
        if any(x in ('node_modules', '__pycache__', '.git') for x in rel.parts):
            continue
        if rel.as_posix() in ('catalog.json', 'pstack.models.json'):
            continue
        if p.is_symlink():
            raise ValueError(f'Bundle symlink: {rel}')
        if p.is_file():
            records[rel.as_posix()] = {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                                     'mode': '755' if p.stat().st_mode & 0o111 else '644'}
    return {'version': 1, 'files': records}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        catalog = ROOT / '.agents/catalog.json'
        data = inventory(ROOT / '.agents')
        if args.check:
            if json.loads(catalog.read_text()) != data:
                raise ValueError('Catalog drift: review the diff, then run python3 tools/catalog.py')
        else:
            catalog.write_text(json.dumps(data, indent=2) + '\n')
        print(json.dumps({'status': 'ok', 'files': len(data['files'])}))
        return 0
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
