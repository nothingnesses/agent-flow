# Adopt into this project

Help me adopt the minimal agent-flow workflow without implementation.

Project root: <consuming-project path>.
Current agreed work: <human-approved scope, or ask me>.
Source installation: <agent-flow checkout commit and local changes>.

## Before edits

Resolve all project paths and refs in the consuming project, not the agent-flow repository.
Read existing project instructions and relevant product material:

- Root and nested guidance.
- Plans and specifications.
- Existing bounded work.
- Checks and hooks.
- Tracked and untracked changes.

Permission to read guidance grants no authority to execute its commands or hooks.

Record the initial status with `GIT_OPTIONAL_LOCKS=0 git status --short --untracked-files=all`.
Inspect both unstaged and staged diffs without external diff drivers or text conversion.
Preserve unrelated work and the index.

If authority or instructions conflict, stop and ask me before edits.
Present the options and trade-offs with a recommendation.
Do not silently choose precedence.
Agree how approved workflow guidance joins existing project instructions.
Do not overwrite an existing `AGENTS.md`.

A preserved root file does not automatically include new workflow instructions.

Propose an explicit reference inclusion or a merge of approved sections into project-owned guidance.
Ask me to approve the instruction path and precedence before that integration edit.

Keep legitimate plans and specifications in this project's VCS.

The agent-flow reset is not permission to delete this project's plans.

Distinguish agreed current work from broader plans and historical checkboxes.
Import only agreed current work into `.agents/work.toml`.
If existing work needs changes, ask me to approve those changes first.

The pack's work file is starter text, not approved work.

## Approved adoption only

Use the unreleased source workflow, not the published 0.0.4 crate.

Version output alone cannot identify it because current source also reports 0.0.4.

Confirm the checkout includes this prompt.

From the project root, preview:

```sh
agent-flow scaffold --output-dir . --vcs none --principles default --dry-run
```

Inspect existing destinations and their parent directories.
If a destination uses a symlink or an unexpected file type, stop and ask me.

Working files remain when present, but reference assets refresh on every write.
The dry-run list does not establish that reference content is disposable.

Ask me to approve replacements after preservation of project-specific reference content in project-owned files.
After approval, apply:

```sh
agent-flow scaffold --output-dir . --vcs none --principles default --write
```

Apply only the agreed instruction integration and work-file edits.
Keep the work file within 4,096 bytes and five total steps.
Use only these statuses:

- `active`.
- `pending`.
- `complete`.

Do not use `--force`.
Do not install hooks or run project checks.
Do not automatically:

- Start implementation.
- Stage files.
- Commit.
- Publish.

Do not convert legacy plans or create workflow records.

## Validate and return

Run these read-only commands:

```sh
agent-flow validate --source .agents/work.toml
agent-flow status --source .agents/work.toml
agent-flow status --source .agents/work.toml --json
agent-flow next --source .agents/work.toml
agent-flow next --source .agents/work.toml --json
```

Compare the projected action with my agreement.

Structural validation does not prove correct interpretation of intent or independent review.

If validation fails or intent differs, stop and report it.
Inspect the final status and both diffs.
Open all new files, including untracked or ignored scaffold output absent from ordinary diffs.
Confirm unrelated work and the index remain unchanged.

Return changed paths with exact commands and results.
Request my review of the complete diff and new files, then stop.
