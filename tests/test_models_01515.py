"""0.15.15 resolution behavior. Synthetic observations are not live model evidence."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_model_policy import EXPECTED, SCRIPTS, m, observed


class NativePolicyTests(unittest.TestCase):
    def without_priority(self):
        obs = observed()
        obs['models']['xai/grok-4.7']['fast'] = False
        return obs

    def test_no_profile_uses_native_large_with_labelled_priority_omission(self):
        order = m.work_order({}, 'arena runners', self.without_priority())
        self.assertEqual(order['preset'], 'capy-native')
        self.assertEqual(order['budget'], 'large')
        self.assertEqual(order['upstream_version'], '0.15.15')
        self.assertEqual(order['choices'], [
            {'model': 'anthropic/claude-opus-5-5', 'reasoning_effort': 'xhigh'},
            {'model': 'xai/grok-4.7', 'reasoning_effort': 'xhigh'},
        ])
        self.assertEqual(order['adaptations'], [{
            'seat': 1, 'field': 'fast', 'requested': True, 'applied': None,
            'reason': 'capy-native omits unsupported priority; model identity and reasoning effort are unchanged',
        }])
        self.assertEqual(order['families'], ['anthropic', 'xai'])
        self.assertEqual(order['distinct_models'], 2)
        self.assertEqual(order['waves'], [[0, 1]])
        self.assertEqual(m.requested({}, 'arena runners'), EXPECTED)
        self.assertFalse(order['native_execution_verified'])

    def test_every_grok_role_adapts_and_opus_roles_preserve_xhigh(self):
        grok_roles = {'feature', 'refactoring', 'bug-fix', 'perf-issue', 'hillclimb',
                     'how explorer', 'why investigators', 'swarm workers', 'reflect tooling'}
        opus_roles = {'judgment and prose', 'hardest tasks', 'how explainer', 'why synthesizer',
                     'reflect judgment', 'reflect divergent', 'reflect synthesizer'}
        for role in grok_roles:
            with self.subTest(role=role):
                order = m.work_order({}, role, self.without_priority())
                self.assertEqual(order['choices'], [{'model': 'xai/grok-4.7', 'reasoning_effort': 'xhigh'}])
                self.assertEqual(order['adaptations'][0]['seat'], 0)
        for role in opus_roles:
            with self.subTest(role=role):
                order = m.work_order({}, role, self.without_priority())
                self.assertEqual(order['choices'], [{'model': 'anthropic/claude-opus-5-5', 'reasoning_effort': 'xhigh'}])
                self.assertEqual(order['adaptations'], [])

    def test_supported_priority_is_not_removed(self):
        order = m.work_order({}, 'feature', observed())
        self.assertEqual(order['choices'], [{'model': 'xai/grok-4.7', 'reasoning_effort': 'xhigh', 'fast': True}])
        self.assertEqual(order['adaptations'], [])

    def test_existing_profiles_without_native_selection_remain_strict(self):
        profiles = [{'version': 2}, {'budget': 'large'}, {'roles': {}},
                    {'preset': 'upstream-faithful'},
                    {'preset': 'custom', 'approved_difference': 'fixture consent'},
                    {'preset': 'single-model', 'approved_difference': 'fixture consent'}]
        obs = self.without_priority()
        obs['parent'] = dict(EXPECTED[1])
        for profile in profiles:
            with self.subTest(profile=profile), self.assertRaisesRegex(m.ModelError, 'Priority/fast unavailable'):
                m.work_order(profile, 'feature', obs)
        self.assertEqual(m.work_order({'version': 2, 'preset': 'capy-native'}, 'feature', obs)['adaptations'][0]['field'], 'fast')

    def test_native_does_not_relax_binding_effort_or_identity_checks(self):
        for mutation, error in [('binding', 'never guess an ID'), ('effort', 'Unsupported reasoning')]:
            obs = self.without_priority()
            if mutation == 'binding':
                del obs['bindings']['xai/grok-4.7']
            else:
                obs['models']['xai/grok-4.7']['reasoning_efforts'] = ['high']
            with self.subTest(mutation=mutation), self.assertRaisesRegex(m.ModelError, error):
                m.work_order({}, 'feature', obs)
        profile = {'preset': 'capy-native', 'roles': {'feature': {'model': 'xai/grok-4.6', 'reasoning_effort': 'xhigh', 'fast': True}}}
        before = copy.deepcopy(profile)
        with self.assertRaisesRegex(m.ModelError, 'faithful identity changed'):
            m.work_order(profile, 'feature', observed())
        self.assertEqual(profile, before)

    def test_explicit_aliases_inherit_settings_and_report_real_diversity(self):
        for alias in ('auto', 'inherit-parent'):
            profile = {'preset': 'capy-native', 'budget': 'small',
                       'roles': {'feature': alias}, 'panels': {'arena runners': [alias, alias]}}
            obs = observed()
            obs['parent'] = {'model': 'anthropic/claude-opus-5-5', 'reasoning_effort': 'max', 'fast': True}
            order = m.work_order(profile, 'arena runners', obs)
            self.assertEqual(order['choices'], [obs['parent'], obs['parent']])
            self.assertEqual(order['inherited_seats'], [0, 1])
            self.assertEqual(order['distinct_models'], 1)
            self.assertEqual(order['families'], ['anthropic'])
            self.assertEqual(order['adaptations'], [])
            self.assertEqual(m.resolve(profile, 'feature', obs), [obs['parent']])
            obs['models'][obs['parent']['model']]['fast'] = False
            with self.assertRaisesRegex(m.ModelError, 'Priority/fast unavailable'):
                m.resolve(profile, 'feature', obs)

    def test_unselected_alias_requires_approval_or_native_selection(self):
        with self.assertRaisesRegex(m.ModelError, 'faithful identity changed'):
            m.requested({'roles': {'feature': 'auto'}}, 'feature')
        with self.assertRaisesRegex(m.ModelError, 'Inheritance requires'):
            obs = observed()
            del obs['parent']
            m.resolve({'preset': 'capy-native', 'roles': {'feature': 'auto'}}, 'feature', obs)

    def test_old_strict_custom_effort_pin_is_not_overwritten_by_new_default_budget(self):
        profile = {'preset': 'custom', 'approved_difference': 'fixture consent',
                   'roles': {'feature': {'model': 'anthropic/claude-opus-5-5', 'reasoning_effort': 'max'}}}
        self.assertEqual(m.resolve(profile, 'feature', observed()), [{'model': 'anthropic/claude-opus-5-5', 'reasoning_effort': 'max'}])
        self.assertEqual(m.work_order(profile, 'feature', observed())['budget'], 'unlimited')

    def test_merge_preserves_explicit_policy_selection_and_strict_legacy(self):
        cases = [({}, {}, 'capy-native'), ({}, {'version': 2}, 'upstream-faithful'),
                 ({'version': 2}, {}, 'upstream-faithful'),
                 ({'preset': 'capy-native'}, {'max_parallel': 1}, 'capy-native'),
                 ({'preset': 'capy-native'}, {'preset': 'upstream-faithful'}, 'upstream-faithful')]
        for base, override, expected in cases:
            with self.subTest(base=base, override=override):
                profile = m.merge_profiles(base, override)
                self.assertEqual(m.work_order(profile, 'arena runners', observed())['preset'], expected)

    def test_adapted_records_and_judge_use_applied_not_requested_priority(self):
        obs = self.without_priority()
        order = m.work_order({}, 'arena runners', obs)
        records = [{'seat': i, 'native_task_id': f'fixture-{i}', 'status': 'done',
                    'accepted': True, 'artifact': f'fixture-{i}.txt', 'settings': settings}
                   for i, settings in enumerate(order['choices'])]
        self.assertEqual(m.check_run(order, records)['status'], 'records-match-work-order')
        judge = m.select_judge({}, obs, order, records)
        self.assertEqual(judge['choices'], [{'model': 'xai/grok-4.7', 'reasoning_effort': 'xhigh'}])
        self.assertEqual(judge['adaptations'], [dict(order['adaptations'][0], seat=0)])
        self.assertEqual(judge['after_task_ids'], ['fixture-0', 'fixture-1'])
        records[1]['settings'] = dict(records[1]['settings'], fast=True)
        with self.assertRaisesRegex(m.ModelError, 'different settings'):
            m.check_run(order, records)

    def test_cli_reports_native_adaptation_and_strict_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            profile = Path(directory) / 'profile.json'
            obs = Path(directory) / 'observed.json'
            profile.write_text('{}')
            obs.write_text(json.dumps(self.without_priority()))
            command = [sys.executable, str(SCRIPTS / 'models.py'), 'resolve', str(profile),
                       '--role', 'reflect tooling', '--observed', str(obs)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual(output['choices'], [{'model': 'xai/grok-4.7', 'reasoning_effort': 'xhigh'}])
            self.assertEqual(output['adaptations'][0]['field'], 'fast')
            profile.write_text('{"version": 2}')
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, '')
            self.assertIn('Priority/fast unavailable', result.stderr)


if __name__ == '__main__':
    unittest.main()
