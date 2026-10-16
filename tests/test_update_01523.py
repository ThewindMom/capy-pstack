from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / '.agents'


class Update01523Tests(unittest.TestCase):
    def test_source_inventory_and_reviewed_dispositions(self):
        source = json.loads((ROOT / 'provenance/updates/0.15.25.json').read_text())['previous_source']
        update = json.loads((ROOT / 'provenance/updates/0.15.23.json').read_text())
        self.assertEqual(source['revision'], '79afd75d5bd51383fbb526b72f36db03180b8301')
        self.assertEqual(source['subtree'], '0b5c4ee63df6c559dc030bc257975c2044bbe27e')
        self.assertEqual(source['version'], '0.15.23')
        self.assertEqual(len(source['files']), 169)
        self.assertEqual(update['from_version'], '0.15.21')
        self.assertEqual(update['to_revision'], source['revision'])
        self.assertEqual(len(update['changes']), 45)
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

    def test_new_skill_and_policy_contracts(self):
        restate = (BUNDLE / 'skills/in-your-own-words/SKILL.md').read_text()
        sharpen = (BUNDLE / 'skills/sharpen/SKILL.md').read_text()
        ketchup = (BUNDLE / 'skills/ketchup/SKILL.md').read_text()
        policy = (BUNDLE / 'skills/poteto-mode/references/model-policy.md').read_text()
        self.assertIn('Use only for /in-your-own-words', restate)
        self.assertIn('Do not start implementation', restate)
        self.assertIn('independent check', sharpen)
        self.assertIn('explicit scope, permissions, model preferences', sharpen)
        self.assertIn('A Markdown table is not a visual', ketchup)
        self.assertIn('Do not start an app', ketchup)
        self.assertIn('example profile is never an override', policy)
        self.assertIn('Preserve explicit budgets', policy)
        self.assertIn('An omitted role effort does not unpin effort derived from a user-selected budget', policy)
