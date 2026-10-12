from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'upstream_audit', ROOT / '.agents/skills/poteto-mode/scripts/upstream-audit.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class UpstreamAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        (self.source / '.cursor-plugin').mkdir(parents=True)
        (self.source / '.cursor-plugin/plugin.json').write_text('{"version":"fixture"}\n')
        self.baseline = self.root / 'baseline.json'
        self.baseline.write_text(json.dumps({'version': 'fixture', 'revision': 'fixture-revision', 'files': []}))
        self.save_current()

    def save_current(self):
        changes = module.audit(self.source, self.baseline)['changes']
        self.baseline.write_text(json.dumps({'version': 'fixture', 'revision': 'fixture-revision',
            'files': [{'source': item['source'], 'source_sha256': item['after_sha256'],
                       'destination': item['source']} for item in changes]}))

    def test_unchanged_snapshot_is_current_without_writes(self):
        before = self.baseline.read_bytes()
        result = module.audit(self.source, self.baseline)
        self.assertEqual(result['status'], 'current')
        self.assertEqual(result['changes'], [])
        self.assertEqual(self.baseline.read_bytes(), before)

    def test_content_drift_is_detected_even_without_a_version_bump(self):
        file = self.source / '.cursor-plugin/plugin.json'
        file.write_text('{"version":"fixture", "description":"changed"}\n')
        result = module.audit(self.source, self.baseline)
        self.assertEqual(result['status'], 'drift')
        self.assertEqual(result['changes'][0]['status'], 'modified')
        self.assertEqual(result['from_version'], result['to_version'])

    def test_additions_and_removals_have_explicit_dispositions(self):
        (self.source / 'skills/new').mkdir(parents=True)
        (self.source / 'skills/new/SKILL.md').write_text('new skill\n')
        (self.source / 'plugin.json').write_text('{}\n')
        old = json.loads(self.baseline.read_text())
        old['files'].append({'source': 'removed.md', 'source_sha256': 'old', 'destination': 'removed.md'})
        self.baseline.write_text(json.dumps(old))
        items = {item['source']: item for item in module.audit(self.source, self.baseline)['changes']}
        self.assertEqual(items['removed.md']['status'], 'removed')
        self.assertEqual(items['skills/new/SKILL.md']['destination'], '.agents/skills/new/SKILL.md')
        self.assertIsNone(items['plugin.json']['destination'])

    def test_missing_source_and_symlinks_fail(self):
        with self.assertRaisesRegex(ValueError, 'does not exist'):
            module.audit(self.root / 'missing', self.baseline)
        (self.source / 'link').symlink_to(self.baseline)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            module.audit(self.source, self.baseline)
