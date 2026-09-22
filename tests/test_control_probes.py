"""Actual terminal and browser behavior; no native Capy execution is claimed."""
import importlib.util
import http.server
import threading
import time
from functools import partial
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
def load(name, path):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
pty_probe=load('pty_probe',ROOT/'.agents/skills/control-cli/scripts/pty_probe.py')
ui=load('browser_probe',ROOT/'.agents/skills/control-ui/scripts/browser_probe.py')
CMD=[sys.executable,str(ROOT/'tests/fixtures/terminal.py')]

class TerminalProbeTests(unittest.TestCase):
    def test_real_prompt_input_and_exit(self):
        out=pty_probe.run(CMD,{'steps':[{'expect':'ready>'},{'send':'help\n'},{'expect':'Commands: help size quit'},{'expect':'ready>'},{'send':'quit\n'}]})
        self.assertEqual(out['exit_code'],0);self.assertEqual(out['status'],'pass');self.assertIn('Commands:',out['transcript'])
    def test_real_resize_changes_reported_dimensions(self):
        out=pty_probe.run(CMD,{'steps':[{'expect':'ready>'},{'resize':[24,80]},{'send':'size\n'},{'expect':'80x24'},{'send':'quit\n'}]})
        self.assertIn('80x24',out['transcript'])
    def test_ctrl_c_reaches_process_and_records_exit(self):
        out=pty_probe.run(CMD,{'steps':[{'expect':'ready>'},{'signal':'INT'},{'expect':'interrupted'}],'exit_code':130})
        self.assertEqual(out['exit_code'],130)
    def test_timeout_cleans_owned_child_and_retains_failure_output(self):
        with tempfile.TemporaryDirectory() as d:
            pidfile=Path(d)/'pid'
            with self.assertRaises(pty_probe.ProbeError) as error:
                pty_probe.run(CMD+[str(pidfile)],{'timeout':5,'steps':[{'expect':'ready>'},{'expect':'never printed'}]})
            pid=int(pidfile.read_text())
            with self.assertRaises(ProcessLookupError):os.kill(pid,0)
            self.assertIn('ready>',error.exception.transcript)
    def test_stale_pattern_does_not_satisfy_second_expect(self):
        with self.assertRaises(pty_probe.ProbeError) as error:
            pty_probe.run(CMD,{'timeout':5,'steps':[{'expect':'ready>'},{'expect':'ready>'}]})
        self.assertEqual(error.exception.transcript.count('ready>'),1)
    def test_early_eof_and_wrong_exit_fail(self):
        for code,steps in [(3,[{'expect':'ready>'},{'send':'quit\n'}]),(0,[{'expect':'ready>'},{'send':'quit\n'},{'expect':'never'}])]:
            with self.subTest(code=code),self.assertRaises(pty_probe.ProbeError):pty_probe.run(CMD,{'steps':steps,'exit_code':code})
    def test_bad_scenario_is_rejected_before_start(self):
        for step in ({'resize':[-1,80]},{'signal':'KILL'},{'expect':''},{'send':'help','expect':'ready'}):
            with self.subTest(step=step),self.assertRaises(pty_probe.ProbeError):pty_probe.run(CMD,{'steps':[step]})
    def test_public_cli_writes_evidence_and_exit_status(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d);(path/'scenario.json').write_text(json.dumps({'steps':[{'expect':'ready>'},{'send':'quit\n'}]}))
            cmd=[sys.executable,str(ROOT/'.agents/skills/control-cli/scripts/pty_probe.py'),'--scenario',str(path/'scenario.json'),'--output',str(path/'out.json'),'--',*CMD]
            out=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
            self.assertEqual(out.returncode,0,out.stderr);self.assertEqual(json.loads((path/'out.json').read_text())['status'],'pass')

