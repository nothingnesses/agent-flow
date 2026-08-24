# Q-78 post-escalation round 1 GPT review brief

Act only as an independent reviewer in your assigned isolated worktree. Do not edit the reviewed product.

## Target

Review `plan/q78-design-pass` after commit `7120d94`, excluding review briefs from the product.

Read `AGENTS.md`, the ledger from `RESUME HERE`, `q78-reset-r4-triage.md`, `q78-reset-r4-fix-brief.md`, and the current `step-intent-encoding` sidecar. Do not read another post-escalation round 1 reviewer file.

## Loops

Review only:

- `step-intent-encoding-inc1`.
- `step-intent-encoding-inc3`.

Both counters reset after the human foreclosure decision. Both enter round 1 at streak zero, remain `risky`, and need two consecutive clean rounds.

Every other Q-78 loop converged. Do not assign findings to it.

## Settled boundaries

Verify I8 through I12 independently. Do not assume that the repair is correct.

Do not re-open I2, I6, I7, D7, T7a through T7f, `GPT-R2-5`, `GPT-R3-2`, `GB-4`, `GB-9`, `F2` or `F3` without evidence that changes class, severity or measured scope.

The human authorised no waiver.

## Lens

Use ground-blind falsification. For each criterion, build the smallest wrong implementation that can pass while violating its rule, risk ground or cited Principle.

Focus on:

- Both fields, every value row and every human or JSON surface.
- The complete render fragment from byte zero.
- Empty Markdown bodies with intent.
- Review and non-review `next` states.
- Increment-3 retention of increment-1 tests and expectations.
- Fresh-scaffold TOML projections after the required flip.
- Exact future changed paths and documentation impact.

Classify findings exactly:

- Class 1: a wrong implementation passes while violating a rule, risk ground or cited Principle.
- Class 2: a second-guard hole, an in-increment non-reproducing figure or a criterion that refuses a correct implementation.

A loop is clean with zero class 1, at most three low or medium class 2 findings, and no finding outside both classes.

## Evidence

Use only:

```text
/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r1-gpt
```

Create a reviewer-owned child directory. Never use bare `/tmp` or wildcard deletion. Run project commands through the project direnv environment.

## Output

Write only:

```text
docs/plans/agent-scaffold.reviews/q78-foreclosure-r1-reviewer-gpt.md
```

Give every finding a stable id, owner, severity, proposed class, reproduced evidence and smallest correction. Include both loops in a raw-count table. State the total and severity ceiling.

Commit only that file with a conventional `docs:` commit. Do not edit product, plan, ledger, metrics, briefs, code or pack. Do not push.
