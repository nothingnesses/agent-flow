# Q-78 reset round 3 GPT review brief

Act only as an independent reviewer. Work only in your assigned isolated review worktree. Do not edit the reviewed product.

## Review target

Review the current `plan/q78-design-pass` branch after commit `bf13e6f`, excluding review briefs from the product.

Read these files first:

- `AGENTS.md`.
- `docs/plans/agent-scaffold.ledger.md`, starting at `RESUME HERE`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r2-triage.md`.
- `docs/plans/agent-scaffold.reviews/q78-reset-r2-fix-brief.md`.
- The current plan TOML, generated view, Q-78 exploration and Q-81 item.
- The active increment sidecars named below.

Do not read another reset round 3 reviewer file. Do not inherit another reviewer's conclusions.

## Active loops

Review only these five active loops:

- `sidecar-status-opening-drift-inc1`, current streak 0.
- `ledger-order-citation-currency-inc1`, current streak 1.
- `plan-order-array-position-inc2`, current streak 1.
- `step-intent-encoding-inc1`, current streak 0.
- `step-intent-encoding-inc3`, current streak 0.

Each loop is `risky`. Each needs two consecutive clean rounds. This is reset round 3, with three rounds used after this review.

These loops already converged and are outside this review:

- `plan-order-array-position-inc1`.
- `step-intent-encoding-inc2a` through `step-intent-encoding-inc2f`.
- `validate-missing-source-exit-inc1`.

Do not re-open T7a through T7f or D7 without new evidence that changes the class, severity or measured boundary. The six T7 loops converged under the class 2 threshold.

## Settled boundaries

The reset round 2 repair addresses T1, T2, T3, T4, T6, T8 and T9. Verify those repairs independently. Do not assume that the repair is correct.

`GPT-R2-5` is dismissed. Do not re-raise it without new evidence that defeats the historical framing cited by triage.

The accepted residuals remain `GB-4`, `GB-9`, `F2` and `F3`. Do not file one as new without evidence that changes its recorded boundary.

Decision `Q-81` counts clean outcomes through the paragraph-value scope change. Do not reopen that decision without new evidence that defeats its recorded reasoning.

## Lens

Use a ground-blind falsification lens. Assume that a wrong implementation can satisfy each criterion.

For each active increment:

1. Identify the rules, risks and principle claims that the criteria promise to enforce.
2. Build the smallest wrong implementation or fixture that can pass the written criteria.
3. File a finding if the wrong result passes or a correct result fails.
4. Reproduce every behavioural claim in the owned scratch directory.

Focus on exact bytes, parser-value independence, per-step ownership, partial states, carriage returns, blank-run preservation, residual-set consistency and changed-path completeness. Check the two unchanged streak-one loops independently rather than declaring them clean by inheritance.

Use the stop-condition classes exactly:

- Class 1 means a wrong implementation passes while violating a stated risk ground, numbered rule or cited plan Principle.
- Class 2 means a second-guard hole, an in-increment non-reproducing figure or a criterion that refuses a correct implementation.

A loop is clean only with zero class 1 findings and at most three class 2 findings, all `low` or `medium`. A valid finding outside both permitted classes makes the loop `new_valid`.

## Evidence

Use only this scratch root:

```text
/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r3-gpt
```

Create a reviewer-owned child directory. Never use bare `/tmp`. Never use wildcard deletion.

Run project commands through the project direnv environment. Use GNU grep where the criteria require GNU behaviour.

Use runnable evidence for behavioural claims. Use exact `file:line` evidence for prose and design claims. Do not use a contrived test when a command or citation settles the claim.

## Output

Write only:

```text
docs/plans/agent-scaffold.reviews/q78-reset-r3-reviewer-gpt.md
```

Give every finding:

- A stable id.
- One owning active increment.
- Severity: `low`, `medium`, `high` or `critical`.
- Proposed class: class 1, class 2 or neither.
- The violated rule, risk ground or Principle.
- Reproduction commands and observed output, or exact citations.
- The smallest required correction.

Include a per-increment raw count table, including zero-finding loops. State the raw total and severity ceiling. State zero findings plainly if the review is clean.

Commit only the findings file with a conventional `docs:` commit. Do not edit the plan, ledger, metrics, briefs, code or pack. Do not push.
