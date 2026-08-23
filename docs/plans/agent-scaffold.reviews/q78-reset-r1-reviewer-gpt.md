# Q-78 reset round 1 GPT findings

## GPT-1: sentence-initial step citations are outside the ledger worklist

- **Owning increment:** `ledger-order-citation-currency-inc1`
- **Severity:** `medium`
- **Class:** `class 1`
- **Claim:** The increment promises to annotate every drifting citation, and its risk ground says a missed citation can misattribute evidence, but every selector and oracle is case-sensitive for lowercase `order`/`step`. Sentence-initial `Order`/`Step` citations therefore survive unchanged while all stated criteria pass. This violates the increment's stated ground and WHAT IT DOES obligation.
- **Reproducible evidence:** `docs/plans/agent-scaffold.steps/ledger-order-citation-currency.md:54-58` states the ground and all-citation obligation, while criterion 1 at `:79`, both L1 searches at `:99` and `:112`, and criterion 4 at `:141` accept only lowercase words. From the repository root, GNU grep finds fourteen omitted drifting occurrences:

  ```bash
  grep -oE '\b(Order|Step) [0-9]+\b' docs/plans/agent-scaffold.ledger.md |
    awk '{ if ($NF + 0 >= 85) print }' |
    wc -l
  ```

  Output:

  ```text
  14
  ```

  This includes the vacated historical value at `docs/plans/agent-scaffold.ledger.md:339` (`Step 91`), which criterion 4 also misses. I built a wrong ledger that annotates every lowercase occurrence through the two named tables and leaves every capitalized occurrence untouched. Running criterion 2's L1 verbatim against it passes:

  ```bash
  S=/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r1-gpt
  bash "$S/analysis/l1.sh" \
    "$S/analysis/wrong-ledger-uppercase-unfixed.md" \
    "$S/analysis/ledger-order-table-clean.tsv" \
    "$S/analysis/ledger-history.tsv"
  grep -oE '\b(Order|Step) [0-9]+\b' "$S/analysis/wrong-ledger-uppercase-unfixed.md" |
    awk '{ if ($NF + 0 >= 85) print }' |
    wc -l
  ```

  Output:

  ```text
  drifting=117 annotated=117 bare=0 unknown_slug=0 wrong_slug=0
  14
  ```

  Criteria 1, 3, and 4 use the same lowercase-only population, while criteria 5-8 do not enumerate citations, so the wrong implementation satisfies the full guard set.
- **Required correction:** Make the worklist, L1, the vacated-value search, and their related measurements handle sentence-initial capitalization while preserving each citation's original `Order`/`Step` spelling. Add a mutation that leaves a capitalized drifting citation bare and require the guard to fail.

## GPT-2: sentence-initial citations are outside the sidecar prose sweep

- **Owning increment:** `plan-order-array-position-inc2`
- **Severity:** `medium`
- **Class:** `class 1`
- **Claim:** Increment 2 scopes itself to every numbered sidecar/front-sidecar step citation and says criterion 2 is the mechanical oracle for a missed or wrong reference, but its complete worklist, P1, and post-edit sweep recognize only lowercase `order`/`step`. A wrong implementation can correctly restate every selected row, leave sentence-initial citations pointing at obsolete positions, and pass. This falsifies the increment's risk ground and violates RULE 4's slug-restatement requirement.
- **Reproducible evidence:** The all-citation scope and risk ground are at `docs/plans/agent-scaffold.steps/plan-order-array-position.md:275-281`; criterion 1's selector is lowercase-only at `:288`, P1's surviving-number search is lowercase-only at `:336`, and the post-edit search repeats it at `:367`. The omitted current population is:

  ```bash
  grep -rnoE '\b(Order|Step) [0-9]+\b' \
    docs/plans/agent-scaffold.steps/ \
    docs/plans/agent-scaffold.success-criteria.md \
    docs/plans/agent-scaffold.documentation-protocol.md \
    docs/plans/agent-scaffold._status-narrative.md
  ```

  Output:

  ```text
  docs/plans/agent-scaffold.steps/decision-folder-currency.md:3:Step 89
  docs/plans/agent-scaffold.steps/decision-folder-currency.md:34:Step 89
  docs/plans/agent-scaffold.steps/checks-runner-worktree-name-collision.md:90:Step 85
  docs/plans/agent-scaffold.steps/workflow-enforcement-tier.md:308:Step 92
  ```

  The `Step 85` row, for example, does not name the slug and will point at the wrong declaration position after the field deletion. I built a throwaway tree that applies the specified replacement to every lowercase drifting row, preserves the decided quotation exception, regenerates the projection, and leaves these four rows unchanged. P1 reports its exact passing relation while the four defects remain:

  ```bash
  S=/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r1-gpt
  R="$S/plan-capital-case-repo"
  cd "$R"
  bash "$S/analysis/p1.sh" "$R/pre.txt" "$R/drift.txt" "$R/table.tsv"
  grep -rhoE '\b(Order|Step) [0-9]+\b' \
    docs/plans/agent-scaffold.steps/ \
    docs/plans/agent-scaffold.success-criteria.md \
    docs/plans/agent-scaffold.documentation-protocol.md \
    docs/plans/agent-scaffold._status-narrative.md |
    awk '{ if ($NF + 0 >= 85) print }' |
    wc -l
  ```

  Output:

  ```text
  NUMBER SURVIVES docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md:105 (was step 86)
  rows=26 restated=25 wrong_slug=0 number_survives=1
  4
  ```

  The one `NUMBER SURVIVES` row is the explicitly decided quotation exception, so this is P1's stated correct result.
