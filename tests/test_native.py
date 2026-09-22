"""Behavioral tests of the self-contained distribution and its public CLIs."""
from __future__ import annotations
import copy
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / '.agents'
SCRIPTS = BUNDLE / 'skills/poteto-mode/scripts'

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

port = module('port', ROOT / 'tools/pstack.py')
models = module('models', SCRIPTS / 'models.py')
tasks = module('tasks', SCRIPTS / 'tasks.py')
EXPECTED = {'architect','arena','automate-me','blast-radius','create-verification-skill',
            'figure-it-out','how','interrogate','maintain-verification-skill','make-bot-ui',
            'no-comments','poteto-mode','recall','reflect','setup-pstack','show-me-your-work',
            'swarm','tdd','teach','technical-writing','typescript-best-practices','unslop','why'}


def cli(script, *args, cwd=None, env=None):
    return subprocess.run([sys.executable, str(script), *map(str, args)], cwd=cwd, env=env,
                          capture_output=True, text=True, timeout=30)


def broken_links(root):
    failures = []
    for file in root.rglob('*.md'):
        for href in re.findall(r'\]\(([^\s)]+)\)', file.read_text()):
            path = href.partition('#')[0]
            if not path or ':' in path or path.startswith('/') or path == 'url':
                continue  # "url" is a literal illustrative citation in a prompt template.
            if not (file.parent / path).exists():
                failures.append(f'{file.relative_to(root)} -> {path}')
    return failures


