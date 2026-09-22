#!/usr/bin/env python3
"""Run an owned CLI under a real POSIX PTY; JSON steps use expect, send, resize or signal."""
from __future__ import annotations
import argparse
import errno
import fcntl
import json
import os
from pathlib import Path
import pty
import select
import signal
import struct
import subprocess
import sys
import termios
import time


class ProbeError(RuntimeError):
    pass


def run(command: list[str], scenario: dict) -> dict:
    if not command or not isinstance(scenario, dict):
        raise ProbeError('Need executable argv and a scenario object')
    timeout = scenario.get('timeout', 5)
    if type(timeout) not in (int, float) or not 0 < timeout <= 120:
        raise ProbeError('timeout must be positive and at most 120 seconds')
    steps = scenario.get('steps')
    if not isinstance(steps, list) or not steps or len(steps) > 128:
        raise ProbeError('Need 1..128 steps')
    for step in steps:
        if not isinstance(step, dict) or len(step) != 1:
            raise ProbeError('Each step must contain exactly one action')
        key, value = next(iter(step.items()))
        if key in ('send', 'expect'):
            if not isinstance(value, str) or (key == 'expect' and not value):
                raise ProbeError('send/expect must be strings; expect must not be empty')
        elif key == 'resize':
            if not isinstance(value, list) or len(value) != 2 or any(type(x) is not int or not 1 <= x <= 1000 for x in value):
                raise ProbeError('resize is [rows, columns], each 1..1000')
        elif key != 'signal' or value not in ('INT', 'TERM'):
            raise ProbeError(f'Unsupported action: {key}')
    expected_exit = scenario.get('exit_code', 0)
    if type(expected_exit) is not int:
        raise ProbeError('exit_code must be an integer')
    fd, slave = pty.openpty()
    bootstrap = ('import fcntl,termios,os,sys; '
                 'fcntl.ioctl(0,termios.TIOCSCTTY,0); '
                 'os.execvp(sys.argv[1],sys.argv[1:])')
    try:
        proc = subprocess.Popen([sys.executable, '-c', bootstrap, *command],
                                stdin=slave, stdout=slave, stderr=slave,
                                start_new_session=True, close_fds=True)
    except BaseException:
        os.close(fd)
        raise
    finally:
        os.close(slave)
    pid = proc.pid
    buffer = bytearray()
    position = 0
    status = None
    eof = False
    actions = []
    def read_until(deadline):
        nonlocal eof
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise ProbeError('Deadline exceeded')
        ready, _, _ = select.select([fd], [], [], min(remaining, 0.1))
        if not ready:
            return
        try:
            chunk = os.read(fd, 4096)
        except OSError as exc:
            if exc.errno != errno.EIO:
                raise
            chunk = b''
        if not chunk:
            eof = True
        buffer.extend(chunk)
        if len(buffer) > 2_000_000:
            raise ProbeError('Terminal output exceeds 2 MB')
    try:
        for step in steps:
            action, value = next(iter(step.items()))
            deadline = time.monotonic() + timeout
            if action == 'expect':
                needle = value.encode()
                while (found := buffer.find(needle, position)) < 0:
                    if eof:
                        raise ProbeError(f'EOF before expected pattern: {value!r}')
                    read_until(deadline)
                position = found + len(needle)
            elif action == 'send':
                data = value.encode()
                while data:
                    if time.monotonic() >= deadline:
                        raise ProbeError('Write deadline exceeded')
                    _, writable, _ = select.select([], [fd], [], min(timeout, 0.1))
                    if writable:
                        data = data[os.write(fd, data[:1024]):]
            elif action == 'resize':
                fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack('HHHH', *value, 0, 0))
            else:
                os.killpg(pid, getattr(signal, 'SIG' + value))
            actions.append(step)
        deadline = time.monotonic() + timeout
        while status is None:
            status = proc.poll()
            if status is not None:
                break
            if eof:
                if time.monotonic() >= deadline:
                    raise ProbeError('Process did not exit after terminal EOF')
                select.select([], [], [], 0.01)
            else:
                read_until(deadline)
        code = status
        if code != expected_exit:
            raise ProbeError(f'Exit {code}, expected {expected_exit}')
        return {'status': 'pass', 'exit_code': code, 'steps': actions,
                'transcript': buffer.decode(errors='replace'), 'native_capy_verified': False}
    except ProbeError as exc:
        exc.transcript = buffer.decode(errors='replace')
        raise
    finally:
        if status is None:
            try:
                os.killpg(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                proc.wait(timeout=0.5)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait(timeout=2)
        os.close(fd)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    try:
        result = run(command, json.loads(args.scenario.read_text()))
    except (ProbeError, OSError, ValueError) as exc:
        result = {'status': 'fail', 'error': str(exc), 'transcript': getattr(exc, 'transcript', ''), 'native_capy_verified': False}
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))
    return 0 if result['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
