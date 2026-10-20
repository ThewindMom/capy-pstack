from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / '.agents'


class Update01529Tests(unittest.TestCase):
    def test_source_inventory_and_reviewed_dispositions(self):
        source = json.loads((ROOT / 'provenance/source.json').read_text())
        update = json.loads((ROOT / 'provenance/updates/0.15.29.json').read_text())
        self.assertEqual(source['revision'], '88d47514b82e7c44f00f2b2a72ff6dd12158038c')
        self.assertEqual(source['subtree'], '34a0b817e5ea92375bb10f20b15cf750d4e8095a')
        self.assertEqual(source['version'], '0.15.29')
        self.assertEqual(len(source['files']), 172)
        self.assertEqual(update['from_revision'], 'd457567332aa6989e753ea289f30ea2bfbc80bc0')
        self.assertEqual(update['to_revision'], source['revision'])
        before = {item['source']: item for item in update['previous_source']['files']}
        after = {item['source']: item for item in source['files']}
        expected = {name for name in before.keys() | after.keys() if before.get(name) != after.get(name)}
        self.assertEqual({item['source'] for item in update['changes']}, expected)
        self.assertEqual(len(expected), 8)
        for item in update['changes']:
            with self.subTest(source=item['source']):
                self.assertIn(item['disposition'], ('ported', 'existing-native-equivalent', 'platform-only'))
                self.assertTrue(item['reason'])
                self.assertEqual(item['before_sha256'], before.get(item['source'], {}).get('source_sha256'))
                self.assertEqual(item['after_sha256'], after.get(item['source'], {}).get('source_sha256'))
                self.assertTrue((ROOT / item['destination']).is_file())
        self.assertEqual((BUNDLE / 'skills/poteto-mode/references/upstream-source.json').read_bytes(),
                         (ROOT / 'provenance/source.json').read_bytes())

    def test_sharpen_returns_only_the_rewrite_within_authorization(self):
        sharpen = (BUNDLE / 'skills/sharpen/SKILL.md').read_text()
        self.assertIn('Use only for /sharpen', sharpen)
        self.assertIn('do four things', sharpen)
        self.assertIn('Return only the rewrite and do not do the task', sharpen)
        self.assertNotIn('Then do the work', sharpen)
        self.assertIn("within the user's authorization", sharpen)
        self.assertIn('model preferences', sharpen)
        self.assertIn("doesn't do the task", (ROOT / 'docs/guide/02-poteto-mode.md').read_text())
        self.assertIn('does not do the task', (BUNDLE / 'skills/poteto-help/SKILL.md').read_text())