class DistributionTests(unittest.TestCase):
    def test_complete_catalog(self):
        info = json.loads((ROOT / 'pstack.json').read_text())
        names = {p.parent.name for p in (BUNDLE / 'skills').glob('*/SKILL.md')}
        self.assertEqual(len(names), 52)
        self.assertTrue(EXPECTED <= names)
        self.assertEqual(len([n for n in names if n.startswith('principle-')]), 23)
        self.assertEqual(sorted(names), info['skills'])
        self.assertFalse(info['runtime_dependency_on_upstream'])

    def test_all_playbooks_and_benny_roles(self):
        self.assertEqual(len(list((BUNDLE / 'skills/poteto-mode/playbooks').glob('*.md'))), 23)
        self.assertEqual(len(list((BUNDLE / 'automations/benny/skills').glob('*/SKILL.md'))), 3)
        self.assertEqual({p.name for p in (BUNDLE / 'roles').glob('*.md')}, {'poteto-agent.md','comment-sicko.md'})
        self.assertGreater((BUNDLE / 'automations/benny/skills/reproduce-and-fix-issues/SKILL.md').stat().st_size, 10000)

    def test_every_source_file_has_a_real_destination(self):
        origin = json.loads((ROOT / 'provenance/source.json').read_text())
        self.assertEqual(origin['subtree'], 'f235052692fba08f7ff40df62775339cb4794c4c')
        self.assertEqual(len(origin['files']), 158)
        self.assertEqual(len({f['source'] for f in origin['files']}), 158)
        for item in origin['files']:
            with self.subTest(source=item['source']):
                self.assertTrue((ROOT / item['destination']).is_file())
                self.assertRegex(item['source_sha256'], r'^[a-f0-9]{64}$')

    def test_skill_bodies_are_not_wrappers(self):
        for file in (BUNDLE / 'skills').glob('*/SKILL.md'):
            text = file.read_text()
            with self.subTest(skill=file.parent.name):
                head, body = text[4:].split('\n---', 1)
                self.assertIn(f'name: {file.parent.name}', head)
                self.assertIn('description:', head)
                if file.parent.name == 'bro':
                    self.assertEqual(body.strip(), 'Restate your last message. Stop using jargon and speak coherently. State it more simply and concisely, like one human talking to another.')
                else:
                    self.assertGreater(len(body.split()), 55)
                self.assertNotIn('CAPY.md', body)
                self.assertNotIn('upstream/', body)
                self.assertNotIn('disable-model-invocation', head)

    def test_no_gitlink_or_adapter_dependency(self):
        self.assertFalse((ROOT / '_upstream').exists())
        self.assertFalse((ROOT / '.gitmodules').exists())
        self.assertFalse((ROOT / 'adapter').exists())
        self.assertFalse((BUNDLE / 'skills/pstack-capy').exists())
        self.assertFalse((ROOT / '.cursor-plugin').exists())

    def test_no_executable_cursor_platform_contracts(self):
        forbidden = ('.cursor/', 'subagent_type', 'run_in_background', 'cloud_base_branch',
                     'cursor-team-kit', 'agent-transcripts/', 'Readonly/Ask mode',
                     'built-in `automate`', '/add-plugin', '/setup-pstack rule')
        for file in BUNDLE.rglob('*.md'):
            text = file.read_text()
            for token in forbidden:
                with self.subTest(path=str(file.relative_to(BUNDLE)), token=token):
                    self.assertNotIn(token, text)

    def test_local_markdown_links(self):
        self.assertEqual(broken_links(ROOT), [])

    def test_catalog_checks_every_hash_and_mode(self):
        output = cli(ROOT / 'tools/catalog.py', '--check')
        self.assertEqual(output.returncode, 0, output.stderr)
        self.assertEqual(port.doctor(ROOT)['skills'], 52)
        self.assertEqual(port.doctor(ROOT)['playbooks'], 23)
        self.assertFalse(port.doctor(ROOT)['upstream_required'])

    def test_original_mit_notice_retained(self):
        self.assertIn('Lauren Tan', (ROOT / 'LICENSE').read_text())
        self.assertEqual((ROOT / 'LICENSE').read_bytes(), (BUNDLE / 'LICENSE').read_bytes())
        self.assertIn('Permission is hereby granted', (BUNDLE / 'LICENSE').read_text())

    def test_task_and_shipping_contracts_remain(self):
        arena = (BUNDLE / 'skills/arena/SKILL.md').read_text()
        self.assertIn('after all', arena.lower())
        self.assertIn('not with the candidates', arena)
        self.assertIn('Do not replace a timed-out owner', arena)
        shipping = (BUNDLE / 'skills/poteto-mode/playbooks/shipping.md').read_text()
        self.assertIn('contiguous verified run', shipping)
        self.assertIn('patch-id', shipping)
        self.assertIn('did not write the code', shipping)

    def test_benny_retains_repro_and_no_post_gates(self):
        text = (BUNDLE / 'automations/benny/skills/reproduce-and-fix-issues/SKILL.md').read_text()
        self.assertIn('Never post a root message in the source channel', text)
        self.assertIn('must appear twice', text)
        self.assertIn('No confirmed repro means no authored fix', text)
        self.assertIn('Do not poll or sleep', text)
        self.assertIn('triage_identity_user_id', text)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.target = self.root / 'project'
        self.want = {'.agents/skills/demo/SKILL.md': (b'full demo workflow\n', 0o644),
                     '.agents/skills/demo/scripts/check.sh': (b'#!/bin/sh\nexit 0\n', 0o755)}

    def install(self):
        return port.apply(self.target, self.want)

    def test_dry_run_has_no_effect(self):
        report = port.apply(self.target, self.want, dry_run=True)
        self.assertEqual(report['write'], sorted(self.want))
        self.assertFalse(self.target.exists())

    def test_identical_install_is_idempotent(self):
        self.install()
        stamps = {n: (self.target/n).stat().st_mtime_ns for n in self.want}
        report = self.install()
        self.assertEqual(report, {'write': [], 'remove': [], 'unchanged': 2})
        self.assertEqual(stamps, {n:(self.target/n).stat().st_mtime_ns for n in self.want})

    def test_preserves_unmanaged_instructions_and_profile(self):
        (self.target/'.agents').mkdir(parents=True)
        (self.target/'AGENTS.md').write_text('existing')
        (self.target/'.agents/pstack.models.json').write_text('{"custom":true}')
        self.install()
        self.assertEqual((self.target/'AGENTS.md').read_text(), 'existing')
        self.assertEqual((self.target/'.agents/pstack.models.json').read_text(), '{"custom":true}')

    def test_unmanaged_collision_blocks_all_writes(self):
        file = self.target / next(iter(self.want))
        file.parent.mkdir(parents=True); file.write_text('mine')
        with self.assertRaises(port.PortError): self.install()
        self.assertEqual(file.read_text(), 'mine')
        self.assertFalse((self.target/port.MANIFEST).exists())
        self.assertFalse((self.target/'.agents/skills/demo/scripts/check.sh').exists())

    def test_modified_file_blocks_update(self):
        self.install(); file = self.target/next(iter(self.want)); file.write_text('modified')
        with self.assertRaises(port.PortError): self.install()
        self.assertEqual(file.read_text(), 'modified')

    def test_missing_owned_file_blocks_update(self):
        self.install(); (self.target/next(iter(self.want))).unlink()
        with self.assertRaises(port.PortError): self.install()

    def test_changed_mode_blocks_update(self):
        self.install(); (self.target/'.agents/skills/demo/scripts/check.sh').chmod(0o644)
        with self.assertRaises(port.PortError): self.install()

    def test_live_lock_refused(self):
        self.target.mkdir(); (self.target/port.LOCK).write_text('live')
        with self.assertRaises(port.PortError): self.install()
        self.assertEqual((self.target/port.LOCK).read_text(), 'live')

    def test_symlink_target_refused(self):
        other=self.root/'other';other.mkdir();self.target.symlink_to(other, target_is_directory=True)
        with self.assertRaises(port.PortError): self.install()
        self.assertEqual(list(other.iterdir()), [])

    def test_symlink_parent_refused(self):
        other=self.root/'other';other.mkdir();self.target.mkdir();(self.target/'.agents').symlink_to(other, target_is_directory=True)
        with self.assertRaises(port.PortError): self.install()
        self.assertEqual(list(other.iterdir()), [])

    def test_path_escape_refused(self):
        for name in ('../secret', '/tmp/secret', '.agents/../../secret', '.agents/a//b', '.agents/.git/config', '.agents/a\\b'):
            with self.subTest(path=name), self.assertRaises(port.PortError):
                port.apply(self.target, {name:(b'bad',0o644)})

    def test_manifest_cannot_delete_neighbors(self):
        self.target.mkdir()
        (self.target/'important').write_text('keep')
        value={'format':1,'volume':False,'files':{'important':{'sha256':port.digest(b'keep'),'mode':0o644}}}
        (self.target/port.MANIFEST).write_text(json.dumps(value))
        with self.assertRaises(port.PortError):port.apply(self.target,{},uninstall=True)
        self.assertEqual((self.target/'important').read_text(),'keep')

    def test_uninstall_only_owned_files(self):
        self.install();(self.target/'AGENTS.md').write_text('keep')
        port.apply(self.target,{},uninstall=True)
        self.assertEqual((self.target/'AGENTS.md').read_text(),'keep')
        self.assertFalse((self.target/port.MANIFEST).exists())
        for name in self.want:self.assertFalse((self.target/name).exists())

    def test_uninstall_refuses_edits(self):
        self.install();file=self.target/next(iter(self.want));file.write_text('edit')
        with self.assertRaises(port.PortError):port.apply(self.target,{},uninstall=True)
        self.assertEqual(file.read_text(),'edit')

    def test_upgrade_removes_only_stale_owned_file(self):
        self.install();old = next(iter(self.want)); new=dict(self.want);del new[old]
        new['.agents/skills/other/SKILL.md']=(b'new',0o644)
        report=port.apply(self.target,new)
        self.assertEqual(report['remove'],[old]);self.assertFalse((self.target/old).exists())
        self.assertEqual((self.target/'.agents/skills/other/SKILL.md').read_bytes(),b'new')

    def test_failure_rolls_back_files_and_manifest(self):
        self.install();before={p.relative_to(self.target).as_posix():p.read_bytes() for p in self.target.rglob('*') if p.is_file()}
        want={n:(data+b'updated', mode) for n,(data,mode) in self.want.items()}
        real=port.os.replace; calls=0
        def broken(a,b):
            nonlocal calls
            calls+=1
            if calls==2:raise OSError('injected replacement failure')
            return real(a,b)
        with patch.object(port.os,'replace',broken),self.assertRaises(OSError):port.apply(self.target,want)
        after={p.relative_to(self.target).as_posix():p.read_bytes() for p in self.target.rglob('*') if p.is_file()}
        self.assertEqual(before,after)

    def test_full_offline_project_install(self):
        with patch.object(socket,'socket',side_effect=AssertionError('network forbidden')):
            port.apply(self.target,port.payload(False))
            result=port.doctor(self.target)
        self.assertEqual(result['skills'],52);self.assertEqual(result['playbooks'],23)
        self.assertEqual(broken_links(self.target/'.agents'),[])
        self.assertFalse((self.target/'_upstream').exists());self.assertFalse((self.target/'.git').exists())
        for name,item in port.catalog(BUNDLE)['files'].items():
            self.assertEqual((self.target/'.agents'/name).read_bytes(), (BUNDLE/name).read_bytes())

    def test_full_offline_volume_install(self):
        port.apply(self.target,port.payload(True),volume=True)
        self.assertEqual(port.doctor(self.target,True)['skills'],52)
        self.assertFalse((self.target/'.agents').exists());self.assertFalse((self.target/'.capy').exists())
        self.assertEqual(broken_links(self.target),[])

    def test_plain_archive_cli_needs_no_git_or_upstream(self):
        plain=self.root/'archive'
        shutil.copytree(ROOT,plain,ignore=shutil.ignore_patterns('.git','_upstream','node_modules','__pycache__','.native-port','dist'))
        output=cli(plain/'tools/pstack.py','install','--target',self.target,cwd=self.root,env=dict(os.environ,PATH=''))
        self.assertEqual(output.returncode,0,output.stderr)
        check=cli(plain/'tools/pstack.py','doctor','--target',self.target,env=dict(os.environ,PATH=''))
        self.assertEqual(check.returncode,0,check.stderr)
        self.assertEqual(json.loads(check.stdout)['skills'],52)

    def test_tampered_bundle_rejected_before_write(self):
        source=self.root/'source';shutil.copytree(BUNDLE,source/'.agents')
        target=source/'.agents/skills/how/SKILL.md';target.write_text('tampered')
        with patch.object(port,'ROOT',source),self.assertRaises(port.PortError):port.payload(False)
        self.assertFalse(self.target.exists())


