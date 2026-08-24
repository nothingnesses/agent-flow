# Q-78 post-escalation round 3 triage

## Scope and gates

I independently adjudicated the four round-3 reports against `0d4cbca`, the current `plan/q78-design-pass` tip. I read the ledger's `RESUME HERE` state, the round-2 triage, both round-3 reviewer reports, and the active increment-1 sidecar. I did not use a reviewer fixture. My independently authored countermodels, generated help transcript, and Cargo target are under the authorised child directory `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r3-triage/triager`.

Every project command ran through `direnv`'s loaded flake environment with `CARGO_TARGET_DIR` inside that child. The baseline is green:

- `validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl`: 454 records, 105 steps, and 81 questions valid.
- The same command with `--workflow`: workflow invariants hold.
- Strict `render --check` is up to date for both `agent-scaffold.plan.toml` and `TEMPLATE.plan.toml`.
- `cargo test`: 470 passed, zero failed.
- `cargo clippy --all-targets --all-features -- -D warnings`: passed.
- `git diff --check`: passed. The worktree is otherwise clean before this triage output.

`R2-1` and `R2-2` remain settled permitted low class-2 findings. No changed evidence reopens either.

## Raw verdicts

| Raw finding | Verdict | Distinct finding | Owner | Severity | Class | Evidence and correction |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-R3-1 | valid | R3-1 | `step-intent-encoding-inc1` | medium | 1 | E1 proves the planned matrices and direct seam admit a pending-loop transfer that drops both fields, violating the every-loop-state `next` contract. Add TOML `next` end-to-end assertions for both `ReadyToPlan` and `Blocked`, on human and JSON surfaces, and a red mutation that drops only the pending transfer. |
| GPT-R3-2 | valid | R3-2 | `step-intent-encoding-inc1` | low | 1 | E2 proves the proposed help selector keeps returning 8 after a hyphenated eighth command is added, despite the Principle 2 no-new-subcommand rule. Count every command token, such as `^  [^[:space:]]+[[:space:]]`, or assert Clap's exact subcommand-name set; add the hyphenated red control. |
| GPT-R3-3 | valid | R3-3 | `step-intent-encoding-inc1` | low | 2 | E3 proves that neither planned `next` matrix enters through the Markdown normalisation boundary and the existing parity test ignores context. Add a Markdown `next --plan` fixture that asserts both intent keys are absent on human and JSON outputs, plus a red mutation that fabricates either Markdown field. |
| R3C-1 | valid | R3-4 | `step-intent-encoding-inc1` | low | 2 | E4 proves that the increment's asserted unchanged population includes the render fixture whose declarations criterion 4 itself requires to gain fields. Scope the unchanged assertion to the live plan and explicitly exempt the render fixture, without asserting an unmeasured remainder. |

No two reports identify the same defect: E1 is the TOML pending constructor, E2 is the help-row selector, E3 is the Markdown source boundary, and E4 is the sidecar's declaration-site scope claim.

## Reproduced evidence

### E1 — R3-1: the all-state seam starts below the pending transfer

