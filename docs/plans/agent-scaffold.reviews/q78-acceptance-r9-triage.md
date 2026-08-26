# Q-78 acceptance pass 9 triage

## Scope and reproduction

I independently read the two pass-9 reports, acceptance triages 1–8, the Q-78 plan product and Success Criteria, the relevant questions and explorations, and the ledger. GPT reported zero shortfalls; Claude raised the three findings adjudicated below.

Using an `agent-flow` binary built from this worktree with its target directory under the authorised `TMPDIR` scratch mount, I reproduced:

- `agent-flow validate --source docs/plans/agent-scaffold.plan.toml`: `475 records, valid`; `114 steps, 87 questions, valid`.
- `agent-flow validate --source docs/plans/agent-scaffold.plan.toml --workflow --workflow-spec .agents/workflow.toml`: `workflow invariants hold`.
- `agent-flow render --check --strict docs/plans/agent-scaffold.plan.toml`: `up to date`.
- `git diff --check` and `git diff --check main...HEAD`: passed.

All scratch probes stayed below the authorised `TMPDIR`; `agent-flow checks` was not run. The worktree was clean before this triage and before this file was written.

## Verdicts

### A — question-sidecar universals: valid, `low`

The finding reproduces. `find docs/plans/agent-scaffold.questions -type f -size +0c` reports `Q-78.md` (1295 bytes) and `Q-86.md` (510 bytes). The unqualified current universals remain at `docs/plans/agent-scaffold.steps/plan-order-array-position.md:432` and `docs/plans/umbrella-membership.explorations/Q-79.md:89`, and render at `docs/plans/agent-scaffold.md:3415` and `:4689` respectively. The generated plan also states at `:5061` that the non-empty Q-78 sidecar supersedes the question ask's historical empty-sidecar observation.

These are not frozen-history statements: the Q-79 document presents its figures as measured on the branch, and the plan-order sentence explains a live `render` contract. The latter must not be confused with the historical Q-78 ask at `agent-scaffold.plan.toml:2404`, which Q-78.md expressly labels superseded. The universal claims are branch-authored (`git log -S 'every question sidecar is 0 bytes'` reaches the Q-78 pass commit) and are false today. They do not invalidate the actual missing-sidecar rule or either design conclusion, so `low` is the correct severity.

**Smallest safe disposition:** at both live sites, retain the existence-contract reasoning but replace the universal with a non-exhaustive form: question sidecars must exist and most are empty. Use `find docs/plans/agent-scaffold.questions -type f -size +0` as the sole current authority for the non-empty set; do not write a count or enumerate the two paths. Re-render after changing the Step Detail source.

### B — five-step audit completeness: invalid, `low` as reported

The reported measurements reproduce: nine later sidecars match `Both validation modes`, and none contains `questions, valid`. The safety control also reproduces independently: in an authorised empty directory, `validate --source docs/plans/TEMPLATE.plan.toml --workflow` exits 1 with `--workflow requested but no plan source resolved`.

They do not contradict the cited claim. `validate-missing-source-exit.md:25-27` names the five exact steps that formed the original Q-78 audit and records the fifth step's accepted residual and the separate `--workflow` protection. The authoritative Q-78 narrative likewise distinguishes “THE ORIGINAL DESIGN PASS AUTHORED FOUR STEPS” plus the pre-existing fifth step from the focused successors subsequently authored by the first and second acceptance repairs (`docs/plans/agent-scaffold.plan.toml:2433`). It explicitly says those successors “do not change the original five steps.” The nine later steps are therefore not an omitted part of the enumerated five-step audit; treating them as such would turn a bounded historical explanation into an open-ended branch inventory.

No change is warranted. Do not add stdout pins to the nine later criteria, replace the bounded paragraph with a moving selector, or state a newer total.

### C — `CHANGELOG.md` Unreleased pointer: invalid, `low` as reported

The factual premise reproduces: `CHANGELOG.md` has no `Unreleased` heading and currently starts with `## [0.0.4] - 2026-08-18`; the pointer at `docs/plans/agent-scaffold.steps/workflow-calibration.md:3` is stale. The plan also correctly records the absent section at `plan-order-array-position.md:417` and `step-intent-encoding.md:1065`.

This is inherited repository staleness, not a Q-78 acceptance shortfall. `git show main:docs/plans/agent-scaffold.steps/workflow-calibration.md` contains the identical pointer, and its introduction commit `0fadd90f` is an ancestor of `main`. The Q-78 product's diff at this source removes the stale status-opening token and updates the step's calibration/design-pass context, but it neither introduces nor changes the pointer. Success Criterion 41 requires the Q-85 receipt, the Q-86 exploration state, and the tracked design brief; all three reproduce without relying on this historical changelog cross-reference.

The new accurate absence observations do not convert an inherited defect into branch-authored scope. The acceptance documentation-currency rule reaches docs made stale by the shipped change; otherwise every unrelated pre-existing stale reference exposed by a new accurate observation would silently expand Q-78. No change is warranted in this acceptance repair. A separately scoped documentation-maintenance task may later repoint or remove the inherited link, but it is not an accepted residual and must not be folded into Q-78 on this evidence.

## Result

One distinct acceptance shortfall is valid: A at `low` severity. B and C are invalid. No high or critical finding was dismissed, so no independent dismissal re-check is owed.
