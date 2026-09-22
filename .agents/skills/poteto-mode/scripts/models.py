#!/usr/bin/env python3
"""Resolve pstack model policy. Output is a work order, never an invented Capy API payload."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys

ROLE_NAMES = ('feature', 'refactoring', 'bug-fix', 'perf-issue', 'hillclimb',
              'judgment and prose', 'hardest tasks', 'how explorer', 'how explainer',
              'why investigators', 'why synthesizer', 'reflect tooling',
              'reflect judgment', 'reflect divergent', 'reflect synthesizer',
              'swarm workers', 'comment review')
PANEL_NAMES = ('arena runners', 'arena cross-judge pool', 'architect runners', 'interrogate reviewers')
ALIASES = ('inherit-parent', 'auto')
PRESETS = Path(__file__).resolve().parents[3] / 'pstack.model-presets.json'


class ModelError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ModelError(message)


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def catalog() -> dict:
    return json.loads(PRESETS.read_text())


def identity(model: str) -> str:
    # Billing routes are not independent weights. Only documented aliases are collapsed.
    return catalog()['identities'].get(model, model)


def family(model: str) -> str:
    return identity(model).split('/', 1)[0]


def choice(value: object) -> dict:
    if isinstance(value, str):
        value = {'model': value}
    require(isinstance(value, dict) and not set(value) - {'model', 'reasoning_effort', 'fast'},
            'A choice needs model and optional reasoning_effort/fast')
    require(nonempty(value.get('model')), 'Missing model')
    if 'reasoning_effort' in value:
        require(nonempty(value['reasoning_effort']), 'reasoning_effort must be a nonempty string')
    if 'fast' in value:
        require(type(value['fast']) is bool, 'fast must be boolean')
    require(value['model'] not in ALIASES or set(value) == {'model'},
            'Inheritance means all parent settings; do not attach effort or fast overrides')
    return dict(value)


def validate(profile: object) -> dict:
    require(isinstance(profile, dict), 'Profile must be an object')
    require(not set(profile) - {'version', 'preset', 'budget', 'max_parallel', 'roles', 'panels',
                                'approved_difference'}, 'Unknown profile field; migrate v1 confirmed_models to --observed')
    require(type(profile.get('version', 2)) is int and profile.get('version', 2) == 2,
            'Profile version must be 2; v1 inheritance is not silently upgraded')
    preset = profile.get('preset', 'upstream-faithful')
    require(preset in ('upstream-faithful', 'single-model', 'custom'), 'Unknown preset')
    require(profile.get('budget', 'unlimited') in ('unlimited', 'large', 'medium', 'small'), 'Unknown budget')
    cap = profile.get('max_parallel', 3)
    require(type(cap) is int and 1 <= cap <= 64, 'max_parallel must be 1..64')
    roles, panels = profile.get('roles', {}), profile.get('panels', {})
    require(isinstance(roles, dict) and not set(roles) - set(ROLE_NAMES), 'Unknown role')
    require(isinstance(panels, dict) and not set(panels) - set(PANEL_NAMES), 'Unknown panel')
    for value in roles.values():
        choice(value)
    for name, values in panels.items():
        minimum = 2 if name == 'architect runners' else 1
        require(isinstance(values, list) and minimum <= len(values) <= 16, f'{name} needs {minimum}..16 seats')
        for value in values:
            choice(value)
    require('approved_difference' not in profile or nonempty(profile['approved_difference']), 'Empty approval reference')
    if preset != 'upstream-faithful':
        require(nonempty(profile.get('approved_difference')),
                'single-model/custom requires the actual user approval reference; do not manufacture it')
    return copy.deepcopy(profile)


def merge_profiles(base: object, override: object) -> dict:
    base, override = validate(base), validate(override)
    merged = dict(base, **override)
    for key in ('roles', 'panels'):
        merged[key] = dict(base.get(key, {}), **override.get(key, {}))
    return validate(merged)


def requested(profile: object, role: str) -> list[dict]:
    profile = validate(profile)
    require(role in (*ROLE_NAMES, *PANEL_NAMES), f'Unknown role: {role}')
    config = catalog()
    group = 'roles' if role in ROLE_NAMES else 'panels'
    defaults = config[group][role]
    defaults = [defaults] if group == 'roles' else defaults
    preset = profile.get('preset', 'upstream-faithful')
    values = [{'model': 'inherit-parent'}] * len(defaults) if preset == 'single-model' else defaults
    if role in profile.get(group, {}):
        override = profile[group][role]
        values = [override] if group == 'roles' else override
    values = [choice(v) for v in values]
    if preset == 'upstream-faithful':
        require(len(values) == len(defaults), f'{role}: faithful seat count changed; select an approved custom profile')
        for selected, original in zip(values, defaults):
            require(identity(selected['model']) == identity(original['model']),
                    f'{role}: faithful identity changed; select an approved custom profile')
            # A subscription route to the same weights is fine; dropped effort/priority is not.
            require({k:v for k,v in selected.items() if k != 'model'} ==
                    {k:v for k,v in original.items() if k != 'model'},
                    f'{role}: faithful settings changed; use the budget field or approved custom profile')
    budget = profile.get('budget', 'unlimited')
    if budget != 'unlimited':
        target = {'large':'xhigh', 'medium':'high', 'small':'medium'}[budget]
        for selected in values:
            if selected['model'] not in ALIASES:
                selected['reasoning_effort'] = target
    return values


def observations(value: object) -> dict:
    require(isinstance(value, dict) and nonempty(value.get('source')),
            '--observed needs a source reference to current account/tool observations')
    require(isinstance(value.get('models'), dict), 'Observed models must be an object keyed by exact route ID')
    for model, capabilities in value['models'].items():
        require(nonempty(model) and model not in ALIASES, 'Observation needs an actual model ID')
        require(isinstance(capabilities, dict), f'Invalid capabilities for {model}')
        efforts = capabilities.get('reasoning_efforts', [])
        require(isinstance(efforts, list) and all(nonempty(x) for x in efforts), 'Invalid effort choices')
        require(type(capabilities.get('fast', False)) is bool, 'Invalid fast capability')
    if 'parent' in value:
        parent = choice(value['parent'])
        require(parent['model'] not in ALIASES and parent['model'] in value['models'], 'Observe the actual parent model')
    return value


def resolve(profile: object, role: str, observed: object = None) -> list[dict]:
    values = requested(profile, role)
    observed = observations(observed)
    result = []
    for selected in values:
        if selected['model'] in ALIASES:
            require('parent' in observed, 'Inheritance requires the observed parent settings')
            selected = choice(observed['parent'])
        model = selected['model']
        require(model in observed['models'], f'Model unavailable in current observation: {model}')
        capabilities = observed['models'][model]
        if 'reasoning_effort' in selected:
            require(selected['reasoning_effort'] in capabilities.get('reasoning_efforts', []),
                    f'Unsupported reasoning effort for {model}: {selected["reasoning_effort"]}; no silent downgrade')
        if selected.get('fast'):
            require(capabilities.get('fast') is True, f'Priority/fast unavailable for {model}; no silent downgrade')
        result.append(dict(selected))
    if validate(profile).get('preset', 'upstream-faithful') == 'upstream-faithful' and role in PANEL_NAMES:
        require(len({identity(x['model']) for x in result}) == 4, 'Faithful panels require four distinct models')
    return result


def work_order(profile: object, role: str, observed: object) -> dict:
    profile = validate(profile)
    values = resolve(profile, role, observed)
    cap = profile.get('max_parallel', 3)
    return {'role': role, 'preset': profile.get('preset', 'upstream-faithful'),
            'budget': profile.get('budget', 'unlimited'), 'choices': values,
            'distinct_models': len({identity(x['model']) for x in values}),
            'families': sorted({family(x['model']) for x in values}),
            'waves': [list(range(i, min(i+cap, len(values)))) for i in range(0, len(values), cap)],
            'pool_not_fanout': role == 'arena cross-judge pool',
            'source': observations(observed)['source'], 'native_execution_verified': False,
            'dispatch': 'Translate each model/effort/fast setting to the actual native task tool schema. '
                        'If a field cannot be set or verified, block. This is not an API payload.'}


def check_run(order: object, records: object) -> dict:
    require(isinstance(order, dict) and isinstance(order.get('choices'), list) and bool(order['choices']), 'Invalid work order')
    require(order.get('pool_not_fanout') is not True, 'A judge pool must be selected, never launched as a panel')
    require(isinstance(records, list) and len(records) == len(order['choices']), 'Missing or unexpected seat records')
    seats, ids = set(), set()
    for record in records:
        require(isinstance(record, dict), 'Record must be an object')
        seat = record.get('seat')
        require(type(seat) is int and 0 <= seat < len(records) and seat not in seats, 'Invalid or duplicate seat')
        seats.add(seat)
        task_id = record.get('native_task_id')
        require(nonempty(task_id) and task_id not in ids, 'Distinct native task IDs required')
        require(task_id not in order.get('after_task_ids', []), 'Judge must be independent of candidates')
        ids.add(task_id)
        require(record.get('status') == 'done', 'Live, idle, failed or stopped tasks are not completed evidence')
        require(record.get('accepted') is True and nonempty(record.get('artifact')), 'Inspect and accept each actual artifact first')
        expected = choice(order['choices'][seat])
        actual = choice(record.get('settings'))
        require(actual == expected, f'Seat {seat} ran different settings or omitted an observed field')
    return {'status': 'records-match-work-order', 'native_execution_verified': False,
            'limitation': 'Records are assertions. Verify their IDs, settings, timestamps and artifacts in Capy.'}


def select_judge(profile: object, observed: object, candidates: object, records: object) -> dict:
    require(isinstance(candidates, dict) and candidates.get('role') == 'arena runners', 'Expected arena candidate order')
    require(candidates.get('choices') == resolve(profile, 'arena runners', observed), 'Candidate order differs from active policy')
    check_run(candidates, records)
    pool = resolve(profile, 'arena cross-judge pool', observed)
    obs = observations(observed)
    require('parent' in obs, 'Observe the parent model before choosing a cross-judge')
    selected = next((x for x in pool if family(x['model']) != family(obs['parent']['model'])), pool[0])
    return {'role': 'arena judge', 'choices': [selected], 'pool_not_fanout': False,
            'after_task_ids': [r['native_task_id'] for r in records],
            'different_parent_family': family(selected['model']) != family(obs['parent']['model']),
            'native_execution_verified': False,
            'dispatch': 'Transfer the accepted artifacts first, then start exactly one independent read-only native judge.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('validate', 'requested', 'resolve', 'select-judge', 'check-run'))
    parser.add_argument('profile', type=Path, help='Profile JSON; for check-run, the resolved work-order JSON')
    parser.add_argument('--role')
    parser.add_argument('--base-profile', type=Path, help='Lower-precedence bundle policy')
    parser.add_argument('--observed', type=Path)
    parser.add_argument('--candidates', type=Path)
    parser.add_argument('--records', type=Path)
    args = parser.parse_args()
    def load(path):
        require(path is not None, 'Missing required input path')
        return json.loads(path.read_text())
    try:
        profile = load(args.profile)
        if args.base_profile and args.command != 'check-run':
            profile = merge_profiles(load(args.base_profile), profile)
        if args.command == 'check-run':
            output = check_run(profile, load(args.records))
        elif args.command == 'validate':
            validate(profile)
            for role in (*ROLE_NAMES, *PANEL_NAMES):
                requested(profile, role)
            output = {'status': 'valid-policy', 'entitlement_verified': False}
        elif args.command == 'requested':
            output = {'role': args.role, 'choices': requested(profile, args.role), 'launch_ready': False}
        elif args.command == 'select-judge':
            output = select_judge(profile, load(args.observed), load(args.candidates), load(args.records))
        else:
            output = work_order(profile, args.role, load(args.observed))
        print(json.dumps(output, indent=2))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f'pstack models: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