The contract says `StepInfo` carries both fields, `steps_from_toml` copies them, `LoopFacts` carries them, and `build_context` inserts each present field in every loop state (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:112`). The complete runtime matrices only enter through the in-progress `AwaitingFirstReview` and `AwaitingFixes` paths (`:260-318`). The all-state test supplies a populated `LoopFacts` directly to `build_context` (`:320-324`).

That misses the separately constructed pending path: `build_pending_loop` constructs `LoopFacts` independently (`src/next.rs:763-778`), while the current ready and blocked tests assert only state metadata or `blocked_by` (`src/next.rs:1377-1400`). A wrong implementation can correctly copy fields in the in-progress builder and unconditionally insert fields in `build_context`, yet initialise both fields to `None` only in `build_pending_loop`.

My triager-authored countermodel, which models precisely those three planned guards rather than any reviewer fixture, reports:

```text
in-progress review matrix: pass
in-progress fix matrix: pass
direct all-state build_context seam: 9/9 pass
wrong ReadyToPlan pending transfer: problem=<absent> approach=<absent>
wrong Blocked pending transfer: problem=<absent> approach=<absent>
```

Thus the stated `next` contract fails for two real loop states while all listed increment-1 guards pass. This is class 1: it violates the increment's stated every-loop-state projection contract and passes its guards. It is medium because both fields disappear from planner or blocker-resolution instructions on a shipped query surface.

### E2 — R3-2: the help selector excludes a valid hyphenated command

The only executable enforcement for the Principle 2 decision is the selector at `step-intent-encoding.md:404-410`, `grep -cE '^  [a-z]+ '`. The current `Command` enum already exposes the ordinary Clap subcommand surface at `src/main.rs:411-425`; the criterion places no restriction on a future subcommand name.

I generated the current binary's `Commands:` section in scratch, inserted the triager-authored row `  intent-query  forbidden hyphenated command`, and reran the criterion selector and a token selector:

```text
current_selector=8
mutant_selector=8
mutant_all_command_tokens=9
```

The existing regex stops at the hyphen, so adding the forbidden eighth product subcommand passes the criterion. This is a low class-1 hole: its direct consequence is unnecessary public CLI surface contrary to the cited Principle 2 ruling, but it does not corrupt data or execution.

### E3 — R3-3: Markdown intent absence has no `next` oracle

The planned boundary specifically requires `steps_from_markdown` to set both fields to `None` because the Markdown Roadmap has no intent columns (`step-intent-encoding.md:112`). The planned `next` matrices remain TOML in-progress matrices (`:260-318`) and the all-state seam injects `LoopFacts` (`:320-324`). The current normaliser is a separate function (`src/next.rs:552-567`), and the existing dual-source test compares only `step`, `increment`, and `state` (`src/next.rs:2160-2202`), not the instruction context.

My independent boundary model preserves those three compared metadata values while giving the Markdown path fabricated context values. It reports:

```text
metadata-only TOML/Markdown parity: pass
wrong Markdown next context: problem=derived-from-slug approach=derived-from-status
```

A correct status test cannot close this: it exercises `status`, not `next`. This is a low class-2 second-guard hole. The explicit no-intent Markdown expectation is present, but it is not a risk ground, numbered rule, or cited Principle that would make this class 1.

### E4 — R3-4: the unchanged declaration-site claim contradicts criterion 4

The scope boundary says none of the 69 inline `[[step]]` declaration sites changes in increment 1 and all change in increment 3 (`step-intent-encoding.md:156-158`). Criterion 4, however, names `src/plan/testdata/render-fixture.plan.toml` and requires fields on `alpha`, `gamma`, `eta`, and `beta` in this increment (`:202`). That file has seven `[[step]]` blocks; GNU grep independently located the four named blocks. Criterion 11 repeats the false claim that no `[[step]]` field changes in this increment (`:440`).

The false sentence cannot make an implementation pass or fail wrongly: criterion 11's path list already includes the fixture and criteria 4 through 6 require the fixture changes. It is therefore a low class-2 in-increment non-reproducing scope figure. The correction must not claim that all 69 sites, or an unmeasured numeric remainder, change in a particular increment. State instead that the live `docs/plans/agent-scaffold.plan.toml` remains unchanged in increment 1 while criterion 4 deliberately changes fields in the render-fixture declarations.

## Per-loop outcome

`step-intent-encoding-inc1` is the only active loop. It is `risky`, entered reset round 3 at streak one, and needs two consecutive clean rounds. The foreclosure condition permits no class-1 finding, at most three low or medium class-2 findings, and no finding outside those classes.

| Loop | Entering streak | Raw / distinct findings | Severities | Class 1 / class 2 / neither | Outcome | Resulting streak | Converged |
| --- | ---: | ---: | --- | --- | --- | ---: | --- |
| `step-intent-encoding-inc1` | 1 | 4 / 4 | medium, low, low, low | 2 / 2 / 0 | new valid findings | 0 | no |

The two class-1 findings make this round non-clean. The two remaining reset rounds can still converge after the valid corrections and two clean rounds.

## Totals and backstop

- Raw findings: 4.
- Raw verdicts: 4 valid, 0 dismissed.
- Distinct valid findings: 4.
- Distinct classes: 2 class 1, 2 class 2, 0 outside both classes.
- Severity ceiling: medium.
- Waiver or residual acceptance: none authorised or used.
- Backstop: not owed; no high or critical finding was dismissed.