class TaskTests(unittest.TestCase):
    def setUp(self):self.plan=json.loads((ROOT/'examples/plan.json').read_text())
    def test_disjoint_concurrency_and_review_dependency(self):
        out=tasks.prepare(self.plan)
        self.assertEqual(out['waves'],[['api','docs'],['review-api']])
        self.assertEqual([x['machine'] for x in out['tasks']],['fresh','fresh','fresh'])
        self.assertTrue(all('CAPY.md' not in x['brief'] and 'skills/poteto-mode/SKILL.md' in x['brief'] for x in out['tasks']))

    def test_shared_reader(self):
        p=copy.deepcopy(self.plan);p['tasks']=[dict(p['tasks'][0],write=False,role='research')]
        self.assertEqual(tasks.prepare(p)['tasks'][0]['machine'],'shared')

    def test_shared_writer_rejected(self):
        self.plan['tasks'][0]['machine']='shared'
        with self.assertRaises(tasks.PlanError):tasks.prepare(self.plan)

    def test_overlap_not_fixed_by_parallelism_one(self):
        self.plan['max_parallel']=1;self.plan['tasks'][1]['scope_paths']=['src/export/file.py']
        with self.assertRaises(tasks.PlanError):tasks.prepare(self.plan)

    def test_stacking_requires_branch_inheritance(self):
        self.plan['tasks'][1].update(scope_paths=['src/export'],depends_on=['api'])
        with self.assertRaises(tasks.PlanError):tasks.prepare(self.plan)
        self.plan['tasks'][1].pop('base_ref');self.plan['tasks'][1]['base_from']='api'
        self.assertEqual(tasks.prepare(self.plan)['waves'],[['api'],['docs','review-api']])

    def test_cycle_and_unknown_dependency(self):
        self.plan['tasks'][0]['depends_on']=['review-api']
        with self.assertRaises(tasks.PlanError):tasks.prepare(self.plan)
        self.plan['tasks'][0]['depends_on']=['missing']
        with self.assertRaises(tasks.PlanError):tasks.prepare(self.plan)

    def test_nesting_cap(self):
        self.plan['parent_depth']=3
        with self.assertRaises(tasks.PlanError):tasks.prepare(self.plan)

    def test_invalid_model_scope_acceptance_and_version(self):
        for update in ({'model':'missing'},{'scope_paths':['../escape']},{'acceptance':[]}):
            p=copy.deepcopy(self.plan);p['tasks'][0].update(update)
            with self.subTest(update=update),self.assertRaises(tasks.PlanError):tasks.prepare(p)
        self.plan['version']=True
        with self.assertRaises(tasks.PlanError):tasks.prepare(self.plan)

    def results(self):
        return [{'id':t['id'],'native_task_id':'native-'+t['id'],'machine_id':'machine-'+t['id'],
                 'status':'done','base_sha':'a'*40,'head_sha':'a'*40,'branch':'test',
                 'changed_paths':[], 'evidence':[{'criterion':c,'artifact':'actual-test-log','result':'pass'} for c in t['acceptance']]}
                for t in self.plan['tasks']]

    def test_results_are_not_shipping_approval(self):
        out=tasks.check_results(self.plan,self.results());self.assertFalse(out['safe_to_ship'])
        self.assertEqual(out['tasks'],3)

    def test_idle_failed_and_waiting_are_not_done(self):
        for status in ('idle','failed','waiting','working'):
            r=self.results();r[0]['status']=status
            with self.subTest(status=status),self.assertRaises(tasks.PlanError):tasks.check_results(self.plan,r)

    def test_missing_failed_duplicate_evidence_rejected(self):
        for evidence in ([],[{'criterion':'wrong','artifact':'log','result':'pass'}],
                         [{'criterion':self.plan['tasks'][0]['acceptance'][0],'artifact':'log','result':'fail'}]):
            r=self.results();r[0]['evidence']=evidence
            with self.subTest(evidence=evidence),self.assertRaises(tasks.PlanError):tasks.check_results(self.plan,r)

    def test_reader_cannot_edit(self):
        r=self.results();r[2]['changed_paths']=['src/export/changed.py']
        with self.assertRaises(tasks.PlanError):tasks.check_results(self.plan,r)

    def test_scope_escape_refused(self):
        r=self.results();r[0]['changed_paths']=['src/auth/secret.py']
        with self.assertRaises(tasks.PlanError):tasks.check_results(self.plan,r)

    def test_stack_base_must_match_real_predecessor(self):
        r=self.results();r[0]['head_sha']='b'*40
        with self.assertRaises(tasks.PlanError):tasks.check_results(self.plan,r)

    def test_duplicate_native_ids_refused(self):
        r=self.results();r[1]['native_task_id']=r[0]['native_task_id']
        with self.assertRaises(tasks.PlanError):tasks.check_results(self.plan,r)

    def test_public_cli_example(self):
        output=cli(SCRIPTS/'tasks.py','prepare',ROOT/'examples/plan.json','--structure-only')
        self.assertEqual(output.returncode,0,output.stderr)
        self.assertEqual(json.loads(output.stdout)['waves'],[['api','docs'],['review-api']])


