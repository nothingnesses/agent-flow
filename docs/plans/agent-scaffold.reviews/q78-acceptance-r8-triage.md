# Q-78 acceptance pass 8 triage

## Scope and verification

I independently read both pass-8 reports, acceptance triages 1–7, Q-78 and Q-84 through Q-87, the complete current planning product, and the ledger. I reproduced every reported command against this worktree.

- `agent-flow validate --source docs/plans/agent-scaffold.plan.toml`: `474 records, valid`; `114 steps, 87 questions, valid`.
- `agent-flow validate --source docs/plans/agent-scaffold.plan.toml --workflow --workflow-spec .agents/workflow.toml`: `workflow invariants hold`.
- `agent-flow render --check --strict docs/plans/agent-scaffold.plan.toml`: `up to date`.
- `git diff --check`: passed.

The current non-empty question-sidecar selector prints `Q-78.md` and `Q-86.md`. The Q-78 acceptance selector prints seven passes with valid-shortfall sequence `[7,10,5,6,5,5,4]` (records 432–437 and 473). `git ls-files docs/plans/workflow-calibration.explorations/` prints thirteen paths, not three.

## Deduplication and classification

The reports raise three distinct claims, not duplicates:

1. the Q-78 exploration's **current question-sidecar** inventory;
2. the Q-86 brief's date-bounded **local acceptance evidence**; and
3. `workflow-calibration`'s asserted **exploration-directory** inventory.

Only (1) and (3) are current acceptance shortfalls. Finding (2) is inherited historical context, not an assertion of a current exhaustive inventory. No residual risk is accepted.

## Verdicts

### R8-G1 — GPT: valid, `low`

`docs/plans/step-intent-encoding.explorations/Q-78.md:44` says that Decision 26 lives in `Q-78.md` “while the rest remain empty,” then labels `find docs/plans/agent-scaffold.questions -type f -size +0` the current non-empty-set reproduction. That command now prints both `Q-78.md` and `Q-86.md`; the latter is substantive Q-86 detail (`docs/plans/agent-scaffold.questions/Q-86.md:1`). The sentence is therefore a live claim contradicted by its own prescribed selector.

This is `low`: the selector remains correct and no criterion depends on a fixed count, but the Q-78 design record is stale. It is a current documentation-currency shortfall, not a re-raise of the historical observation that sidecars were empty when the pass began.

**Smallest durable disposition:** remove the exhaustive “while the rest remain empty” clause. Retain the command and make its path output the sole authority for the current non-empty set; do not replace one stale one-file inventory with a two-file inventory. Re-render after the source-sidecar change.

### R8-C1 — Claude A: invalid, `low` as reported

The reported selector does reproduce seven passes and `[7,10,5,6,5,5,4]`. It does not, however, contradict the Q-86 brief. The brief explicitly frames six and its six adjudications as the sample **“at this fold”** (`docs/plans/workflow-calibration.explorations/Q-86-convergence-mechanism-brief.md:27-33`) and immediately directs an explorer to derive the *current* count and sequence from the append-only-log selector rather than copying a permanent total. The seventh acceptance record was appended only after this design brief was scheduled, at record 473.

The enumerated triages are the corresponding adjudications for that fixed six-pass local demonstration; they do not say they are the current complete contents of `docs/plans/agent-scaffold.reviews/`. Replacing them with a glob would turn the bounded, reproducible historical sample into a moving and eventually self-referential corpus. A later explorer may read newer adjudications as additional context, but making that optional research mandatory is not an acceptance correction.

### R8-C2 — Claude B: valid, `low`

`docs/plans/agent-scaffold.steps/workflow-calibration.md:9` says the directory “currently holds” exactly three named files. `git ls-files docs/plans/workflow-calibration.explorations/` reproduces thirteen tracked files, including the Q-86 brief. The assertion is consequently false as a current inventory. Most omitted paths predate this acceptance product, but the current Q-85/Q-86 fold added another file to the same directory while leaving the exhaustive wording live; acceptance's documentation-currency check therefore reaches it.

The narrower proposed consequence does not reproduce. `2026-08-14-causation-investigation.md` answers the distinct Q-76 question of why the loop turned (`docs/plans/workflow-calibration.explorations/2026-08-14-causation-investigation.md:1`), and its receipt is owned by `workflow-audit-followups`, not `workflow-calibration`. The Q-86 brief's existing-calibration-work section is a deliberately scoped reading list for sequential/survival and severity-trajectory analysis (`Q-86-convergence-mechanism-brief.md:35-39`). No evidence establishes that the causation record is required input to the bounded-mechanism design. Adding it is optional scope, not part of this valid disposition.

**Smallest durable disposition:** replace “The directory currently holds” and its exhaustive three-file list with a non-exhaustive description: identify those three as the audit's core records if their descriptions remain useful, then refer to the directory as also carrying related calibration and design records. Do not state a file count or enumerate all current files, and do not add a new mandatory Q-86 reading obligation. Re-render after the source-sidecar change.

## Result

Two distinct `low` acceptance shortfalls are valid: the Q-78 exploration's stale current question-sidecar assertion and `workflow-calibration`'s stale current directory inventory. Claude A is invalid because it treats a bounded historical evidence sample as a live exhaustive inventory. No high or critical finding was dismissed, so no independent dismissal re-check is owed.
