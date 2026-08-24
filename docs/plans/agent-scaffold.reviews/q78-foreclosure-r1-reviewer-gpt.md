# Q-78 post-escalation round 1 GPT review

## Scope and method

Reviewed commit `7120d94` on `plan/q78-design-pass`, excluding the review briefs, with ground-blind falsification over only `step-intent-encoding-inc1` and `step-intent-encoding-inc3`. I did not re-open any settled item named in the brief.

Reviewer fixtures and command output are under the authorised child directory `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r1-gpt/reviewer-gpt`.

The baseline gates passed through the project direnv environment:

- `validate`: 450 records valid; 105 steps and 81 questions valid.
- `validate --workflow`: workflow invariants hold.
- `render --check --strict`: up to date.
- `cargo test`: 470 passed, 0 failed.
- `cargo clippy --all-targets --all-features -- -D warnings`: exit 0.
- `git diff --check 7120d94^..7120d94`: exit 0.
- The repair commit changes only `docs/plans/agent-scaffold.steps/step-intent-encoding.md` and the rendered `docs/plans/agent-scaffold.md`; both have zero non-ASCII matches under the required check.

## Findings

### GPT-FR1-1 - The empty-body oracle exercises both fields, not the required one-field case

- **Owner:** `step-intent-encoding-inc1`
- **Severity:** low
- **Proposed class:** Class 1

The rule says a step carrying **at least one** field contributes an entry even when its body is empty (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:100`). The repaired oracle constructs an empty-body step with both `problem` and `approach` present (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:218`). The partial `eta` fixture has one field but a non-empty body (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:202`, `:244`).

The smallest wrong renderer contributes when the body is non-empty **or both fields are present**. It passes the new empty-body oracle and the body-bearing partial fixture, but returns no Step Details for an empty body carrying only `problem` or only `approach`.

Reproduced with `falsifiers.sh`:

```text
empty-body: both-fields-oracle=pass body-bearing-partial=pass one-field-empty-rule=fail
```

This is Class 1 because the wrong implementation passes every named coordinate while violating the explicit at-least-one-field render rule.

**Smallest correction:** make the empty-body unit oracle table-driven over `problem` only, `approach` only, and both fields, comparing each complete returned fragment. Add a red guard using the `problem && approach` contribution condition.

### GPT-FR1-2 - Three sampled states still do not enforce intent in every `next` loop state

- **Owner:** `step-intent-encoding-inc1`
- **Severity:** medium
- **Proposed class:** Class 1

The contract requires `build_context` to insert both intent slots "in every loop state" (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:112`). Increment 1 now checks `awaiting-first-review` and `awaiting-fixes` (`:260`, `:294-318`), while increment 3's fresh scaffold adds `ready-to-plan` (`:842-851`). The production state model has additional independently matched variants, including `blocked`, `awaiting-reviewers`, `converged`, `escalate`, and `risk-class-conflict` (`src/next.rs:273-301`).

The smallest wrong implementation inserts intent only for `awaiting-first-review`, `awaiting-reviewers`, `awaiting-fixes`, and `ready-to-plan`. That passes both increment-1 state families and the increment-3 fresh-scaffold projection while omitting intent from `blocked` and the terminal/control states. The current fresh-scaffold probe independently confirmed that the added increment-3 command supplies only the `ready-to-plan` coordinate.

Reproduced with `falsifiers.sh` and the fresh scaffold probe:

```text
next-states: stated-checks=pass blocked-every-state-rule=fail
```

```text
ready-to-plan
isolation_tier,ledger
```

This is Class 1 because a state whitelist can pass all stated state checks while violating the every-state rule on an instruction surface.

**Smallest correction:** keep the full value matrices in the representative review and writer states, and add a table-driven state-axis test over every production `LoopState` that asserts both intent keys and values are present. Its red mutation should whitelist only the currently sampled states and fail on the remaining variants.

### GPT-FR1-3 - The required migration notice has only a path/heading guard

- **Owner:** `step-intent-encoding-inc3`
- **Severity:** medium
- **Proposed class:** Class 1

Criterion 9 proves that `CHANGELOG.md` changed (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:921`), and the documentation-impact paragraph says the Unreleased entry must record both required fields, paragraph support, the absence of a cap, and that earlier plans stop parsing until every step is updated (`:943`). No acceptance check proves any of those contents.

The smallest wrong implementation opens `## [Unreleased]` and adds an unrelated housekeeping bullet. It satisfies the exact changed-path set and the only stated heading probe while omitting the migration warning for the schema break every existing project inherits.

Reproduced with `falsifiers.sh`:

```text
documentation: changed-path-set=pass heading-check=pass required-entry=fail
```

This is Class 1 because the wrong documentation edit passes the executable guards while violating the explicit documentation-impact duty and leaving the Principle 3 adoption cost undisclosed. The accepted `F3` residual covers only duplicate-heading/clobber sequencing and explicitly does not waive either changelog entry (`docs/plans/agent-scaffold.steps/step-intent-encoding.md:945`).

**Smallest correction:** add an executable content oracle for the Unreleased entry that independently requires (1) both `problem` and `approach` as required non-empty fields, (2) one-or-more-paragraph support with no sentence/line/character cap, and (3) the earlier-plan parse break and required per-step migration. Keep the existing path check.

## Coordinates with no finding

- I8 now runs all eight logical-value rows through both fields on both human and JSON `status --step` surfaces, with field-specific red controls.
- I9 now compares the complete no-heading `beta` entry from byte zero and includes a generated-heading red control.
- I11 retains a single named increment-1 projection contract and exercises all four fresh-scaffold TOML projection surfaces after the required flip.

## Raw counts and proposed outcomes

| Loop | Raw findings | Severity ceiling | Class 1 | Class 2 | Proposed round outcome |
| --- | ---: | --- | ---: | ---: | --- |
| `step-intent-encoding-inc1` | 2 | medium | 2 | 0 | new valid; streak remains 0 if upheld |
| `step-intent-encoding-inc3` | 1 | medium | 1 | 0 | new valid; streak remains 0 if upheld |

**Total:** 3 raw findings, all distinct; 3 proposed Class 1, 0 proposed Class 2, and none outside the two classes. **Severity ceiling:** medium. Neither loop is clean under the brief's foreclosure rule.
