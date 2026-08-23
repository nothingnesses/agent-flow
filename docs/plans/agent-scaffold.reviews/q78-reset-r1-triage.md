# Q-78 reset round 1 triage

## Method

I read both reviewer findings, the round-4 triage, reset-fix brief, both review briefs, the live ledger from `RESUME HERE (2026-08-23)`, and all five Q-78 sidecars. I rebuilt the behavioural demonstrations in `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-reset-r1-triage`; I did not read either reviewer fixture directory. Toolchain commands used `direnv allow && eval "$(direnv export bash)"`; GNU grep was `/nix/store/gn94gpcp5q08x4v6g8mvw8v4r65rcjzk-gnugrep-3.12/bin/grep` where its syntax mattered.

All nine raw findings reproduce. No submitted demonstration needed a material correction. The seven distinct findings below are new defects in the repaired sidecars, not re-raises of settled items: C-1 attacks the new GB-1 guard; the two citation findings attack population coverage rather than the settled named-commit tables; GPT-3 is distinct from accepted residual GB-4; C-4 and C-5 attack new criterion contradictions; and C-6 is distinct from F1's repaired handover invocation.

## Deduplication map

| Distinct finding | Raw findings | Owning increment |
| --- | --- | --- |
| D1: opening-additions filter is inert | C-1 | `sidecar-status-opening-drift-inc1` |
| D2: uppercase ledger citations are outside the worklist | GPT-1, C-3 | `ledger-order-citation-currency-inc1` |
| D3: uppercase sidecar citations are outside the worklist | GPT-2, C-2 | `plan-order-array-position-inc2` |
| D4: TOML continuation hides a physical multiline block | GPT-3 | `step-intent-encoding-inc1` |
| D5: the post sweep omits the 84 rows | C-4 | `plan-order-array-position-inc2` |
| D6: increment 3 requires an unchanged generated view in its exact diff | C-5 | `step-intent-encoding-inc3` |
| D7: out-of-repository criteria cannot locate `./target/debug/agent-flow` | C-6 | `validate-missing-source-exit-inc1` |

## Raw verdicts

| Raw finding | Verdict | Distinct finding | Severity | Class |
| --- | --- | --- | --- | --- |
| GPT-1 | valid | D2 | medium | class 1 |
| GPT-2 | valid | D3 | medium | class 1 |
| GPT-3 | valid | D4 | medium | class 1 |
| C-1 | valid | D1 | medium | class 1 |
| C-2 | valid | D3 | medium | class 1 |
| C-3 | valid | D2 | medium | class 1 |
| C-4 | valid | D5 | low | class 2 -- criterion refuses a correct implementation |
| C-5 | valid | D6 | medium | class 2 -- criterion refuses a correct implementation |
| C-6 | valid | D7 | low | class 2 -- criterion refuses a correct implementation |

## Distinct findings and required corrections

### D1 -- opening-additions filter is inert

**Class 1, medium.** The premise says the increment authors no replacement prose and that criterion 6 rejects every added word (`sidecar-status-opening-drift.md:39-43`), while the accepted G-F9 boundary relies on the same guard (`:213`). The filter must therefore distinguish added words from the diff header.

The exact current filter at `:229` is `grep -v '^\+\+\+'`, a basic-regex invocation. GNU grep warns `stray \ before +` and removes both `+++ b/x` and `+authored words`; changing only that command to `grep -vE '^\+\+\+'` retains `+authored words`.

I built the prescribed 17-file bare-token deletion, then appended `This newly authored sentence carries no status vocabulary.` to the worklist opening in `decision-folder-currency.md`. The selector/handover relation, changed-path set, and 2/2 numstat bound all passed (`selector_difference=0`, `changed_set_difference=0`, `worklist_numstat_outside_2_2=0`). The criterion-6 script printed `checked=17 bad_anchor=0 added=0`, while the raw porcelain diff contains the added sentence. The mutation violates the premise while its consequence still holds.

