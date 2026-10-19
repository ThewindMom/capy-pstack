from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / '.agents'


class Update01525Revision4382e68Tests(unittest.TestCase):
    def test_source_inventory_and_reviewed_dispositions(self):
        source = json.loads((ROOT / 'provenance/updates/0.15.28.json').read_text())['previous_source']
        update = json.loads((ROOT / 'provenance/updates/0.15.25-4382e68.json').read_text())
        self.assertEqual(source['revision'], '4382e687a50b8d2c5ce4d141d001186589cff8d5')
        self.assertEqual(source['subtree'], '28b372cc7c490a963c9407d681427a0503745eb8')
        self.assertEqual(source['version'], '0.15.25')
        self.assertEqual(len(source['files']), 171)
        self.assertEqual(update['from_revision'], '182f2ce414e83224915c190d2f63239c1608d0a5')
        self.assertEqual(update['to_revision'], source['revision'])
        before = {item['source']: item for item in update['previous_source']['files']}
        after = {item['source']: item for item in source['files']}
        expected = {name for name in before.keys() | after.keys() if before.get(name) != after.get(name)}
        self.assertEqual({item['source'] for item in update['changes']}, expected)
        self.assertEqual(len(expected), 19)
        for item in update['changes']:
            with self.subTest(source=item['source']):
                self.assertIn(item['disposition'], ('ported', 'existing-native-equivalent', 'platform-only'))
                self.assertTrue(item['reason'])
                self.assertEqual(item['before_sha256'], before.get(item['source'], {}).get('source_sha256'))
                self.assertEqual(item['after_sha256'], after.get(item['source'], {}).get('source_sha256'))
                self.assertTrue((ROOT / item['destination']).is_file())

    def test_formal_verification_skill_is_native_and_routed(self):
        skill = (BUNDLE / 'skills/create-formal-verification-skill/SKILL.md').read_text()
        self.assertIn('name: create-formal-verification-skill\n', skill)
        self.assertNotIn('disable-model-invocation', skill)
        self.assertIn('.agents/skills/verify-<area>/SKILL.md', skill)
        self.assertIn('Able to fail', skill)
        self.assertIn('Do not edit the project\'s Setup as a side effect', skill)
        self.assertIn('/create-formal-verification-skill', (BUNDLE / 'skills/poteto-help/SKILL.md').read_text())
        self.assertIn('create-formal-verification-skill', (ROOT / 'docs/skill-catalog.md').read_text())

    def test_ketchup_lists_every_call_and_keeps_native_reads(self):
        ketchup = (BUNDLE / 'skills/ketchup/SKILL.md').read_text()
        self.assertIn('Never cut items or shrink them to stay under a word count', ketchup)
        self.assertIn('Fit the shape to the call', ketchup)
        self.assertNotIn('well under 150 words, not counting visuals. Draw', ketchup)
        self.assertIn('thread.get', ketchup)
        self.assertIn('Do not start an app', ketchup)
        self.assertIn('A Markdown table is not a visual', ketchup)

    def test_brands_come_from_type_guards(self):
        rules = (BUNDLE / 'skills/typescript-best-practices/SKILL.md').read_text()
        patterns = (BUNDLE / 'skills/typescript-best-practices/references/patterns.md').read_text()
        self.assertIn('never from `as`', rules)
        self.assertIn('input is AgentId', patterns)
        self.assertNotIn('return input as AgentId', patterns)