class BundledCliTests(unittest.TestCase):
    def test_plan_checker_accepts_native_template_and_rejects_missing_lane(self):
        text=(BUNDLE/'skills/poteto-mode/playbooks/multi-phase-plan.md').read_text()
        template=text.split('````markdown\n',1)[1].split('````',1)[0]
        with tempfile.TemporaryDirectory() as d:
            plan=Path(d)/'plan.md';plan.write_text(template)
            out=subprocess.run(['node',str(SCRIPTS/'check-plan.mjs'),str(plan)],capture_output=True,text=True)
            self.assertEqual(out.returncode,0,out.stderr)
            plan.write_text(re.sub(r'^- \[ \] Lane 10\..*\n','',template,flags=re.M))
            bad=subprocess.run(['node',str(SCRIPTS/'check-plan.mjs'),str(plan)],capture_output=True,text=True)
            self.assertNotEqual(bad.returncode,0)
            self.assertIn('expected 1 to 10',bad.stderr)

    def test_worktree_audit_handles_spaces_without_deleting(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'repo with spaces';root.mkdir()
            def git(*args):
                out=subprocess.run(['git','-C',str(root),*args],capture_output=True,text=True)
                self.assertEqual(out.returncode,0,out.stderr)
                return out
            git('init','-b','main');git('-c','user.name=Test','-c','user.email=test@example.invalid','commit','--allow-empty','-m','fixture')
            other=Path(d)/'other with spaces';git('worktree','add','-b','task',str(other))
            (other/'untracked').write_text('preserve')
            out=subprocess.run(['bash',str(SCRIPTS/'worktree-audit.sh'),str(root)],capture_output=True,text=True)
            self.assertEqual(out.returncode,0,out.stderr)
            records=json.loads(out.stdout)
            self.assertEqual(len(records),2)
            self.assertTrue(any(x['path']==str(other) and x['dirty'] for x in records))
            self.assertTrue(all(x['safe_to_delete'] is False for x in records))
            self.assertEqual((other/'untracked').read_text(),'preserve')


if __name__ == '__main__':unittest.main()