**Required correction:** use an ERE header exclusion, such as `grep -vE '^\+\+\+'`, and add the authored-opening mutation as a red control requiring non-zero `added`. Reconcile `:213` with the implementation: either limit the word-diff to the opening or say clearly that the guard is stricter and scans the whole changed file.

### D2 -- uppercase ledger citations are outside the worklist

**Class 1, medium.** `ledger-order-citation-currency.md:58` requires every citation at or above 85 to be annotated, but criterion 1, both L1 loops, and criterion 4 only match lowercase (`:79`, `:99`, `:112`, `:141`). GNU grep finds 14 capitalized `Order`/`Step` citations at or above 85; criterion 4 also misses `339:Step 91`.

I generated named current and historical (`5fcd020`) resolution tables, annotated every lowercase drifting occurrence in a scratch ledger, and left the capitalized population unchanged. L1 printed `drifting=117 annotated=117 bare=0 unknown_slug=0 wrong_slug=0`; the 14 capitalized citations remained. The lowercase vacated-value search prints 14 rows and the capitalized equivalent adds `339:Step 91`. Thus the stated all-citation obligation and ledger risk ground can be violated by an implementation all current guards accept.

**Required correction:** make criterion 1, both L1 loops, and criterion 4 recognize `[Oo]rder|[Ss]tep`; preserve the original leading-word spelling in the annotation and make L1 accept it. Add a capitalized bare-citation mutation, and explicitly dispose of capitalized rows that already carry a bare slug.

### D3 -- uppercase sidecar citations are outside the worklist

**Class 1, medium.** The all-citation scope and risk ground are at `plan-order-array-position.md:275-281`, while criterion 1, P1, and the post sweep use lowercase-only selectors (`:288`, `:336`, `:367`). GNU grep finds four unselected capitalized citations in the stated source set, including the bare `Step 85` at `checks-runner-worktree-name-collision.md:90`.

I restated every lower-case drifting row in a scratch tree except the decided quotation. P1 printed `rows=26 restated=25 wrong_slug=0 number_survives=1`; all four capitalized citations remained. This is a wrong implementation that passes P1 while leaving citations that will resolve to nothing or the wrong step.

**Required correction:** make the pre-capture, P1 actual recomputation, and post sweep recognize `[Oo]rder|[Ss]tep`; state that leading-word case is intentionally case-insensitive; preserve the quotation exception in either spelling; and add a capitalized-citation mutation.

### D4 -- TOML continuation hides a physical multiline block

**Class 1, medium.** RULE 1 forbids `"""` and `'''` blocks (`step-intent-encoding.md:29`), but RULE 2 limits enforcement to the deserialized value (`:31`). A `toml = "0.8"` probe parsed a two-physical-line continuation block as `value="first second" contains_newline=false`. The current validator similarly accepted a current-schema template carrying such a multiline `title`, printing `1 steps, 0 questions, valid`.

The proposed `contains('\n') || contains('\r')` guard therefore cannot distinguish a continuation-escaped multiline `problem` or `approach` from an ordinary single-line value. It violates the physical representation rule and the cited Principle 5 while every specified newline fixture can pass.

**Required correction:** inspect and reject the physical TOML representation before deserialization discards the continuation, with red fixtures for continuation-escaped multiline `problem` and `approach`. If physical representation is not intended to be constrained, remove RULE 1's block prohibition and its physical-line-cost rationale instead.

### D5 -- the post sweep omits the 84 rows

**Class 2, low.** Criterion 1 defines `pre = exempt + drift + rows reading 84`, while criterion 2 says `post = exempt + enumerated NUMBER SURVIVES` (`plan-order-array-position.md:319`, `:371`). The 84 row is neither exempt nor drift and remains in the post sweep.

The current lower-case capture gives `pre=48 exempt=21 drift=26 eightyfour=1`. On the otherwise-correct D3 scratch implementation P1 passes, but the criterion-2 post check gives `post=23 exempt_lost=0` against its specified `21 + 1 = 22`; the unaccounted row is `ledger-order-citation-currency.md:24:order 84`. A correct implementation is refused.

