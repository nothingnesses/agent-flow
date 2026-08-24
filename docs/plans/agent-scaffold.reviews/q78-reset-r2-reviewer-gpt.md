# Q-78 reset round 2 review — GPT lens

## Result

Six findings. All belong to `step-intent-encoding`; the D1, D2, D3 and D5 repairs reproduce.

The full repository gates passed at `f5260c6`: 470 tests, Clippy with warnings denied, both validation modes, and strict render check. The two new metrics records each occur once and the generated plan is current. For the reset repairs, the repaired D1 filter retains the authored `+` row, the corrected ledger selector reaches 131 citations at or above 85 versus 117 under the old lower-case-only form, and the sidecar population partitions as `pre=52 = exempt=21 + eighty_four=1 + drift=30`.

## GPT-R2-1 — Human projection criteria do not exercise repeated blank lines or bare CR

- **Increment:** `step-intent-encoding-inc1`
- **Severity:** medium
- **Candidate class:** class 1
- **Violated contract:** RULE 10 requires every internal blank line to survive, CRLF and CR to normalise to LF, and all human projections to use the quoted-line representation (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:53`, `:95`).

### Evidence

The executable criteria use a single paragraph, a continuation collapsed to one paragraph, or two paragraphs separated by exactly one blank line (`step-intent-encoding.md:177-255`). No criterion supplies repeated blank lines or a bare CR to `render`, human `next`, or human `status --step`.

A runnable wrong-helper construction is at the authorised scratch path:

```bash
SCR=/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r2-gpt
rustc "$SCR/bad_human_projection.rs" -o "$SCR/bad_human_projection"
"$SCR/bad_human_projection"
```

It prints:

```text
specified_single=pass
specified_one_blank=pass
specified_continuation=pass
repeated_blank_actual="> paragraph one\n>\n> paragraph two"
repeated_blank_expected="> paragraph one\n>\n>\n> paragraph two"
bare_cr_actual="> paragraph one\rparagraph two"
bare_cr_expected="> paragraph one\n> paragraph two"
```

This helper can replace the proposed shared human formatter in an otherwise-correct implementation. Every input shape named by the human-output criteria still passes, while two explicit RULE 10 behaviours fail.

### Smallest correction

Add exact-byte fixtures for repeated blank lines, CRLF and bare CR to all three human surfaces, plus a red mutation that collapses blank runs and leaves bare CR untouched.

## GPT-R2-2 — `next --json` can apply display normalisation while its only JSON fixture stays green

- **Increment:** `step-intent-encoding-inc1`
- **Severity:** medium
- **Candidate class:** class 1
- **Violated contract:** RULE 10 says JSON preserves the deserialised string unchanged (`step-intent-encoding.md:53`); the `next` contract repeats that requirement (`:127-139`).

### Evidence

Criterion 2 compares `status --step --json` with parser values, but criterion 7 tests `next --json` only with an already-trimmed LF value containing one paragraph break (`step-intent-encoding.md:210-226`). It never gives `next` leading/trailing whitespace, CRLF, or bare CR.

Runnable wrong implementation:

```bash
SCR=/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r2-gpt
rustc "$SCR/bad_next_json.rs" -o "$SCR/bad_next_json"
"$SCR/bad_next_json"
```

Output:

```text
specified_next_json_fixture=pass
actual="paragraph one\nparagraph two"
expected="  paragraph one\rparagraph two  "
```

The mutation trims and normalises the machine value. It passes criterion 7's exact logical shape while changing another valid deserialised string.

### Smallest correction

Run `next --json` over the same logical-value matrix used to prove TOML forms, including outer whitespace and escaped `\r`/`\r\n`, and byte-compare each context value with the parser result. Add the normalising mutation as a red control.

## GPT-R2-3 — The status matrix omits both partial optional states

- **Increment:** `step-intent-encoding-inc1`
- **Severity:** medium
- **Candidate class:** class 1
- **Violated contract:** a declared step has `found: true`, and each optional field independently carries its string or `null` (`step-intent-encoding.md:144`). The optional schema deliberately admits a partial state, and the render golden exercises `problem` alone (`:187`).

### Evidence

Criterion 8 exercises both fields present, both absent, and an unknown slug, but never `problem=Some/approach=None` or its mirror (`step-intent-encoding.md:227-260`). Therefore it cannot distinguish a field-wise implementation from one that collapses a partial step into an unknown or no-intent result.

Runnable wrong projection:

```bash
SCR=/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r2-gpt
rustc "$SCR/bad_status_projection.rs" -o "$SCR/bad_status_projection"
"$SCR/bad_status_projection"
```

Output:

```text
criterion_good=pass criterion_no_intent=pass criterion_unknown=pass
partial_actual=Unknown
partial_expected=Known { problem: Some("kept problem"), approach: None }
```

The wrong projection passes every data-state fixture criterion 8 names and loses a valid field in the omitted state.

### Smallest correction

Add human and JSON status checks for both one-field permutations. Require `found: true`, preserve the present field exactly, and emit `(not recorded)`/`null` only for the absent field. Include a red mutation that collapses either partial state.

## GPT-R2-4 — R4's aggregate label counts permit an omission and a duplicate to cancel

- **Increment:** `step-intent-encoding-inc1`
- **Severity:** medium
- **Candidate class:** class 1
- **Violated contract:** R4 calls itself a total projection and cites Principle 8, Structured data first, project for humans (`step-intent-encoding.md:523-555`). RULE 10 requires each step's values to project under its labels.

### Evidence

R4 counts source fields and rendered labels globally. It never associates a label block with the step that owns the source field. An omitted block on one step and duplicate block on another therefore satisfy every stated equality.

Runnable wrong rendered projection:

```bash
SCR=/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r2-gpt
bash "$SCR/r4_offsetting.sh"
```

Output:

```text
R4 aggregate: steps=2 source=2/2 quoted=0/0 projected=2/2
alpha_problem_labels=0 beta_problem_labels=2
```

This meets R4's batch relation exactly while `alpha` loses its problem and `beta` receives two. The increment-1 golden's named ranges do not prevent a renderer defect scoped to other slugs, and the live plan has no intent values during increment 1.

### Smallest correction

Reconcile per slug: within each generated Step Details section, require exactly one label and the correctly quoted value for each present field, and no label for an absent field. Add the offsetting omission/duplication as a red control. Keep global quoted-label subtraction only as a secondary census.

## GPT-R2-5 — The structured Q-78 ask still restores the superseded single-line design

- **Increment:** `step-intent-encoding-inc1`
- **Severity:** medium
- **Candidate class:** class 1
- **Violated decision:** the authoritative decision permits one or more paragraphs and applies no sentence, line, or character cap. The review brief explicitly requires that no live clause restore the superseded design.

### Evidence

The plan's structured queue still says the recommendation is “two required single-line fields ... one sentence each” at `docs/plans/agent-scaffold.plan.toml:2259`. It separately says a scaffolded plan needs “two prose sentences” at `:2269`. These are in the appended “THE PASS RAN” outcome text that the ask itself makes authoritative, not in the earlier brief it marks historical.

By contrast, `docs/plans/agent-scaffold.questions/Q-78.md:1-3`, `docs/plans/step-intent-encoding.explorations/Q-78.md:85`, and the step's RULES all state the paragraph decision. The inconsistency is faithfully projected: strict render check reports the plan up to date, so this is not stale generated Markdown.

Exact reproducer:

```bash
grep -nE 'required single-line|one sentence each|two prose sentences' docs/plans/agent-scaffold.plan.toml
cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
```

The first command prints lines 2259 and 2269; the second prints `up to date`. This leaves two authoritative representations of the decision and violates Principle 16, One source of truth, while all mechanical gates pass.

### Smallest correction

Revise the Q-78 `ask` in `agent-scaffold.plan.toml` to mark the former recommendation historical and replace both live sentence-bound statements with the paragraph contract, then re-render the generated view.

## GPT-R2-6 — The decision records promise three eventual residuals while the owning step has four

- **Increment:** `step-intent-encoding-inc3`
- **Severity:** low
- **Candidate class:** class 1
- **Violated rule:** the exploration and structured question both say every accepted residual belongs in the eventual decision receipt, while the step says its residual list is the single home. Principle 16 requires one authoritative set.

### Evidence

- `docs/plans/agent-scaffold.plan.toml:2285` says there are three residuals and enumerates them.
- `docs/plans/step-intent-encoding.explorations/Q-78.md:324` likewise says three and says all three live in the step.
- `docs/plans/agent-scaffold.steps/step-intent-encoding.md:799-809` says there are four and adds residual 4, the accepted `next`/`status` parse-failure reporting cost.

Reproducer:

```bash
grep -n 'THREE RESIDUALS' docs/plans/agent-scaffold.plan.toml
grep -n 'Three residuals' docs/plans/step-intent-encoding.explorations/Q-78.md
grep -nE '^Four\.|^RESIDUAL 4' docs/plans/agent-scaffold.steps/step-intent-encoding.md
```

A closing receipt following either pointer omits an accepted residual while every implementation criterion remains green. This is new evidence about recording the residual, not a re-raise of its accepted behaviour.

### Smallest correction

Make the structured ask and exploration point to the sidecar without restating a count, or update both to four and include residual 4 in the eventual-receipt obligation; then re-render.

## Gate evidence

```text
cargo test: 470 passed, 0 failed
cargo clippy --all-targets -- -D warnings: exit 0
validate --source ... --metrics ...: 426 records; 105 steps, 80 questions, valid
validate --source ... --workflow: workflow invariants hold
render --check --strict: up to date
```
