# Q-78 post-escalation round 2 GPT review brief

Act only as an independent reviewer in your isolated worktree. Do not edit product.

Review `plan/q78-design-pass` after `c54a0b9`, excluding review briefs. Read `AGENTS.md`, the ledger from `RESUME HERE`, post-escalation round 1 triage and fix brief, and the current `step-intent-encoding` sidecar. Do not read the Claude round 2 review.

Review only:

- `step-intent-encoding-inc1`, entering streak 0.
- `step-intent-encoding-inc3`, entering streak 1.

Both are risky. This is reset round 2. A clean increment 1 reaches streak 1. A clean increment 3 reaches streak 2 and converges.

Verify FR1-2 independently. Do not re-open FR1-1, FR1-3, FR1-4, I2, I6, I7, D7, T7a through T7f, prior dismissals or accepted residuals without evidence that changes their settled boundary. No waiver is authorised.

Use ground-blind falsification. Attack the exhaustive state-table construction, exact values, negative control, future enum growth, test retention and every active acceptance criterion.

Class 1 means a wrong implementation passes while violating a risk ground, numbered rule or cited Principle. Class 2 means a second-guard hole, an in-increment non-reproducing figure or a criterion that refuses a correct implementation. A loop is clean with zero class 1, at most three low or medium class 2 findings, and no finding outside both classes.

Use only this scratch root and create a reviewer-owned child:

```text
/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r2-gpt
```

Never use bare `/tmp` or wildcard deletion. Run project commands through direnv.

Write only `docs/plans/agent-scaffold.reviews/q78-foreclosure-r2-reviewer-gpt.md`. Give each finding an id, owner, severity, class, evidence and correction. Include both loops in the count table. Commit only that file with a `docs:` subject. Do not push.