**Required correction:** capture the 84 rows as a separate file and include its count in criterion 2's required `post` relation, alongside `exempt` and the enumerated quotation rows.

### D6 -- increment 3 requires an unchanged generated view in its exact diff

**Class 2, medium.** Criterion 9 requires `docs/plans/agent-scaffold.md` (`step-intent-encoding.md:741`), but the batches own all live `problem`/`approach` edits and regenerate that projection before increment 3; increment 3 forbids touching either value in the plan. The earlier optional-field increment explicitly requires that view not change while no live values exist (`:246`, `:274`), and the batches, not increment 3, own regeneration (`:312`, `:497`). Increment 3's own output-producing template change instead requires `docs/plans/TEMPLATE.md` (`:568`). No described increment-3 edit can alter `agent-scaffold.md` without a forbidden plan edit or a hand edit of the generated view.

**Required correction:** remove `docs/plans/agent-scaffold.md` from criterion 9's must-appear set and list it as must-not-appear with the reason that the batches already produced the final projection. Add `render --check --strict docs/plans/agent-scaffold.plan.toml` to criterion 11 so a hand edit is refused.

### D7 -- out-of-repository criteria cannot locate the binary

**Class 2, low.** Criteria 2 and 3 direct the reader to an empty directory outside the repository but invoke `./target/debug/agent-flow` (`validate-missing-source-exit.md:51-64`); criterion 4's later empty-directory command and criterion 5 repeat it (`:72`, `:80`, `:91`). Run exactly from an empty owned scratch directory, criterion 2 exits 127 with `/bin/bash: ./target/debug/agent-flow: No such file or directory`, not the required exit 1. The command is therefore unable to test a correct implementation.

**Required correction:** bind the built binary to an absolute path in the outcome/fixture convention, and use absolute fixture paths where the command must run outside the repository. Apply the same convention to the analogous outside-repository invocations identified in the other Q-78 sidecars; this raw finding is counted only on its assigned increment.

## Round outcome

All loops are `risky`. This is their first reset-count round, so a clean result starts a streak at one and a `new_valid` result remains at zero.

| Increment | Distinct valid | Severities | Class 1 / class 2 | Outcome | Resulting streak |
| --- | ---: | --- | --- | --- | ---: |
| `sidecar-status-opening-drift-inc1` | 1 | medium | 1 / 0 | new_valid | 0 |
| `ledger-order-citation-currency-inc1` | 1 | medium | 1 / 0 | new_valid | 0 |
| `plan-order-array-position-inc1` | 0 | none | 0 / 0 | clean | 1 |
| `plan-order-array-position-inc2` | 2 | medium, low | 1 / 1 | new_valid | 0 |
| `step-intent-encoding-inc1` | 1 | medium | 1 / 0 | new_valid | 0 |
| `step-intent-encoding-inc2a` | 0 | none | 0 / 0 | clean | 1 |
| `step-intent-encoding-inc2b` | 0 | none | 0 / 0 | clean | 1 |
| `step-intent-encoding-inc2c` | 0 | none | 0 / 0 | clean | 1 |
| `step-intent-encoding-inc2d` | 0 | none | 0 / 0 | clean | 1 |
| `step-intent-encoding-inc2e` | 0 | none | 0 / 0 | clean | 1 |
| `step-intent-encoding-inc2f` | 0 | none | 0 / 0 | clean | 1 |
| `step-intent-encoding-inc3` | 1 | medium | 0 / 1 | clean | 1 |
| `validate-missing-source-exit-inc1` | 1 | low | 0 / 1 | clean | 1 |

**Total distinct valid findings:** 7. **Severity ceiling:** medium. Four loops are `new_valid` because each has a class 1 finding. The three class-2-only loops remain clean because each is at or below the permitted three low-or-medium findings.

No finding was dismissed or accepted as residual risk. In particular, no high or critical dismissal exists, so an independent dismissal re-check is not owed.
