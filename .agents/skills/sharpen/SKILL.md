---
name: sharpen
description: "Make a task deeper, not bigger, then rewrite the prompt. Use only for /sharpen."
---

# Sharpen

The user wants a deeper version of this task, not a bigger one. Before rewriting it, do four things:

1. Say what a top professional in this field would do here that the user is not asking for.
2. Name the rawest material they would start from instead of what has already been digested.
3. Name the specific methods and tools they would use.
4. Say what, other than you or the user, would show the result is right. Keep this independent check.

Then rewrite the user's prompt to ask for exactly that. Return only the rewrite and do not do the task.

Leave choices that are the user's to make open instead of deciding them. Relax incidental constraints only within the user's authorization. Preserve explicit scope, permissions, model preferences, and choices only the user can make.