@unittest.skipUnless(os.environ.get('PSTACK_BROWSER_TESTS')=='1','optional real Chromium tests; CI enables these explicitly')
class BrowserProbeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.browser=shutil.which('chromium') or shutil.which('google-chrome')
        self.response_delay=0
        fixture=self
        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/app.html' and fixture.response_delay:
                    time.sleep(fixture.response_delay)
                super().do_GET()
        handler=partial(Handler,directory=str(self.root))
        self.server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        def stop_server():
            self.server.shutdown();self.server.server_close();self.thread.join(timeout=2)
        self.addCleanup(stop_server)
        self.url=f'http://127.0.0.1:{self.server.server_port}/app.html'
        self.html='''<!doctype html><title>Local fixture</title><link rel="icon" href="data:,"><main data-app="counter"><button>Increment</button><output data-testid="count">0</output></main><script>let count=0;document.querySelector('main').onclick=e=>{if(e.target.tagName==='BUTTON'){count+=STEP;document.querySelector('output').textContent=count;e.target.outerHTML='<button>Increment</button>'}};</script>'''
        self.scenario={'marker':'[data-app="counter"]','timeout_ms':700,'steps':[
            {'action':'click','role':'button','name':'Increment','expect':{'selector':'output','text':'1'}},
            {'action':'click','role':'button','name':'Increment','expect':{'selector':'output','text':'2'}},
            {'action':'resize','value':[800,600],'expect':{'selector':'output','text':'2'}}]}
    def test_actual_dom_replacement_and_resize_flow_with_screenshots(self):
        app=self.root/'app.html';app.write_text(self.html.replace('STEP','1'))
        out=ui.run(self.scenario,self.url,self.root/'evidence',self.browser)
        self.assertEqual(out['status'],'pass',out)
        self.assertEqual(len(out['screenshots']),6)
        for file in out['screenshots']:self.assertTrue((self.root/'evidence'/file).read_bytes().startswith(b'\x89PNG'))
    def test_same_scenario_fails_on_bug_then_passes_on_fixed_application(self):
        app=self.root/'app.html';app.write_text(self.html.replace('STEP','2'))
        before=ui.run(self.scenario,self.url,self.root/'before',self.browser)
        self.assertEqual(before['status'],'fail');self.assertTrue(before.get('error'))
        app.write_text(self.html.replace('STEP','1'))
        after=ui.run(self.scenario,self.url,self.root/'after',self.browser)
        self.assertEqual(after['status'],'pass',after)
    def test_page_selection_is_not_tab_order_and_ambiguity_fails(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,executable_path=self.browser)
            try:
                context=browser.new_context();wrong=context.new_page();wrong.set_content('<main>wrong</main>')
                right=context.new_page();right.set_content('<main data-app="right">right</main>')
                self.assertIs(ui.select_page(browser,'[data-app="right"]'),right)
                with self.assertRaises(ValueError):ui.select_page(browser,'[data-app="missing"]')
                duplicate=context.new_page();duplicate.set_content('<main data-app="right">duplicate</main>')
                with self.assertRaises(ValueError):ui.select_page(browser,'[data-app="right"]')
            finally:browser.close()
    def test_navigation_budget_is_separate_from_action_deadline(self):
        app=self.root/'app.html';app.write_text(self.html.replace('STEP','1'))
        self.response_delay=1.2
        self.scenario['navigation_timeout_ms']=5000
        result=ui.run(self.scenario,self.url,self.root/'delayed',self.browser)
        self.assertEqual(result['status'],'pass',result)
        self.assertEqual(len(result['screenshots']),6)
    def test_console_error_is_not_a_pass(self):
        app=self.root/'app.html';app.write_text(self.html.replace('STEP','1')+'<script>console.error("fixture failure")</script>')
        result=ui.run(self.scenario,self.url,self.root/'error',self.browser)
        self.assertEqual(result['status'],'fail');self.assertIn('fixture failure',result['console_errors'])

if __name__=='__main__':unittest.main()
