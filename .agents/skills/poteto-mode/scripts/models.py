#!/usr/bin/env python3
"""Validate and resolve pstack's explicit model-role profiles without a provider SDK."""
from __future__ import annotations
import argparse
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


class ModelError(ValueError):
    pass


def validate(profile: object) -> dict:
    if not isinstance(profile, dict):
        raise ModelError('Profile must be an object')
    if set(profile) - {'version', 'max_parallel', 'confirmed_models', 'roles', 'panels', 'budget'}:
        raise ModelError('Unknown profile field')
    if type(profile.get('version', 1)) is not int or profile.get('version', 1) != 1:
        raise ModelError('Unknown profile version')
    cap = profile.get('max_parallel', 3)
    if type(cap) is not int or not 1 <= cap <= 64:
        raise ModelError('max_parallel must be 1..64')
    observed = profile.get('confirmed_models', [])
    if not isinstance(observed, list) or not all(isinstance(x, str) and x.strip() for x in observed):
        raise ModelError('confirmed_models must contain observed model IDs')
    roles, panels = profile.get('roles', {}), profile.get('panels', {})
    if not isinstance(roles, dict) or set(roles) - set(ROLE_NAMES):
        raise ModelError('Unknown role')
    if not isinstance(panels, dict) or set(panels) - set(PANEL_NAMES):
        raise ModelError('Unknown panel')
    def check(model):
        if not isinstance(model, str) or model not in (*ALIASES, *observed):
            raise ModelError(f'Unconfirmed model: {model!r}')
    for model in roles.values():
        check(model)
    for name, values in panels.items():
        minimum = 2 if name == 'architect runners' else 1
        if not isinstance(values, list) or not minimum <= len(values) <= 16:
            raise ModelError(f'{name} needs {minimum}..16 seats')
        for model in values:
            check(model)
    return dict(profile)


def resolve(profile: object, role: str) -> list[dict]:
    profile = validate(profile)
    if role in ROLE_NAMES:
        choices = [profile.get('roles', {}).get(role, 'inherit-parent')]
    elif role in PANEL_NAMES:
        choices = profile.get('panels', {}).get(role, ['inherit-parent'] * 4)
    else:
        raise ModelError(f'Unknown role: {role}')
    return [{} if model in ALIASES else {'model': model} for model in choices]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('validate', 'resolve'))
    parser.add_argument('profile', type=Path)
    parser.add_argument('--role')
    args = parser.parse_args()
    try:
        profile = validate(json.loads(args.profile.read_text()))
        if args.command == 'resolve':
            if not args.role:
                raise ModelError('--role is required')
            output = {'role': args.role, 'choices': resolve(profile, args.role),
                      'launch': 'Recheck account availability before native task start.',
                      'pool_not_fanout': args.role == 'arena cross-judge pool'}
        else:
            output = {'status': 'valid', 'entitlement_verified': False}
        print(json.dumps(output, indent=2))
        return 0
    except (OSError, ValueError) as exc:
        print(f'pstack models: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
