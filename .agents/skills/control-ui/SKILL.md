---
name: control-ui
description: Drive and verify the actual application with Capy browser and desktop tools.
---

# Control a UI

Read the project verify-* skill. Start the real application with the configured setup and
startup commands, then health-check it. Use Capy's available browser/desktop tools to
exercise the user-visible path, not a screenshot of source code. For a bug, capture the
same surface failing first. Record viewport, route, user state, interactions, expected
visible result, console/network failures, and screenshots or recordings without secrets.
Run the fixed flow and at least one neighboring regression. Doctor or reset after a
surprising result before another drive. Serialize control of a shared UI instance; isolate
writers and independent candidate apps on fresh machines. Transfer evidence with
transfer_files and verify its presence before cleaning up owned processes. Native previews
sleep with the machine; startup must restart services. Do not expose a port or publish
private screenshots without authorization. Missing access is an explicit blocked gate.
