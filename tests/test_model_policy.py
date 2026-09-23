"""Model decisions tested through public functions and CLIs, not phrase presence."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT/'.agents/skills/poteto-mode/scripts'
def load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod
m = load('policy', SCRIPTS/'models.py')
t = load('task_policy', SCRIPTS/'tasks.py')
EXPECTED = [
    {'model':'anthropic/claude-opus-5-5','reasoning_effort':'max'},
    {'model':'openai/gpt-5.6-sol','reasoning_effort':'max'},
    {'model':'xai/grok-4.7','reasoning_effort':'xhigh','fast':True},
]

def observed():
    return {'source':'synthetic unit fixture, NOT an authenticated Capy observation',
            'models':{x['model']:{'reasoning_efforts':['medium','high','xhigh','max'], 'fast':True} for x in EXPECTED},
            'parent':EXPECTED[0],
            'bindings': {x['model']:{'model':x['model'],'source':'synthetic picker identity fixture, NOT live evidence'}
                         for x in (EXPECTED[0],EXPECTED[2])}}

def records():
    return [{'seat':i,'native_task_id':f'fixture-{i}','status':'done','settings':x,
             'accepted':True,'artifact':f'fixture-output-{i}'} for i,x in enumerate(EXPECTED)]

class ModelPolicyTests(unittest.TestCase):
    def test_faithful_panels_preserve_all_three_identities_and_efforts(self):
        for panel in m.PANEL_NAMES:
            self.assertEqual(m.resolve({}, panel, observed()), EXPECTED)
    def test_implementation_and_prose_do_not_collapse_to_parent(self):
        for role in ('feature','refactoring','bug-fix','perf-issue','hillclimb','how explorer','why investigators','swarm workers'):
            self.assertEqual(m.resolve({},role,observed()),[EXPECTED[2]])
        for role in ('judgment and prose','hardest tasks','how explainer','why synthesizer','reflect judgment','reflect divergent','reflect synthesizer'):
            self.assertEqual(m.resolve({},role,observed()),[EXPECTED[0]])
        self.assertEqual(m.resolve({},'reflect tooling',observed()),[EXPECTED[1]])
    def test_unspecified_upstream_comment_role_inherits_actual_parent(self):
        self.assertEqual(m.resolve({},'comment review',observed()),[EXPECTED[0]])
    def test_no_observation_is_not_entitlement(self):
        with self.assertRaises(m.ModelError): m.resolve({},'arena runners')
    def test_missing_model_fails_whole_panel_without_partial_fallback(self):
        obs=observed();del obs['models'][EXPECTED[2]['model']]
        with self.assertRaisesRegex(m.ModelError,'unavailable'):m.resolve({},'arena runners',obs)
    def test_effort_is_not_silently_dropped_or_approximated(self):
        obs=observed();obs['models'][EXPECTED[0]['model']]['reasoning_efforts']=['high']
        with self.assertRaisesRegex(m.ModelError,'Unsupported reasoning'):m.resolve({},'arena runners',obs)
    def test_fast_priority_is_checked_separately(self):
        obs=observed();obs['models'][EXPECTED[2]['model']]['fast']=False
        with self.assertRaisesRegex(m.ModelError,'Priority'):m.resolve({},'feature',obs)
    def test_budget_is_explicit_and_applies_to_every_real_role(self):
        for budget, effort in [('large','xhigh'),('medium','high'),('small','medium')]:
            values=m.resolve({'budget':budget},'arena runners',observed())
            self.assertEqual([v['reasoning_effort'] for v in values],[effort]*3)
            self.assertTrue(values[2]['fast'])
    def test_four_aliases_cannot_masquerade_as_four_faithful_models(self):
        values=[dict(EXPECTED[1],model=x) for x in ('openai/gpt-5.6-sol','codex/gpt-5.6-sol','copilot/gpt-5.6-sol','azure/gpt-5.6-sol')]
        self.assertEqual(len({m.identity(x['model']) for x in values}),1)
        with self.assertRaises(m.ModelError):m.requested({'panels':{'arena runners':values}},'arena runners')
    def test_same_weights_billing_override_is_explicit_and_supported(self):
        values=copy.deepcopy(EXPECTED);values[1]['model']='codex/gpt-5.6-sol'
        obs=observed();obs['models']['codex/gpt-5.6-sol']=obs['models']['openai/gpt-5.6-sol']
        order=m.work_order({'panels':{'arena runners':values}},'arena runners',obs)
        self.assertEqual(order['choices'],values);self.assertEqual(order['distinct_models'],3)
        self.assertEqual(order['families'],['anthropic','openai','xai'])
    def test_same_model_is_opt_in_and_labelled_not_silent(self):
        with self.assertRaises(m.ModelError):m.resolve({'preset':'single-model'},'arena runners',observed())
        order=m.work_order({'preset':'single-model','approved_difference':'fixture explicit consent'},'arena runners',observed())
        self.assertEqual(order['choices'],[EXPECTED[0]]*3);self.assertEqual(order['distinct_models'],1)
        self.assertEqual(order['preset'],'single-model')
    def test_custom_panel_needs_approval_and_architect_has_two_minimum(self):
        profile={'preset':'custom','approved_difference':'fixture consent','panels':{'architect runners':[EXPECTED[0]]}}
        with self.assertRaises(m.ModelError):m.validate(profile)
        profile['panels']['architect runners'].append(EXPECTED[1]);m.validate(profile)
    def test_v1_profile_is_not_silently_upgraded(self):
        with self.assertRaises(m.ModelError):m.validate({'version':1,'confirmed_models':[]})
    def test_unknown_fields_roles_and_malformed_choices_fail(self):
        for profile in ([],{'max_parallel':True},{'roles':{'typo':'auto'}},{'preset':'unknown'},
                        {'roles':{'feature':{'model':'x','fast':'yes'}}},{'budget':'cheap'},
                        {'roles':{'feature':{'model':'auto','reasoning_effort':'max'}}}):
            with self.subTest(profile=profile),self.assertRaises(m.ModelError):m.validate(profile)
    def test_concurrency_limits_waves_not_number_of_seats(self):
        self.assertEqual(m.work_order({},'arena runners',observed())['waves'],[[0,1,2]])
        self.assertEqual(m.work_order({'max_parallel':1},'arena runners',observed())['waves'],[[0],[1],[2]])
    def test_pool_is_not_a_launchable_panel(self):
        order=m.work_order({},'arena cross-judge pool',observed())
        with self.assertRaises(m.ModelError):m.check_run(order,records())
    def test_judge_is_one_seat_after_all_candidates_with_different_family(self):
        order=m.work_order({},'arena runners',observed())
        judge=m.select_judge({},observed(),order,records())
        self.assertEqual(judge['choices'],[EXPECTED[1]])
        self.assertEqual(judge['after_task_ids'],['fixture-0','fixture-1','fixture-2'])
        self.assertTrue(judge['different_parent_family'])
    def test_judge_waits_for_live_failed_idle_and_missing_candidates(self):
        order=m.work_order({},'arena runners',observed())
        for state in ('working','waiting','idle','failed','draft'):
            results=records();results[-1]['status']=state
            with self.subTest(state=state),self.assertRaises(m.ModelError):m.select_judge({},observed(),order,results)
        with self.assertRaises(m.ModelError):m.select_judge({},observed(),order,records()[:-1])
    def test_unaccepted_or_forged_settings_block_evidence_gate(self):
        order=m.work_order({},'arena runners',observed())
        for key,value in [('accepted',False),('settings',{'model':EXPECTED[0]['model']}),('artifact','')]:
            results=records();results[0][key]=value
            with self.subTest(key=key),self.assertRaises(m.ModelError):m.check_run(order,results)
    def test_duplicate_task_or_seat_cannot_satisfy_two_candidates(self):
        order=m.work_order({},'arena runners',observed())
        for key,value in [('seat',0),('native_task_id','fixture-0')]:
            results=records();results[1][key]=value
            with self.subTest(key=key),self.assertRaises(m.ModelError):m.check_run(order,results)
    def test_record_checker_never_claims_remote_authentication(self):
        out=m.check_run(m.work_order({},'arena runners',observed()),records())
        self.assertEqual(out['status'],'records-match-work-order');self.assertFalse(out['native_execution_verified'])
    def test_tasks_route_through_same_policy(self):
        plan=json.loads((ROOT/'examples/plan.json').read_text())
        out=t.prepare(t.with_profile(plan,{},observed()))
        self.assertEqual(out['tasks'][0]['expected_settings'],EXPECTED[2])
        self.assertEqual(out['tasks'][2]['expected_settings'],EXPECTED[0])
        plan['tasks'][0]['model']='inherit-parent'
        with self.assertRaises(ValueError):t.with_profile(plan,{},observed())
    def test_role_layering_merges_keys_and_rejects_legacy(self):
        merged=m.merge_profiles({'budget':'medium','roles':{'feature':EXPECTED[2]}}, {'max_parallel':2})
        self.assertEqual(merged['budget'],'medium');self.assertEqual(merged['max_parallel'],2)
        self.assertEqual(merged['roles']['feature'],EXPECTED[2])
        with self.assertRaises(m.ModelError):m.merge_profiles({'version':1},{})
    def test_cli_emits_literal_faithful_settings_and_nonzero_on_unavailable(self):
        with tempfile.TemporaryDirectory() as d:
            obs=Path(d)/'observed.json';obs.write_text(json.dumps(observed()))
            cmd=[sys.executable,str(SCRIPTS/'models.py'),'resolve',str(ROOT/'.agents/pstack.models.example.json'),
                 '--role','arena runners','--observed',str(obs)]
            out=subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(out.returncode,0,out.stderr);self.assertEqual(json.loads(out.stdout)['choices'],EXPECTED)
            obs.write_text(json.dumps({'source':'empty fixture','models':{}}))
            bad=subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(bad.returncode,2);self.assertEqual(bad.stdout,'')
    def test_task_cli_cannot_inherit_without_observed_policy(self):
        cmd=[sys.executable,str(SCRIPTS/'tasks.py'),'prepare',str(ROOT/'examples/plan.json')]
        out=subprocess.run(cmd,capture_output=True,text=True)
        self.assertEqual(out.returncode,2)
        out=subprocess.run(cmd+['--structure-only'],capture_output=True,text=True)
        self.assertEqual(out.returncode,0,out.stderr);self.assertFalse(json.loads(out.stdout)['model_policy_resolved'])

if __name__=='__main__':unittest.main()
