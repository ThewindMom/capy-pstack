#!/usr/bin/env python3
"""Compare a local Cursor pstack snapshot with the installed port's source inventory."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


def audit(source: Path, baseline: Path) -> dict:
    previous = json.loads(baseline.read_text())
    old = {item['source']: item for item in previous['files']}
    current = {}
    if not source.is_dir():
        raise ValueError(f'Source directory does not exist: {source}')
    for path in sorted(source.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Source symlink is not supported: {path}')
        if path.is_file():
            current[path.relative_to(source).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    version = json.loads((source / '.cursor-plugin/plugin.json').read_text())['version']
    changes = []
    for name in sorted(old.keys() | current.keys()):
        before = old.get(name, {}).get('source_sha256')
        after = current.get(name)
        if before != after:
            destination = old.get(name, {}).get('destination')
            if destination is None and name.startswith('skills/'):
                destination = '.agents/' + name
            changes.append({'source': name, 'destination': destination,
                            'status': 'added' if before is None else 'removed' if after is None else 'modified',
                            'before_sha256': before, 'after_sha256': after})
    return {'status': 'drift' if changes else 'current',
            'from_version': previous['version'], 'to_version': version,
            'baseline_revision': previous['revision'], 'changes': changes}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--baseline', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'references/upstream-source.json')
    args = parser.parse_args()
    try:
        print(json.dumps(audit(args.source, args.baseline), indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
