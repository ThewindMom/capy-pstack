from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / '.agents'


class Update01525Tests(unittest.TestCase):
    def test_source_inventory_and_reviewed_dispositions(self):
        source = json.loads((ROOT / 'provenance/updates/0.15.25-182f2ce.json').read_text())['previous_source']
        update = json.loads((ROOT / 'provenance/updates/0.15.25.json').read_text())
        self.assertEqual(source['revision'], '99743e9c151c8537cbbf1f98bb38f34ef3368453')
        self.assertEqual(source['subtree'], '0d5fd349cbc77d054eed60f0e8cdfbea86321ff9')
        self.assertEqual(source['version'], '0.15.25')
        self.assertEqual(len(source['files']), 169)
        self.assertEqual(update['from_version'], '0.15.23')
        self.assertEqual(update['to_revision'], source['revision'])
        self.assertEqual(len(update['changes']), 15)
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

    def test_restated_principles_and_native_safeguards(self):
        ketchup = (BUNDLE / 'skills/ketchup/SKILL.md').read_text()
        swarm = (BUNDLE / 'skills/swarm/SKILL.md').read_text()
        tests = (BUNDLE / 'skills/principle-test-behavior-not-implementation/SKILL.md').read_text()
        root = (BUNDLE / 'skills/principle-fix-root-causes/SKILL.md').read_text()
        premise = (BUNDLE / 'skills/principle-attack-the-premise/SKILL.md').read_text()
        types = (BUNDLE / 'skills/principle-type-system-discipline/SKILL.md').read_text()
        self.assertIn('well under 150 words', ketchup)
        self.assertIn('Do not start an app', ketchup)
        self.assertIn('A Markdown table is not a visual', ketchup)
        self.assertIn('Change the internals', tests)
        self.assertNotIn('returned `undefined`', tests)
        self.assertIn('the state it handles is legitimate', root)
        self.assertIn('Write the premise down', premise)
        self.assertNotIn('refuse to lie', types)
        self.assertNotIn('N is total workers', swarm)
        self.assertIn('pstack.models.json', swarm)
        self.assertIn('fresh cloud machines', swarm)
