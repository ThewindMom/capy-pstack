# capy-pstack

This repository contains complete native Capy skills in `.agents/skills/`, with role
prompts, automation workflows and supporting scripts. No submodule or runtime upstream
loader belongs here. Keep native task/PR/automation mechanics in the actual workflows.

Run `python3 -m unittest discover -s tests -v` and `python3 tools/catalog.py --check`.
After an intentional bundled-file edit, review it and run `python3 tools/catalog.py`.
Optional Bun tools live in `.agents/skills/poteto-mode/scripts`; run their tests/typecheck
when changed. Keep all source destinations in `provenance/source.json` accounted for.
Do not claim live Capy integration based only on local or CI tests.
