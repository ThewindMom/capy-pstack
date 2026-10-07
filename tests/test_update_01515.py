"""Source parity and native workflow contracts, not remote integration certification."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / '.agents'


class Update01515Tests(unittest.TestCase):
    def test_complete_source_and_change_inventory(self):
        source = json.loads((ROOT / 'provenance/source.json').read_text())
        update = json.loads((ROOT / 'provenance/updates/0.15.15.json').read_text())
        self.assertEqual(source['revision'], 'df581122cde17e6e27686b5a448bde23e4ad4318')
        self.assertEqual(source['subtree'], '9d9cb20f79203a97c925de402c66183d0fa26c42')
        self.assertEqual(source['version'], '0.15.15')
        self.assertEqual(len(source['files']), 164)
        self.assertEqual(update['to_revision'], source['revision'])
        self.assertEqual(update['from_version'], '0.15.3')
        self.assertEqual(update['previous_source']['revision'], update['from_revision'])
        self.assertEqual(len(update['previous_source']['files']), 158)
        self.assertEqual(len(update['changes']), 59)
        current = {item['source']: item for item in source['files']}
        previous = {item['source']: item for item in update['previous_source']['files']}
        changed = {item['source'] for item in update['changes']}
        self.assertEqual(changed, {name for name in current.keys() | previous.keys()
                                   if current.get(name) != previous.get(name)})
        for item in source['files']:
            with self.subTest(source=item['source']):
                self.assertTrue((ROOT / item['destination']).is_file())
                self.assertEqual(len(item['source_sha256']), 64)
        for item in update['changes']:
            with self.subTest(source=item['source']):
                self.assertEqual(item['after_sha256'], current[item['source']]['source_sha256'])
                self.assertEqual(item['before_sha256'], previous.get(item['source'], {}).get('source_sha256'))
                self.assertEqual(item['destination'], current[item['source']]['destination'])

    def test_new_skill_sources_and_native_destinations(self):
        source = json.loads((ROOT / 'provenance/source.json').read_text())
        current = {item['source']: item['destination'] for item in source['files']}
        for name in ('benchmark-checklist', 'correct', 'poteto-help', 'principle-explain-the-number'):
            with self.subTest(skill=name):
                self.assertEqual(current[f'skills/{name}/SKILL.md'], f'.agents/skills/{name}/SKILL.md')
                text = (BUNDLE / f'skills/{name}/SKILL.md').read_text()
                self.assertIn(f'name: {name}\n', text)
                self.assertNotIn('disable-model-invocation:', text)
        checklist = (BUNDLE / 'skills/benchmark-checklist/SKILL.md').read_text()
        for question in ('Why not double?', 'Was it tuned?', 'Did it break limits?', 'Did it error?',
                         'Does it reproduce?', 'Does it matter?', 'Did it even happen?'):
            self.assertIn(question, checklist)

    def test_native_placement_and_publication_contracts(self):
        mode = (BUNDLE / 'skills/poteto-mode/SKILL.md').read_text()
        opening = (BUNDLE / 'skills/poteto-mode/playbooks/opening-a-pr.md').read_text()
        for text in ('shared', 'device', 'fresh', 'consolidated'):
            self.assertIn(text, mode)
        self.assertIn('gh-stack', opening)
        self.assertNotIn('Commit liberally', opening)
        self.assertNotIn('Amend when the fix belongs', opening)
        self.assertNotIn('gh pr create --base', opening)
        for path in BUNDLE.glob('skills/**/SKILL.md'):
            with self.subTest(skill=path.parent.name):
                self.assertNotIn('Three faithful seats', path.read_text())

    def test_same_runner_example_declares_coordination_and_local_boundary(self):
        example = json.loads((ROOT / 'examples/same-runner-plan.json').read_text())
        self.assertEqual(example['runner'], 'device')
        self.assertTrue(example['require_local'])
        self.assertEqual(example['shared_coordination'], {'git_writer': 'parent', 'concurrent_commits': False})
        self.assertEqual([task['machine'] for task in example['tasks']], ['shared', 'shared'])

    def test_help_and_audits_use_the_installed_contract(self):
        help_text = (BUNDLE / 'skills/poteto-help/SKILL.md').read_text()
        self.assertNotIn('github.com/thewindmom/capy-pstack/blob/main', help_text)
        self.assertIn('Bundle-only installations', help_text)
        self.assertIn('Check that a file exists', help_text)
        for name in ('autopilot-full', 'autopilot-stack', 'multi-phase-plan'):
            text = (BUNDLE / f'skills/poteto-mode/playbooks/{name}.md').read_text()
            with self.subTest(playbook=name):
                self.assertNotIn('git show origin/main:', text)
                self.assertIn('installed bundle', text)

    def test_native_pstack_trigger_is_in_the_discovered_description(self):
        frontmatter=(BUNDLE/'skills/poteto-mode/SKILL.md').read_text().split('---',2)[1]
        description=next(line for line in frontmatter.splitlines() if line.startswith('description:'))
        self.assertIn('Use for pstack, poteto, /poteto-mode',description)
