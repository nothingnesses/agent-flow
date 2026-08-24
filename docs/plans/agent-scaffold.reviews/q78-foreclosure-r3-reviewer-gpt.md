# Q-78 post-escalation round 3 GPT review

## Scope and gates

I reviewed only `step-intent-encoding-inc1` on the current `plan/q78-design-pass` product. I did not read the other round-3 review. I treated R2-1 and R2-2 as settled permitted class-2 findings and did not re-raise them.

All scratch evidence and the Cargo target are under the authorised reviewer child `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r3-gpt/reviewer-gpt`. Every project command ran through `direnv exec .`.

Baseline gates pass:

- `cargo test`: 470 passed, zero failed.
- `cargo clippy --all-targets --all-features -- -D warnings`: passed.
- `validate --source ... --metrics ...`: 454 records, 105 steps and 81 questions valid.
- The same validation with `--workflow`: workflow invariants hold.
- Strict render checks for `agent-scaffold.plan.toml` and `TEMPLATE.plan.toml`: up to date.
- `git diff --check`: passed.
- The current sizing commands reproduce `steps=105 batches=6 size=18` and six declared batch loops; the leading-heading selector still returns only `core-assets.md`.

## Findings

### GPT-R3-1 - the all-state seam bypasses the separate pending-step transfer - medium, class 1

The contract requires `problem` and `approach` in every loop state (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:112`), and numbered RULE 10 makes `next` one of the projections this increment must pin. The end-to-end matrices, however, enter only through the in-progress paths `AwaitingFirstReview` and `AwaitingFixes` (`:260-318`). The all-state test then starts below the production transfer boundary by constructing a `LoopFacts` with both fields and calling `build_context` directly (`:320-324`).

That misses a real separate constructor. The current production shape builds pending loops through `build_pending_loop` and constructs their `LoopFacts` independently at `src/next.rs:768-778`; the existing `ready_to_plan_row` and `blocked_row` tests check state metadata but not intent context (`src/next.rs:1377-1400`). An implementation can copy both fields in the in-progress builders, implement `build_context` perfectly for all nine states, but set both pending `LoopFacts` fields to `None`. Every specified matrix and the all-state seam still pass while actual `ReadyToPlan` and `Blocked` instructions omit both values.

Reproduction:

```text
direnv exec . bash /tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r3-gpt/reviewer-gpt/pending-transfer-counterexample.sh
specified in-progress matrices: pass
specified all-state build_context seam: pass
production ReadyToPlan: problem=<absent> approach=<absent>
production Blocked: problem=<absent> approach=<absent>
```

This is class 1 because the counterexample passes the stated guards while violating RULE 10's `next` projection and the explicit every-loop-state requirement. It is distinct from R2-1's one-field inputs and R2-2's red-control rationale. Add an end-to-end TOML projection oracle for intent-bearing `ReadyToPlan` and `Blocked` steps, on both human and JSON output, and a red mutation that drops the fields only in `build_pending_loop`.

### GPT-R3-2 - the "no eighth subcommand" selector ignores hyphenated commands - low, class 1

Criterion 8 says its help count is the executable form of the Principle 2 ruling and claims an implementation that adds a subcommand prints `9` (`step-intent-encoding.md:404-410`). Its regex, `^  [a-z]+ `, does not count a normal hyphenated Clap name such as `intent-query`.

I inserted one such command row into the current real help output and ran the criterion unchanged. The result is:

```text
criterion_selector=8
actual_command_rows=9
inserted=1
```

The exact output is in `.../reviewer-gpt/subcommand-counterexample.txt`; the input is `help-with-hyphenated-eighth.txt`. Thus an implementation can add the forbidden eighth product subcommand alongside `status --step`, leave every other criterion green, and still satisfy the stated count. This is class 1 because it passes the criterion while violating the cited Principle 2 ruling. Count every command token (for example `^  [^[:space:]]+[[:space:]]`) or, preferably, assert the exact Clap subcommand-name set through `CommandFactory`.

### GPT-R3-3 - no `next` oracle exercises the Markdown normalisation boundary - low, class 2

The product contract explicitly requires `steps_from_markdown` to set both fields to `None` because the Markdown Roadmap has no intent columns (`step-intent-encoding.md:112`). None of increment 1's `next` acceptance paths exercises that function: the two complete matrices use TOML sources (`:260-318`), and the state-axis test injects `LoopFacts` directly (`:320-324`). The current parity test cannot supply the missing guard: `toml_and_markdown_sources_give_the_same_verdict` compares only step, increment and state, not instruction context (`src/next.rs:2160-2202`).

Consequently, a wrong `steps_from_markdown` implementation can fabricate `Some` intent from a Markdown field such as status or slug. All new oracles and the existing parity test still pass, while human and JSON `next --plan ...` emit invented agent instructions. This is a second-guard hole, class 2, and differs from R2-1's partial TOML values. Extend the dual-source test or add a CLI fixture that runs `next --plan` on an in-progress Markdown Roadmap and asserts that neither intent key exists on both surfaces.

## Outcome

Three distinct findings: one medium and two low; two class 1 and one class 2. Under the controlling foreclosure condition this round is not clean because class 1 must be zero. No waiver is authorised or used.
