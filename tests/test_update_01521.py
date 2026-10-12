from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / '.agents'


class Update01521Tests(unittest.TestCase):
    def test_complete_source_inventory_and_dispositions(self):
        source = json.loads((ROOT / 'provenance/source.json').read_text())
        update = json.loads((ROOT / 'provenance/updates/0.15.21.json').read_text())
        self.assertEqual(source['revision'], '997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102')
        self.assertEqual(source['subtree'], '8824c764d99583f7cc8059c915296e444c53f060')
        self.assertEqual(source['version'], '0.15.21')
        self.assertEqual(len(source['files']), 167)
        self.assertEqual(update['from_version'], '0.15.15')
        self.assertEqual(update['to_revision'], source['revision'])
        self.assertEqual(len(update['changes']), 62)
        before = {item['source']: item for item in update['previous_source']['files']}
        after = {item['source']: item for item in source['files']}
        expected = {name for name in before.keys() | after.keys() if before.get(name) != after.get(name)}
        self.assertEqual({item['source'] for item in update['changes']}, expected)
        for item in update['changes']:
            with self.subTest(source=item['source']):
                self.assertIn(item['disposition'], ('ported', 'existing-native-equivalent', 'platform-only'))
                self.assertTrue(item['reason'])
                self.assertEqual(item['before_sha256'], before.get(item['source'], {}).get('source_sha256'))
                self.assertEqual(item['after_sha256'], after.get(item['source'], {}).get('source_sha256'))
                self.assertTrue((ROOT / item['destination']).is_file())

    def test_bundle_only_install_has_the_actual_accepted_baseline(self):
        installed = BUNDLE / 'skills/poteto-mode/references/upstream-source.json'
        self.assertEqual(installed.read_bytes(), (ROOT / 'provenance/source.json').read_bytes())
        maintenance = (BUNDLE / 'skills/poteto-mode/references/upstream-maintenance.md').read_text()
        self.assertIn('actual installed', (ROOT / 'README.md').read_text())
        self.assertIn('locally modified managed file', maintenance)
        self.assertIn('uncommitted', maintenance)

    def test_ketchup_is_native_read_only_catch_up(self):
        text = (BUNDLE / 'skills/ketchup/SKILL.md').read_text()
        self.assertIn('name: ketchup\n', text)
        self.assertIn('read-only', text)
        self.assertIn('action item', text.lower())
        self.assertNotIn('disable-model-invocation:', text)
        self.assertNotIn('.cursor/', text)
