from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / '.agents'


class Update01525Revision182f2ceTests(unittest.TestCase):
    def test_source_inventory_and_reviewed_dispositions(self):
        source = json.loads((ROOT / 'provenance/source.json').read_text())
        update = json.loads((ROOT / 'provenance/updates/0.15.25-182f2ce.json').read_text())
        self.assertEqual(source['revision'], '182f2ce414e83224915c190d2f63239c1608d0a5')
        self.assertEqual(source['subtree'], '54ac5265638c4455ec3d04d496a379b5afc6aac2')
        self.assertEqual(source['version'], '0.15.25')
        self.assertEqual(len(source['files']), 170)
        self.assertEqual(update['from_revision'], '99743e9c151c8537cbbf1f98bb38f34ef3368453')
        self.assertEqual(update['to_revision'], source['revision'])
        before = {item['source']: item for item in update['previous_source']['files']}
        after = {item['source']: item for item in source['files']}
        expected = {name for name in before.keys() | after.keys() if before.get(name) != after.get(name)}
        self.assertEqual({item['source'] for item in update['changes']}, expected)
        self.assertEqual(expected, {'README.md', 'docs/harness/claude-code.md'})
        for item in update['changes']:
            with self.subTest(source=item['source']):
                self.assertEqual(item['disposition'], 'platform-only')
                self.assertTrue(item['reason'])
                self.assertEqual(item['before_sha256'], before.get(item['source'], {}).get('source_sha256'))
                self.assertEqual(item['after_sha256'], after.get(item['source'], {}).get('source_sha256'))
                self.assertTrue((ROOT / item['destination']).is_file())
        self.assertEqual((BUNDLE / 'skills/poteto-mode/references/upstream-source.json').read_bytes(),
                         (ROOT / 'provenance/source.json').read_bytes())

    def test_claude_code_adapter_is_not_imported(self):
        porting = (ROOT / 'docs/porting.md').read_text()
        self.assertIn('docs/harness/claude-code.md', porting)
        self.assertFalse((ROOT / 'docs/harness').exists())
        for path in (BUNDLE / 'skills').rglob('*.md'):
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertNotIn('/pstack:', path.read_text())
