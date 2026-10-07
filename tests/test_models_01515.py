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

    def test_custom_luna_low_wins_over_medium_budget(self):
        luna = {'model': 'openai/gpt-6-luna', 'reasoning_effort': 'low', 'fast': True}
        profile = {'preset': 'custom', 'approved_difference': 'fixture consent', 'budget': 'medium',
                   'roles': {'how explorer': luna}}
        obs = observed()
        obs['models'][luna['model']] = {
            'reasoning_efforts': ['none', 'low', 'medium', 'high', 'xhigh', 'max'], 'fast': True}
        self.assertEqual(m.requested(profile, 'how explorer'), [luna])
        self.assertEqual(m.resolve(profile, 'how explorer', obs), [luna])
        self.assertEqual(m.work_order(profile, 'how explorer', obs)['budget'], 'medium')

    def test_custom_unsupported_effort_is_rejected(self):
        profile = {'preset': 'custom', 'approved_difference': 'fixture consent', 'budget': 'medium',
                   'roles': {'how explorer': {'model': 'openai/gpt-6-luna', 'reasoning_effort': 'low'}}}
        obs = observed()
        obs['models']['openai/gpt-6-luna'] = {'reasoning_efforts': ['high'], 'fast': False}
        with self.assertRaisesRegex(m.ModelError, 'Unsupported reasoning'):
            m.resolve(profile, 'how explorer', obs)

    def test_custom_role_without_effort_still_takes_medium_budget(self):
        profile = {'preset': 'custom', 'approved_difference': 'fixture consent', 'budget': 'medium',
                   'roles': {'how explorer': {'model': 'openai/gpt-6-luna', 'fast': True}}}
        obs = observed()
        obs['models']['openai/gpt-6-luna'] = {'reasoning_efforts': ['high', 'low'], 'fast': True}
        self.assertEqual(m.resolve(profile, 'how explorer', obs),
                         [{'model': 'openai/gpt-6-luna', 'reasoning_effort': 'high', 'fast': True}])
        other = {'preset': 'custom', 'approved_difference': 'fixture consent', 'budget': 'medium',
                 'roles': {'how explorer': {'model': 'openai/gpt-6-luna', 'reasoning_effort': 'low', 'fast': True}}}
        self.assertEqual(m.resolve(other, 'feature', obs),
                         [{'model': 'xai/grok-4.7', 'reasoning_effort': 'high', 'fast': True}])

    def test_mixed_custom_panel_keeps_pinned_medium_and_budgets_unpinned_seat(self):
        pinned = {'model': 'openai/gpt-6-luna', 'reasoning_effort': 'medium'}
        profile = {'preset': 'custom', 'approved_difference': 'fixture consent', 'budget': 'medium',
                   'panels': {'arena runners': [pinned, {'model': 'xai/grok-4.7'}]}}
        obs = observed()
        obs['models'][pinned['model']] = {'reasoning_efforts': ['medium', 'high'], 'fast': False}
        self.assertEqual(m.resolve(profile, 'arena runners', obs), [
            pinned, {'model': 'xai/grok-4.7', 'reasoning_effort': 'high'}])

    def test_aliases_faithful_native_and_single_model_keep_budget_contracts(self):
        parent = {'model': 'anthropic/claude-opus-5-5', 'reasoning_effort': 'max', 'fast': True}
        obs = observed()
        obs['parent'] = parent
        for alias in ('inherit-parent', 'auto'):
            profile = {'preset': 'custom', 'approved_difference': 'fixture consent', 'budget': 'medium',
                       'roles': {'feature': alias}}
            with self.subTest(alias=alias):
                self.assertEqual(m.resolve(profile, 'feature', obs), [parent])
        self.assertEqual(m.resolve({'preset': 'capy-native', 'budget': 'medium'}, 'feature', observed()),
                         [{'model': 'xai/grok-4.7', 'reasoning_effort': 'high', 'fast': True}])
        self.assertEqual(m.resolve({'preset': 'upstream-faithful', 'budget': 'medium'}, 'how explainer', observed()),
                         [{'model': 'anthropic/claude-opus-5-5', 'reasoning_effort': 'high'}])
        for preset in ('capy-native', 'upstream-faithful'):
            pinned = {'preset': preset, 'budget': 'medium',
                      'roles': {'feature': {'model': 'xai/grok-4.7', 'reasoning_effort': 'low', 'fast': True}}}
            with self.subTest(preset=preset), self.assertRaisesRegex(m.ModelError, 'faithful settings changed'):
                m.requested(pinned, 'feature')
        self.assertEqual(m.resolve({'preset': 'single-model', 'approved_difference': 'fixture consent',
                                    'budget': 'medium'}, 'arena runners', obs), [parent, parent])
        obs['models']['openai/gpt-6-luna'] = {'reasoning_efforts': ['low', 'high'], 'fast': False}
        single_pin = {'preset': 'single-model', 'approved_difference': 'fixture consent', 'budget': 'medium',
                      'roles': {'feature': {'model': 'openai/gpt-6-luna', 'reasoning_effort': 'low'}}}
        self.assertEqual(m.resolve(single_pin, 'feature', obs),
                         [{'model': 'openai/gpt-6-luna', 'reasoning_effort': 'high'}])

    def test_cli_base_profile_keeps_medium_budget_and_custom_override(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / 'base.json'
            override = Path(directory) / 'override.json'
            obs_path = Path(directory) / 'observed.json'
            base.write_text(json.dumps({
                'version': 2, 'preset': 'custom', 'approved_difference': 'fixture base consent',
                'budget': 'medium',
            }))
            override.write_text(json.dumps({
                'version': 2, 'preset': 'custom', 'approved_difference': 'fixture override consent',
                'roles': {'how explorer': {'model': 'openai/gpt-6-luna', 'reasoning_effort': 'low', 'fast': True}},
            }))
            obs = observed()
            obs['models']['openai/gpt-6-luna'] = {'reasoning_efforts': ['low', 'high'], 'fast': True}
            obs_path.write_text(json.dumps(obs))
            cases = (
                ('how explorer', [{'model': 'openai/gpt-6-luna', 'reasoning_effort': 'low', 'fast': True}]),
                ('feature', [{'model': 'xai/grok-4.7', 'reasoning_effort': 'high', 'fast': True}]),
            )
            for role, expected in cases:
                command = [sys.executable, str(SCRIPTS / 'models.py'), 'resolve', str(override),
                           '--base-profile', str(base), '--role', role, '--observed', str(obs_path)]
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                output = json.loads(result.stdout)
                self.assertEqual(output['budget'], 'medium')
                self.assertEqual(output['preset'], 'custom')
                self.assertEqual(output['choices'], expected)

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
