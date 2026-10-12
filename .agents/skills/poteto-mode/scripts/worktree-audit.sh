#!/usr/bin/env bash
# Read-only worktree audit. Reports whether each worktree HEAD is an ancestor
# of a base ref. Never deletes a worktree and never marks one safe to delete.
#
# Usage: worktree-audit.sh [-b|--base <ref>] [repo-path]
#   repo-path defaults to the current directory.
#   -b sets the ref the merged field checks against (for example origin/integration).
#   Without it the base is origin/HEAD, then origin/main, then origin/master.
#   origin/HEAD is the remote default branch, not necessarily the branch PRs
#   merge into. Pass -b when they differ.
#   A checkout with none of those refs and no -b still audits. merged is null.
set -euo pipefail

base=""
while [ $# -gt 0 ]; do
	case "$1" in
	-b|--base) [ $# -ge 2 ] || { echo "error: $1 needs a ref" >&2; exit 2; }; base="$2"; shift 2 ;;
	-h|--help) sed -n '2,/^set -euo pipefail/p' "$0" | sed '$d; s/^# \{0,1\}//'; exit 0 ;;
	-*) echo "error: unknown option: $1" >&2; exit 2 ;;
	*) break ;;
	esac
done

repo="${1:-.}"
exec python3 - "$repo" "$base" <<'PY'
import json, subprocess, sys

repo = sys.argv[1]
requested = sys.argv[2]

def git(root, *args, check=True):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or f'git {" ".join(args)} failed')
    return result

def verifies(ref):
    return git(repo, 'rev-parse', '--verify', '--quiet', f'{ref}^{{commit}}', check=False).returncode == 0

def fetch_origin(ref):
    if not ref.startswith('origin/'):
        return
    branch = ref[len('origin/'):]
    fetched = git(
        repo, 'fetch', 'origin',
        f'+refs/heads/{branch}:refs/remotes/{ref}',
        '--quiet', check=False,
    )
    if fetched.returncode:
        print(f'warn: could not fetch {ref}; merged column may be stale', file=sys.stderr)

def resolve_base():
    if requested:
        fetch_origin(requested)
        if not verifies(requested):
            print(f'error: base ref not found: {requested}', file=sys.stderr)
            raise SystemExit(1)
        return requested
    seen = []
    symbolic = git(repo, 'symbolic-ref', '--short', 'refs/remotes/origin/HEAD', check=False)
    if symbolic.returncode == 0 and symbolic.stdout.strip():
        seen.append(symbolic.stdout.strip())
    for cand in ('origin/main', 'origin/master'):
        if cand not in seen:
            seen.append(cand)
    for cand in seen:
        if verifies(cand):
            print(f'warn: no -b given; MERGED checks against {cand}', file=sys.stderr)
            fetch_origin(cand)
            return cand
    print('warn: no base ref (origin/HEAD, origin/main, origin/master all missing); merged is unknown', file=sys.stderr)
    return None

try:
    base = resolve_base()
    if base is not None:
        print(f'# base: {base}', file=sys.stderr)
    rows = []
    raw = git(repo, 'worktree', 'list', '--porcelain', '-z').stdout
    for record in raw.split('\0\0'):
        fields = record.strip('\0').split('\0')
        info = dict(f.split(' ', 1) if ' ' in f else (f, True) for f in fields if f)
        if 'worktree' not in info:
            continue
        status = git(info['worktree'], 'status', '--porcelain=v1', '-z').stdout
        merged = None
        if base is not None:
            ancestor = git(info['worktree'], 'merge-base', '--is-ancestor', 'HEAD', base, check=False)
            merged = ancestor.returncode == 0
        rows.append({
            'path': info['worktree'],
            'head': info.get('HEAD'),
            'branch': info.get('branch'),
            'dirty': bool(status),
            'locked': 'locked' in info,
            'base': base,
            'merged': merged,
            'safe_to_delete': False,
            'next': 'Reconcile live Capy tasks, pushed commits and retained evidence.',
        })
    print(json.dumps(rows, indent=2))
except SystemExit:
    raise
except (OSError, RuntimeError) as exc:
    print(str(exc), file=sys.stderr)
    sys.exit(2)
PY
