from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / '.agents'


class Update01528Tests(unittest.TestCase):
    def test_source_inventory_and_reviewed_dispositions(self):
        source = json.loads((ROOT / 'provenance/source.json').read_text())
        update = json.loads((ROOT / 'provenance/updates/0.15.28.json').read_text())
        self.assertEqual(source['revision'], 'd457567332aa6989e753ea289f30ea2bfbc80bc0')
        self.assertEqual(source['subtree'], '06803099e18ed488c8c2a2fda118ce772b4e2a77')
        self.assertEqual(source['version'], '0.15.28')
        self.assertEqual(len(source['files']), 172)
        self.assertEqual(update['from_revision'], '4382e687a50b8d2c5ce4d141d001186589cff8d5')
        self.assertEqual(update['to_revision'], source['revision'])
        before = {item['source']: item for item in update['previous_source']['files']}
        after = {item['source']: item for item in source['files']}
        expected = {name for name in before.keys() | after.keys() if before.get(name) != after.get(name)}
        self.assertEqual({item['source'] for item in update['changes']}, expected)
        self.assertEqual(len(expected), 16)
        for item in update['changes']:
            with self.subTest(source=item['source']):
                self.assertIn(item['disposition'], ('ported', 'existing-native-equivalent', 'platform-only'))
                self.assertTrue(item['reason'])
                self.assertEqual(item['before_sha256'], before.get(item['source'], {}).get('source_sha256'))
                self.assertEqual(item['after_sha256'], after.get(item['source'], {}).get('source_sha256'))
                self.assertTrue((ROOT / item['destination']).is_file())
        self.assertEqual((BUNDLE / 'skills/poteto-mode/references/upstream-source.json').read_bytes(),
                         (ROOT / 'provenance/source.json').read_bytes())

    def test_maintain_formal_verification_is_native_and_routed(self):
        skill = (BUNDLE / 'skills/maintain-formal-verification-skill/SKILL.md').read_text()
        self.assertIn('name: maintain-formal-verification-skill\n', skill)
        self.assertNotIn('disable-model-invocation', skill)
        self.assertIn('do not weaken the property or the model to make it pass', skill)
        self.assertIn("do not edit the project's Setup as a side effect", skill)
        self.assertIn('Leave them uncommitted unless publication is authorized', skill)
        self.assertIn('/maintain-formal-verification-skill', (BUNDLE / 'skills/poteto-help/SKILL.md').read_text())
        self.assertIn('maintain-formal-verification-skill', (ROOT / 'docs/skill-catalog.md').read_text())

    def test_formal_generator_records_sync_and_setup_offers_it(self):
        skill = (BUNDLE / 'skills/create-formal-verification-skill/SKILL.md').read_text()
        self.assertIn('TLA+ is the default', skill)
        self.assertIn('sync commit', skill)
        self.assertIn('.agents/skills/verify-<area>/SKILL.md', skill)
        self.assertIn('/maintain-formal-verification-skill', skill)
        setup = (BUNDLE / 'skills/setup-pstack/SKILL.md').read_text()
        self.assertIn('offer create-formal-verification-skill once', setup)

    def test_sharpen_keeps_native_authorization(self):
        sharpen = (BUNDLE / 'skills/sharpen/SKILL.md').read_text()
        self.assertNotIn('rewritten prompt', sharpen)
        self.assertIn("within the user's authorization", sharpen)
        self.assertIn('model preferences', sharpen)
