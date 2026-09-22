#!/usr/bin/env python3
"""Optional real-browser probe; requires installed Python Playwright, never installs it."""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def select_page(browser, marker: str, exclude: str | None = None):
    matches = [page for context in browser.contexts for page in context.pages
               if page.locator(marker).count() and not (exclude and page.locator(exclude).count())]
    if len(matches) != 1:
        pages = [{'title': p.title(), 'url': p.url.split('?')[0].split('#')[0]}
                 for c in browser.contexts for p in c.pages]
        raise ValueError(f'Expected one matching app page, found {len(matches)}: {pages}')
    return matches[0]


def run(scenario: dict, url: str, output: Path, executable: str | None = None,
        cdp: str | None = None) -> dict:
    from playwright.sync_api import sync_playwright, expect
    if not isinstance(scenario, dict) or not isinstance(scenario.get('marker'), str) or not scenario['marker']:
        raise ValueError('Need a stable app marker')
    steps = scenario.get('steps')
    if not isinstance(steps, list) or not 1 <= len(steps) <= 128:
        raise ValueError('Need 1..128 interaction steps')
    for field in ('timeout_ms', 'navigation_timeout_ms'):
        value = scenario.get(field, 5000 if field == 'timeout_ms' else 30000)
        if type(value) is not int or not 1 <= value <= 120000:
            raise ValueError(f'{field} must be an integer in 1..120000')
    output.mkdir(parents=True, exist_ok=True)
    report = {'status': 'fail', 'screenshots': [], 'console_errors': [], 'network_failures': [],
              'native_capy_verified': False}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(cdp) if cdp else p.chromium.launch(executable_path=executable, headless=True)
        try:
            if cdp:
                page = select_page(browser, scenario['marker'], scenario.get('exclude_marker'))
            else:
                size = scenario.get('viewport', [1280, 800])
                page = browser.new_page(viewport={'width': size[0], 'height': size[1]})
            page.set_default_timeout(scenario.get('timeout_ms', 5000))
            page.set_default_navigation_timeout(scenario.get('navigation_timeout_ms', 30000))
            expect.set_options(timeout=scenario.get('timeout_ms', 5000))
            page.on('pageerror', lambda error: report['console_errors'].append(str(error)))
            page.on('console', lambda msg: report['console_errors'].append(msg.text) if msg.type == 'error' else None)
            page.on('requestfailed', lambda req: report['network_failures'].append(req.failure))
            page.on('response', lambda response: report['network_failures'].append(f'HTTP {response.status}') if response.status >= 400 else None)
            if not cdp:
                page.goto(url)
            expect(page.locator(scenario['marker'])).to_be_visible()
            select_page(browser, scenario['marker'], scenario.get('exclude_marker'))
            for index, step in enumerate(steps):
                if not isinstance(step, dict) or not isinstance(step.get('expect'), dict):
                    raise ValueError('Each action needs an explicit visible expectation')
                before = output / f'{index:03}-before.png'
                page.screenshot(path=str(before), full_page=True)
                report['screenshots'].append(before.name)
                action = step['action']
                if action in ('click', 'fill', 'press', 'drag'):
                    target = page.get_by_role(step['role'], name=step['name'], exact=True)
                    expect(target).to_have_count(1)
                    if action == 'click': target.click()
                    elif action == 'fill': target.fill(step['value'])
                    elif action == 'press': target.press(step['value'])
                    else:
                        destination = page.get_by_role(step['target_role'], name=step['target_name'], exact=True)
                        expect(destination).to_have_count(1)
                        target.drag_to(destination)
                elif action == 'resize':
                    page.set_viewport_size({'width':step['value'][0], 'height':step['value'][1]})
                elif action == 'scroll': page.mouse.wheel(*step['value'])
                elif action == 'navigate': page.goto(step['value'])
                else: raise ValueError(f'Unsupported browser action: {action}')
                expected = step['expect']
                observed = page.locator(expected['selector'])
                expect(observed).to_be_visible()
                expect(observed).to_have_text(expected['text'])
                after = output / f'{index:03}-after.png'
                page.screenshot(path=str(after), full_page=True)
                report['screenshots'].append(after.name)
            if report['console_errors'] or report['network_failures']:
                raise ValueError('Browser errors require investigation, not a passing report')
            report['status'] = 'pass'
        except Exception as exc:
            report['error'] = str(exc)
        finally:
            if not cdp:
                browser.close()
            # Exiting Playwright disconnects an attached browser; never close its owner.
    (output/'result.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True)
    parser.add_argument('--scenario', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--executable')
    parser.add_argument('--cdp')
    args = parser.parse_args()
    report = run(json.loads(args.scenario.read_text()), args.url, args.output, args.executable, args.cdp)
    print(json.dumps(report, indent=2))
    return 0 if report['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
