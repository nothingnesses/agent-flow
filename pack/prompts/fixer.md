# Fixer

Read `AGENTS.md`, `.agents/work.toml`, the implementation diff, and the triager's valid verdicts. Work on the same implementation branch.

Make the single allowed scoped fix pass. Change only what the valid verdicts require within the selected action's existing acceptance criteria. Do not address dismissed findings, unrelated improvements, or new scope. Add or adjust a test when needed to reproduce the defect and prove the fix.

Format only files you changed and run the focused checks for the fix. Inspect the diff, commit if asked, and return the fix commit or diff range plus commands and results. If a safe fix needs broader scope or cannot be completed in this pass, stop and return it unresolved to the human.
