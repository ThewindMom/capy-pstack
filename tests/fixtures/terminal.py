"""Disposable real-PTY app for control-cli regression tests."""
import os
from pathlib import Path
import signal
import sys
if len(sys.argv) > 1:
    Path(sys.argv[1]).write_text(str(os.getpid()))
def interrupt(_signum, _frame):
    print('interrupted', flush=True)
    raise SystemExit(130)
signal.signal(signal.SIGINT, interrupt)
while True:
    print('ready>', flush=True)
    line = sys.stdin.readline()
    if not line or line.strip() == 'quit':
        break
    if line.strip() == 'help': print('Commands: help size quit', flush=True)
    elif line.strip() == 'size':
        columns, rows = os.get_terminal_size(0)
        print(f'{columns}x{rows}', flush=True)
    else: print('unknown', flush=True)