- **Required correction:** Include `Order` and `Step` in every pre/post population and P1 check, preserve exempt citations in either case, and add a sentence-initial mutation. Re-measure the worklist and regenerate the expected projection after the four real rows are restated by slug.

## GPT-3: TOML line continuation defeats the encoded single-line representation

- **Owning increment:** `step-intent-encoding-inc1`
- **Severity:** `medium`
- **Class:** `class 1`
- **Claim:** RULE 1 forbids multiline TOML blocks because physical block growth is the cost the design controls, and RULE 2 claims a pure check over the deserialized string catches every `"""` block. TOML basic multiline strings can escape their physical newline with a trailing backslash. The parser then gives `validate` a one-line `String`, so the specified implementation and all six criterion-2 fixtures accept an arbitrarily many-line `problem` or `approach` representation. This violates numbered RULE 1 and the Principle 5 (`Make illegal states unrepresentable`) ruling cited by RULE 2.
- **Reproducible evidence:** The physical-line cost is stated at `docs/plans/agent-scaffold.steps/step-intent-encoding.md:23-25`; RULE 1's explicit "never `"""`" requirement is at `:29`; RULE 2 limits the implementation to the deserialized value at `:31`; criterion 2 only asks for multiline values whose newline survives deserialization at `:143-159`. The project uses `toml = "0.8"`. A probe using that exact dependency shows the representation/value split:

  ```bash
  S=/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r1-gpt
  CARGO_TARGET_DIR="$S/toml-probe-target" \
    cargo run --quiet --manifest-path "$S/toml-probe/Cargo.toml"
  ```

  Output:

  ```text
  source_lines=2 value="first second" contains_newline=false
  ```

  The analogous current-schema control at `$S/analysis/multiline-continuation.plan.toml` uses this representation for the existing `title: String`; `cargo run --quiet -- validate --source <that path>` prints `1 steps, 0 questions, valid` at exit 0. Replacing `title` with either proposed intent key after increment 1 leaves the proposed `value.contains('\n') || value.contains('\r')` guard no signal to reject. Render, `next`, and `status` also receive the same one-line value, so the remaining criteria pass.
- **Required correction:** Enforce the physical TOML representation before it is erased by Serde, and add continuation-block fixtures for both fields to the hand-run checks and unit tests. If only the deserialized value is meant to be constrained, instead remove the "never multiline block" rule and the physical-line cost claim; the current specification cannot promise both.

## Per-increment raw counts and severity ceilings

| Increment | Raw findings | Severity ceiling |
| --- | ---: | --- |
| `sidecar-status-opening-drift-inc1` | 0 | none |
| `ledger-order-citation-currency-inc1` | 1 | `medium` |
| `plan-order-array-position-inc1` | 0 | none |
| `plan-order-array-position-inc2` | 1 | `medium` |
| `step-intent-encoding-inc1` | 1 | `medium` |
| `step-intent-encoding-inc2a` | 0 | none |
| `step-intent-encoding-inc2b` | 0 | none |
| `step-intent-encoding-inc2c` | 0 | none |
| `step-intent-encoding-inc2d` | 0 | none |
| `step-intent-encoding-inc2e` | 0 | none |
| `step-intent-encoding-inc2f` | 0 | none |
| `step-intent-encoding-inc3` | 0 | none |
| `validate-missing-source-exit-inc1` | 0 | none |
