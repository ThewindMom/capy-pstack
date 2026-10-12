"""Behavioral checks for the 0.15.21 tooling port. Not a catalog or provenance audit."""
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / '.agents' / 'skills' / 'poteto-mode' / 'scripts'
AUDIT = SCRIPTS / 'worktree-audit.sh'


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True)


class WorktreeAuditBaseTests(unittest.TestCase):
    def test_repo_without_origin_stays_unknown_and_deletes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'repo with spaces'
            root.mkdir()
            self.assertEqual(git(root, 'init', '-b', 'main').returncode, 0)
            self.assertEqual(git(root, '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '--allow-empty', '-m', 'fixture').returncode, 0)
            other = Path(d) / 'other with spaces'
            self.assertEqual(git(root, 'worktree', 'add', '-b', 'task', str(other)).returncode, 0)
            (other / 'untracked').write_text('preserve')
            out = subprocess.run(['bash', str(AUDIT), str(root)], capture_output=True, text=True)
            self.assertEqual(out.returncode, 0, out.stderr)
            records = json.loads(out.stdout)
            self.assertEqual(len(records), 2)
            self.assertTrue(all(row['base'] is None and row['merged'] is None for row in records))
            self.assertTrue(all(row['safe_to_delete'] is False for row in records))
            self.assertEqual((other / 'untracked').read_text(), 'preserve')
            self.assertIn('merged is unknown', out.stderr)

    def test_explicit_base_splits_ancestor_from_unmerged(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'repo'
            root.mkdir()
            self.assertEqual(git(root, 'init', '-b', 'main').returncode, 0)
            self.assertEqual(git(root, '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '--allow-empty', '-m', 'base').returncode, 0)
            landed = Path(d) / 'landed'
            extra = Path(d) / 'extra'
            self.assertEqual(git(root, 'worktree', 'add', '-b', 'landed', str(landed)).returncode, 0)
            self.assertEqual(git(root, 'worktree', 'add', '-b', 'extra', str(extra)).returncode, 0)
            self.assertEqual(git(extra, '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '--allow-empty', '-m', 'not merged').returncode, 0)
            out = subprocess.run(['bash', str(AUDIT), '-b', 'main', str(root)], capture_output=True, text=True)
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertIn('# base: main', out.stderr)
            records = {row['path']: row for row in json.loads(out.stdout)}
            self.assertTrue(records[str(landed)]['merged'])
            self.assertFalse(records[str(extra)]['merged'])
            self.assertTrue(all(row['safe_to_delete'] is False and row['base'] == 'main' for row in records.values()))

    def test_default_base_uses_origin_head_instead_of_literal_main(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'repo'
            root.mkdir()
            self.assertEqual(git(root, 'init', '-b', 'master').returncode, 0)
            self.assertEqual(git(root, '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '--allow-empty', '-m', 'master').returncode, 0)
            head = git(root, 'rev-parse', 'HEAD').stdout.strip()
            self.assertEqual(git(root, 'update-ref', 'refs/remotes/origin/master', head).returncode, 0)
            self.assertEqual(git(root, 'symbolic-ref', 'refs/remotes/origin/HEAD', 'refs/remotes/origin/master').returncode, 0)
            landed = Path(d) / 'landed'
            extra = Path(d) / 'extra'
            self.assertEqual(git(root, 'worktree', 'add', str(landed), 'HEAD').returncode, 0)
            self.assertEqual(git(root, 'worktree', 'add', '-b', 'extra', str(extra)).returncode, 0)
            self.assertEqual(git(extra, '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '--allow-empty', '-m', 'ahead').returncode, 0)
            out = subprocess.run(['bash', str(AUDIT), str(root)], capture_output=True, text=True)
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertIn('MERGED checks against origin/master', out.stderr)
            self.assertNotIn('origin/main', out.stderr)
            records = {row['path']: row for row in json.loads(out.stdout)}
            self.assertEqual(records[str(landed)]['base'], 'origin/master')
            self.assertTrue(records[str(landed)]['merged'])
            self.assertFalse(records[str(extra)]['merged'])

    def test_missing_base_and_bad_options_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'repo'
            root.mkdir()
            self.assertEqual(git(root, 'init', '-b', 'main').returncode, 0)
            missing = subprocess.run(['bash', str(AUDIT), '-b', 'refs/heads/missing', str(root)], capture_output=True, text=True)
            self.assertEqual(missing.returncode, 1)
            self.assertIn('base ref not found: refs/heads/missing', missing.stderr)
            unknown = subprocess.run(['bash', str(AUDIT), '--nope', str(root)], capture_output=True, text=True)
            self.assertEqual(unknown.returncode, 2)
            self.assertIn('unknown option', unknown.stderr)
            bare = subprocess.run(['bash', str(AUDIT), '-b'], capture_output=True, text=True)
            self.assertEqual(bare.returncode, 2)
            help_out = subprocess.run(['bash', str(AUDIT), '--help'], capture_output=True, text=True)
            self.assertEqual(help_out.returncode, 0, help_out.stderr)
            self.assertIn('Usage: worktree-audit.sh', help_out.stdout)


if __name__ == '__main__':
    unittest.main()
