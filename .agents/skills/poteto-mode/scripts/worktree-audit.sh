#!/usr/bin/env bash
set -euo pipefail
exec python3 - "${1:-.}" <<'PY'
import json, subprocess, sys
from pathlib import Path

def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    return result.stdout

try:
    rows = []
    raw = git(sys.argv[1], 'worktree', 'list', '--porcelain', '-z')
    for record in raw.split('\0\0'):
        fields = record.strip('\0').split('\0')
        info = dict(f.split(' ', 1) if ' ' in f else (f, True) for f in fields if f)
        if 'worktree' not in info:
            continue
        status = git(info['worktree'], 'status', '--porcelain=v1', '-z')
        rows.append({'path': info['worktree'], 'head': info.get('HEAD'),
                     'branch': info.get('branch'), 'dirty': bool(status),
                     'locked': 'locked' in info, 'safe_to_delete': False,
                     'next': 'Reconcile live Capy tasks, pushed commits and retained evidence.'})
    print(json.dumps(rows, indent=2))
except (OSError, RuntimeError) as exc:
    print(str(exc), file=sys.stderr)
    sys.exit(2)
PY
