"""0.15.3 model and logger regressions; workflow checks cover text, not live agents."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from test_model_policy import EXPECTED, m, observed

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / '.agents/skills/show-me-your-work/scripts/log.sh'
HEADER = 'ts\tphase\tdecision\twhy\tevidence\tresult\n'


class ObservedBindingTests(unittest.TestCase):
    def test_public_identifier_shape_does_not_prove_native_route(self):
        obs = observed()
        del obs['bindings']
        with self.assertRaisesRegex(m.ModelError, 'never guess an ID'):
            m.resolve({}, 'arena runners', obs)
        self.assertEqual(m.requested({}, 'arena runners'), EXPECTED)

    def test_observed_opaque_routes_keep_identity_and_judge_family(self):
        obs = observed()
        for required, route in ((EXPECTED[0]['model'], 'fixture/native-opus-55'),
                                (EXPECTED[2]['model'], 'fixture/native-grok-47')):
            obs['models'][route] = obs['models'].pop(required)
            obs['bindings'][required]['model'] = route
        obs['parent'] = dict(EXPECTED[0], model='fixture/native-opus-55')
        order = m.work_order({'max_parallel': 2}, 'arena runners', obs)
        self.assertEqual(order['choices'], [dict(EXPECTED[0], model='fixture/native-opus-55'),
                                           EXPECTED[1], dict(EXPECTED[2], model='fixture/native-grok-47')])
        self.assertEqual(order['model_identities'], [x['model'] for x in EXPECTED])
        self.assertEqual(order['distinct_models'], 3)
        self.assertEqual(order['families'], ['anthropic', 'openai', 'xai'])
        self.assertEqual(order['upstream_version'], '0.15.3')
        self.assertEqual(order['waves'], [[0, 1], [2]])
        records = [{'seat': i, 'native_task_id': f'fixture-{i}', 'status': 'done',
                    'accepted': True, 'artifact': f'fixture-{i}.txt', 'settings': settings}
                   for i, settings in enumerate(order['choices'])]
        judge = m.select_judge({'max_parallel': 2}, obs, order, records)
        self.assertEqual(judge['choices'], [EXPECTED[1]])
        self.assertTrue(judge['different_parent_family'])
        self.assertFalse(order['native_execution_verified'])

    def test_binding_requires_its_own_identity_evidence_and_available_route(self):
        for binding in ({'model': EXPECTED[0]['model'], 'source': ''},
                        {'model': EXPECTED[0]['model']},
                        {'model': 'missing-native-route', 'source': 'fixture'},
                        'not-an-object'):
            obs = observed()
            obs['bindings'][EXPECTED[0]['model']] = binding
            with self.subTest(binding=binding), self.assertRaises(m.ModelError):
                m.resolve({}, 'arena runners', obs)

    def test_known_old_or_different_weights_cannot_be_relabelled(self):
        for route in ('anthropic/claude-opus-5', 'anthropic/claude-fable-5-1',
                      'xai/grok-4.6', 'supergrok/grok-4.6', 'openai/gpt-5.6-sol',
                      'codex/gpt-5.6-sol', EXPECTED[2]['model']):
            obs = observed()
            obs['models'][route] = {'reasoning_efforts': ['max', 'xhigh'], 'fast': True}
            obs['bindings'][EXPECTED[0]['model']]['model'] = route
            with self.subTest(route=route), self.assertRaises(m.ModelError):
                m.resolve({}, 'arena runners', obs)

    def test_one_native_route_cannot_supply_two_required_identities(self):
        obs = observed()
        obs['models']['fixture/shared-route'] = {'reasoning_efforts': ['max', 'xhigh'], 'fast': True}
        for binding in obs['bindings'].values():
            binding['model'] = 'fixture/shared-route'
        with self.assertRaisesRegex(m.ModelError, 'different upstream weights'):
            m.resolve({}, 'arena runners', obs)

    def test_unknown_binding_identity_is_not_added_to_the_registry(self):
        obs = observed()
        obs['bindings']['made/up-identity'] = {'model': EXPECTED[0]['model'], 'source': 'fixture'}
        with self.assertRaisesRegex(m.ModelError, 'Unknown upstream binding'):
            m.resolve({}, 'arena runners', obs)

    def test_binding_does_not_waive_effort_or_priority_checks(self):
        for capabilities in ({'reasoning_efforts': ['high'], 'fast': True},
                             {'reasoning_efforts': ['xhigh'], 'fast': False}):
            obs = observed()
            obs['models'][EXPECTED[2]['model']] = capabilities
            with self.subTest(capabilities=capabilities), self.assertRaises(m.ModelError):
                m.resolve({}, 'feature', obs)

    def test_old_pins_are_not_mutated_or_silently_migrated(self):
        profiles = [
            {'version': 2, 'roles': {'feature': {'model': 'xai/grok-4.6',
                                              'reasoning_effort': 'xhigh', 'fast': True}}},
            {'version': 2, 'panels': {'arena runners': [*EXPECTED, EXPECTED[0]]}},
        ]
        for profile in profiles:
            before = copy.deepcopy(profile)
            role = 'feature' if 'roles' in profile else 'arena runners'
            with self.subTest(role=role), self.assertRaisesRegex(m.ModelError, 'override|pin'):
                m.resolve(profile, role, observed())
            self.assertEqual(profile, before)
        reset = {'version': 2, 'roles': {}, 'panels': {}, 'max_parallel': 2}
        self.assertEqual(m.resolve(reset, 'arena runners', observed()), EXPECTED)
        self.assertEqual(reset['max_parallel'], 2)

    def test_explicit_custom_profile_can_keep_old_observed_weights(self):
        old = {'model': 'xai/grok-4.6', 'reasoning_effort': 'xhigh', 'fast': True}
        profile = {'version': 2, 'preset': 'custom', 'approved_difference': 'fixture approval, not live',
                   'roles': {'feature': old}}
        obs = {'source': 'synthetic fixture', 'models': {old['model']: {'reasoning_efforts': ['xhigh'], 'fast': True}}}
        self.assertEqual(m.resolve(profile, 'feature', obs), [old])


class AppendOnlyLogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.log = Path(self.tmp.name) / 'evidence with spaces' / 'decisions.tsv'

    def append(self, *fields):
        fields = fields or ('test', 'keep', 'real reason', 'artifact.txt', 'pass')
        output = subprocess.run(['bash', str(LOG), str(self.log), *fields],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(output.returncode, 0, output.stderr)

    def test_new_empty_and_populated_logs_append_without_duplicate_headers(self):
        self.append()
        first = self.log.read_bytes()
        self.append()
        self.assertTrue(self.log.read_bytes().startswith(first))
        self.assertEqual(self.log.read_text().count(HEADER), 1)
        empty = self.log.parent / 'empty.tsv'
        empty.touch()
        self.log = empty
        self.append()
        self.assertTrue(self.log.read_text().startswith(HEADER))
        self.assertEqual(len(self.log.read_text().splitlines()), 2)

    def test_false_empty_stat_never_truncates_prior_evidence(self):
        self.append()
        before = self.log.read_bytes()
        # Inject only the false stat result; all actual appends still use a real file.
        wrapper = r'''function [() {
  if [[ "$#" == 4 && "$1" == '!' && "$2" == '-s' ]]; then return 0; fi
  builtin [ "$@"
}
export -f '['
bash "$@"
'''
        out = subprocess.run(['bash', '-c', wrapper, 'fixture', str(LOG), str(self.log),
                              'test', 'after false stat', 'fixture', 'artifact.txt', 'pass'],
                             capture_output=True, text=True, timeout=10)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertTrue(self.log.read_bytes().startswith(before))
        self.assertEqual(self.log.read_text().count(HEADER), 2)
        self.assertIn('after false stat', self.log.read_text())

    def test_field_sanitization_and_existing_evidence_survive(self):
        self.append('=phase', 'line\nwith\ttabs', '+formula', '@evidence', '-result')
        fields = self.log.read_text().splitlines()[1].split('\t')
        self.assertEqual(fields[1:], ["'=phase", 'line with tabs', "'+formula", "'@evidence", "'-result"])

    def test_invalid_arguments_do_not_create_a_log(self):
        out = subprocess.run(['bash', str(LOG), str(self.log), 'missing fields'],
                             capture_output=True, text=True, timeout=10)
        self.assertNotEqual(out.returncode, 0)
        self.assertFalse(self.log.exists())


class UpdateInventoryTests(unittest.TestCase):
    def test_each_changed_source_has_a_native_destination_and_matching_provenance(self):
        update = json.loads((ROOT / 'provenance/updates/0.15.3.json').read_text())
        source = json.loads((ROOT / 'provenance/source.json').read_text())
        files = {entry['source']: entry for entry in source['files']}
        self.assertEqual(update['source_subtree'], 'f66b1f3ed67364a915305457ee9099edc44f9333')
        self.assertEqual(update['to_revision'], source['revision'])
        self.assertEqual(update['to_version'], '0.15.3')
        self.assertEqual(len(update['changes']), 34)
        self.assertEqual(len({entry['source'] for entry in update['changes']}), 34)
        self.assertEqual(len(files), 158)
        for entry in update['changes']:
            with self.subTest(source=entry['source']):
                self.assertEqual(entry['after_sha256'], files[entry['source']]['source_sha256'])
                self.assertNotEqual(entry['before_sha256'], entry['after_sha256'])
                self.assertEqual(entry['destination'], files[entry['source']]['destination'])
                self.assertTrue((ROOT / entry['destination']).is_file())
                self.assertTrue(entry['handling'])

    def test_native_workflow_text_retains_new_round_and_receipt_requirements(self):
        full = (ROOT / '.agents/skills/poteto-mode/playbooks/autopilot-full.md').read_text()
        for requirement in ("code-ready head SHA", "each later push that changes the PR's patch",
                            'two or more review lanes', 'A defect that a lane filed as a note is a finding',
                            'red test that covers every site', 'CI must pass on that head',
                            'children.tsv', 'No timeout grants permission for two live writers',
                            'even after the last merge', 'never gives or bypasses an approval'):
            self.assertIn(requirement, full)
        shipping = (ROOT / '.agents/skills/poteto-mode/playbooks/shipping.md').read_text()
        self.assertIn('twice at the verdict SHA and once at the current head', shipping)
        self.assertIn('Judge each difference, not each file', shipping)
        self.assertIn('Do not reuse a lane result from a dev server', shipping)
        swarm = (ROOT / '.agents/skills/swarm/SKILL.md').read_text()
        self.assertIn('sample count, what one sample is, order', swarm)
        self.assertIn('rerun that worker once', swarm)
        self.assertIn('A gap does not count as a pass', swarm)
        plan = (ROOT / '.agents/skills/poteto-mode/playbooks/multi-phase-plan.md').read_text()
        self.assertIn('no earlier status message reported', plan)
        self.assertIn("log this tick's row", plan)


if __name__ == '__main__':
    unittest.main()
