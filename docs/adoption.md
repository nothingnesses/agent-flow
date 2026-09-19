# Adopt agent-flow into an existing project

This guide covers the unreleased minimal workflow, not the published 0.0.4 crate.

The rehearsal uses runtime source at `d486e747981776eb36c8d13c8217a4d5263dcda4` with this delivery's candidate directory pack. That base predates the adoption prompt. No released version or future commit identifies the complete candidate yet.

Use the [source installation instructions](../README.md#install-the-current-workflow). Record the exact checkout commit and any local changes.

The source still reports 0.0.4, so version output alone is insufficient.

## 1. Establish authority before edits

All project paths and refs below belong to the consuming project, not the agent-flow source checkout.

Read the project's existing instructions and relevant product material:

- Root and nested agent guidance.
- Plans and specifications.
- Current work and its acceptance criteria.
- Check configuration and hooks.
- Local changes and untracked files.

Permission to read guidance grants no authority to execute its commands or hooks.

Ask the human to resolve instruction conflicts before edits. Ask who owns uncertain decisions. Agree how the new workflow joins the existing instructions. Do not silently choose precedence.

Keep legitimate project plans and specifications in that project's VCS.

The agent-flow reset authorises no deletion of another project's plans. Historical checkboxes and broader plans do not establish current agreed work.

Identify only the current work that the human approves for `.agents/work.toml`. If scope exceeds five steps or 4,096 bytes, stop for a smaller agreed scope.

## 2. Inspect the project and proposed assets

Change to the consuming project root:

```sh
cd /path/to/your-project
```

Record the initial state without index refresh:

```sh
GIT_OPTIONAL_LOCKS=0 git status --short --untracked-files=all
git diff --no-ext-diff --no-textconv
git diff --cached --no-ext-diff --no-textconv
```

Preserve unrelated changes and the index. Do not stage or stash work as part of adoption.

Preview the default pack:

```sh
agent-flow scaffold --output-dir . --vcs none --principles default --dry-run
```

The preview labels each destination with its proposed action. It does not establish that existing reference content is disposable.

Inspect every existing destination and its parent directories. If a destination uses a symlink or an unexpected file type, stop for human direction.

The default pack has two ownership classes:

- Working files, `AGENTS.md` and `.agents/work.toml`, remain unchanged when present.
- Reference assets under `.agents/` refresh on every write, including locally edited copies.

Compare reference content before replacement. If local references contain project requirements, ask the human how to preserve them in project-owned files first. Obtain approval for each reference replacement. Do not use `--force`.

Checks and hooks stay outside this default write.

Do not select `--module checks` or `--with-precommit-hook` during adoption.

## 3. Apply the approved scaffold

After the human approves the destinations and instruction integration, apply the scaffold:

```sh
agent-flow scaffold --output-dir . --vcs none --principles default --write
```

`--vcs none` prevents repository initialisation. This command neither stages nor commits the output.

Do not overwrite an existing `AGENTS.md`. Apply only the human-approved integration edit to that file, or to the project's actual instruction entry point.

Two integration approaches are available:

- Add an explicit instruction to read `.agents/AGENTS.reference.md`, after approval of its full content and precedence.
- Merge the approved workflow sections into project-owned guidance, with the existing project rules intact.

A reference link makes future reference refreshes instruction changes too. A manual merge requires later human reconciliation when the workflow changes.

A preserved root file alone does not activate the workflow.

Ask the human to approve the applicable instruction path and any precedence rule. If neither approach preserves project intent, stop.

## 4. Set only agreed current work

The generated work file contains starter text, not approved project work.

If `.agents/work.toml` already exists, preserve it unless the human explicitly approves specific changes. If it is new, replace the starter only with human-approved current work.

Keep broader plans and specifications at their existing project paths. Refer to them from the work prose when necessary. Do not convert legacy plans or copy historical checkboxes into active steps.

This example assumes the human approved only a help-text correction. It grants no authority in your project.

```toml
version = 1
selected_action = "clarify-help"

[[step]]
id = "clarify-help"
status = "active"
blocked_by = []
user_problem = "The help text omits the output directory default."
change = "Document the output directory default in the help text."
acceptance = [
  "The help text names the default output directory.",
  "The existing CLI tests pass.",
]
why_next = "The human selected this correction before further CLI changes."
```

The [state reference](reference.md#bounded-work-state) describes the closed schema and its limits.

## 5. Validate and review

Run the read-only state commands from the consuming project root:

```sh
agent-flow validate --source .agents/work.toml
agent-flow status --source .agents/work.toml
agent-flow status --source .agents/work.toml --json
agent-flow next --source .agents/work.toml
agent-flow next --source .agents/work.toml --json
```

These commands parse and project state. They do not execute the project's checks or hooks. Structural validation proves neither correct interpretation of project intent nor independent review.

Compare the projected action with the human's agreement. If validation fails or the interpretation differs, stop for correction within the approved scope.

Inspect the complete result:

```sh
GIT_OPTIONAL_LOCKS=0 git status --short --untracked-files=all
git diff --no-ext-diff --no-textconv
git diff --cached --no-ext-diff --no-textconv
git ls-files --others --exclude-standard
```

Open every new file listed above, since ordinary `git diff` excludes untracked files. Inspect any new ignored files at the scaffold destinations too. Compare the index and unrelated changes with the initial state.

Request human review of the diff and all new files. Report the source revision alongside commands and results. Report unresolved decisions separately.

Stop here. Do not automatically:

- Start implementation or invoke `kickoff.md`.
- Install or execute hooks.
- Run project check commands.
- Stage or commit files.
- Publish changes.
- Convert or delete legacy plans.

For later refreshes, repeat the destination review before the scaffold write.

Unchanged references produce identical bytes, but edited reference copies are replaced. Working-file preservation and reference refresh are separate behaviours.
