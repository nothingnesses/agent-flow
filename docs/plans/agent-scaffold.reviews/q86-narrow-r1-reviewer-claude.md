# Q-86 narrowed round 1 — reviewer (claude)

Reviewed tip `aec61700` against `main` (`e47fbcb5`), lens: human choice, executability and adoption. I read `AGENTS.md`, `.agents/prompts/reviewer.md`, the Q-86 brief, `Q-86-state-machine.md`, `Q-86-safety-process.md`, the narrowed `Q-86-synthesis.md`, `q86-controller-proof.py`, `q86-q78-scope-replay.sh`, the `[[question]]` entries for Q-86 and Q-88, `agent-scaffold.questions/Q-86.md` and `Q-88.md`, `agent-scaffold.steps/workflow-calibration.md`, `agent-scaffold.success-criteria.md`, the appended `docs/metrics/workflow.jsonl` receipt, the generated `agent-scaffold.md`, the ledger's live Q-86 block, and all five `q86-synthesis-r1..r5` triages. I did not inspect the other reviewer.

**Result: five valid findings — zero critical, zero high, two medium, three low.**

I found nothing at critical or high severity, and that is a positive result rather than an omission. The specific properties I set out to break all hold:

- **The proof gate genuinely blocks implementation.** The blocking selected-option gate is stated in four independent durable records that agree — `Q-86-synthesis.md:182-203`, `agent-scaffold.questions/Q-86.md:23-29`, `agent-scaffold.steps/workflow-calibration.md:26`, and `agent-scaffold.success-criteria.md:41` — and each one makes proof completion an explicit blocker for *every* production implementation unit. I found no path that grants implementation authority: `Q-86-synthesis.md:217` gates the whole migration inventory behind the passing proof, and `:230` forbids implementing an architecture, floor or constant before it.
- **Failure returns to the human, with no automatic fallback.** `Q-86-synthesis.md:201-203` and `Q-86.md:29` both say implementation stays blocked, Q-86 returns to the human, and no fallback architecture *or terminal floor* is automatic. This closes round-1 T10 (`failed-proof fallback pre-authorizes a different architecture`).
- **The recommendation rests only on architecture.** `Q-86-synthesis.md:176-180` names its three supporting and three constraining Principles and states explicitly that it does not rely on the prototype. No zero counter, graph count or replay total is used as its ground.
- **Every constant remains unapproved.** `Q-86-synthesis.md:15,41`, `Q-86.md:41` and the TOML ask all decline architecture, floor and controller constants; every bound in the artefact is qualified `proposed`.
- **The terminal-floor co-decision is explicit and symmetric**, including the `defer` branch's separate receipt requirement (`Q-86-synthesis.md:205-213`).
- **Q-88 is exact.** The appended receipt carries the six option labels in the order Q-88 presents them, `recommendation` and `chosen` both exactly `Narrow the proof scope`, `q_id` `Q-88`, and `task` equal to `folded_into` per the `AGENTS.md:145` convention. `[[question]] Q-88` is `decided` / `folded_into = "workflow-calibration"` / `receipt = "Q-88"`, and the sidecar judges the decision against all eight Principles by name.
- **The generated projection is faithful.** I rebuilt the three changed regions mechanically and they match byte-for-byte (commands under *Projection fidelity* below). `render --check` and `validate --workflow` could not be run here: this container has no `cargo`, `rustc` or `python3` (`which cargo rustc python3` returns nothing), so the executable prototypes were read, not run, and the fidelity check below substitutes for `render --check` on the changed regions only.
- **Every number reproduces.** The authoritative Q-78 selector returns exactly ten passes and `[7,10,5,6,5,5,4,2,1,0]`; A stopping at pass seven leaves `2+1+0 = 3` shortfalls, all `low`; C stopping at pass three leaves `6+5+5+4+2+1+0 = 23`, including the highs at passes four, five and six; the floor-`high` restriction does apply on passes three through six; the "nineteen" false-clean records count is 19; six of ten Q-78 triage files remain. The B algebra is internally consistent (`sum(4n_q+1)` over `m+1` phases `= 4|O|+m+1`, `+7 = 4|O|+m+8`; `sum(n_q+1) = |O|+m+1`; `I_B` decomposes as `34` plan-review calls plus `4(4|O|+m+1) + 2|O| = 18|O|+4m+4`).
- **Round-5 T8 and T9 are closed.** The superseded exact graph counts are gone from `Q-86-state-machine.md`, and `n_a` no longer occurs anywhere in the tree.
- **The ledger is not stale.** Round-1 T12's correction is an integration action, and on `main` the resume anchor still correctly reads Q-86 `exploring` (the status change is on this branch, not on `main`) while forwarding to a Q-86 block that already records Q-88, the narrowing and narrowed round 1. I re-raise nothing there.

The two medium findings below are both **regressions of repairs that were already applied and are visible in the branch's own history**: the narrowing rewrite at `e8cc8ba1` replaced the synthesis wholesale and dropped two corrections that commits `c37f4564`..`d24cf02b` had landed for settled round-1 and round-2 verdicts. That is the specific failure mode a wholesale rewrite invites, and it is why I checked the pre-narrowing text rather than only the current tip.

---

## NR1C-1 (medium). The narrowed artefact's own no-change sentence is false, and re-breaks the applied repair for round-2 T10

**Evidence.** `Q-86-synthesis.md:7` ends:

> No current workflow rule, cap, reset behaviour, acceptance rule, metric, specification, pack file, prompt, template, README, changelog, **generated plan**, or Rust source changes in this pass.

Both italicised classes change in this pass:

```sh
git diff --name-only main...HEAD -- docs/metrics/workflow.jsonl docs/plans/agent-scaffold.md
# docs/metrics/workflow.jsonl
# docs/plans/agent-scaffold.md
git log --oneline main..HEAD -- docs/metrics/workflow.jsonl
# e8cc8ba1 docs: narrow Q-86 proof scope
```

`e8cc8ba1` — the commit that writes this very sentence — appends the Q-88 decision receipt to `docs/metrics/workflow.jsonl`, and `aec61700` rewrites `docs/plans/agent-scaffold.md`.

This is a regression, not a new slip. Round-2 T10 (`q86-synthesis-r2-triage.md:94-100`, valid, low) found the same false clause and gave the exact correction "say that it changes no generated-plan content beyond the required projection of the Q-86 source edits, or omit 'generated plan' from the list". That correction was applied and held for three commits:

```sh
git show d24cf02b:docs/plans/workflow-calibration.explorations/Q-86-synthesis.md | sed -n 5p
# ... It changes no workflow rule, cap, reset behaviour, metric, specification, pack file, prompt,
#     template, README, changelog, or Rust source. It changes generated-plan content only through
#     the separately required projection of the Q-86 planning sources.
sed -n 7p docs/plans/workflow-calibration.explorations/Q-86-synthesis.md
# ... changelog, generated plan, or Rust source changes in this pass.
```

The narrowing rewrite restored the pre-repair wording and extended it: `metric` was accurate at `d24cf02b` (that commit touched no metrics) and is inaccurate now.

**Consequence.** This sentence is the decision-boundary statement a human reads to answer "what did this pass actually touch?" before deciding. It denies the existence of the Q-88 decision receipt, which under *Structured data first, project for humans* is the structured source of the very decision authorising this artefact — `Q-88.md:36` and the plan both call that receipt the source while the synthesis says no metric changed. An auditor taking the sentence at face value would not look for the receipt that makes the human-input contract auditable. Severity is above round-2 T10's `low` because the false clause now also covers the receipt, and because a settled correction silently regressing is worse than the original slip.

**Correction.** Restore the `d24cf02b:5` form and extend it to the receipt: state that the pass changes no workflow rule, cap, reset behaviour, acceptance rule, specification, pack file, prompt, template, README, changelog or Rust source; that it appends exactly one `type:"decision"` `q_id:"Q-88"` metrics record and changes no other metric; and that it changes generated-plan content only through the required projection of the Q-86 and Q-88 planning sources. Note that `Q-86-synthesis.md:219` ("changes planning and prototype-status records only") is already correct and does not need changing.

## NR1C-2 (medium). The narrowing orphans both explorer proposals and drops the round-1 T16 label map, leaving a live competing recommendation reachable with three colliding label systems

**Evidence.** The narrowed synthesis never names either proposal:

```sh
grep -c "state-machine\|safety-process\|Candidate" docs/plans/workflow-calibration.explorations/Q-86-synthesis.md
# 0
```

Neither does `Q-86.md`, the `[[question]] Q-86` ask, or `agent-scaffold.steps/workflow-calibration.md` — those name only the synthesis and the two scripts. The pre-narrowing synthesis carried both the pointer and an explicit map:

```sh
git show d24cf02b:docs/plans/workflow-calibration.explorations/Q-86-synthesis.md | sed -n 5p\;13p
# :5  This synthesis reconciles the corrected proofs in `Q-86-state-machine.md` and `Q-86-safety-process.md`.
# :13 The source labels map as follows. Option A is the state-machine proposal's Candidate A and the
#     safety proposal's M1. Option B is the safety proposal's corrected M2 plus the state-machine
#     proposal's sealed authority envelope. Option C is the state-machine proposal's Candidate B.
#     The safety proposal's M3 remains excluded.
```

Line 13 was the applied repair for round-1 T16 (`q86-synthesis-r1-triage.md:139-145`, valid, low). Commit `e8cc8ba1` removed the pointer and the map together.

Three label systems are still live in the tree, and the proposals' `## Prototype status` quarantine sections do not reach them — those sections quarantine only proof, exhaustiveness and zero-violation claims:

- `Q-86-synthesis.md`: Option `A` / `B` / `C`.
- `Q-86-state-machine.md:9-12`: Candidate A (= Option A) and Candidate B (= **Option C**), with a live recommendation at `:16` — "The recommendation is Candidate A. The later human decision remains required."
- `Q-86-safety-process.md:310,322,348`: M1 (= Option A), M2 (= Option B), M3 (excluded); `:476` recommends M2, consistent with the synthesis.

**Consequence.** The human is asked to choose one of three architectures, and the artefact that asks them does not point at the two documents where those architectures are actually specified — the detail behind the recommended Option B lives in `Q-86-safety-process.md` §5 and is reachable only by directory browsing or ledger archaeology. A human who does browse the directory meets `Q-86-state-machine.md:16` recommending "Candidate A", which without the map reads as a second, contradictory recommendation for Option A, while its "Candidate B" silently means Option C. Round 1 rated this `low` when the pointer existed and only the map was missing; losing both, with a live competing recommendation on the other side, makes it a real risk of choosing under a misapprehension, and it also risks the later proof-of-concept unit being commissioned against the wrong source document.

**Correction.** Either restore the pointer and the `d24cf02b:13` label map to the narrowed synthesis (preferred: the proposals remain decision inputs), or, if the intent is that the synthesis is now the sole decision artefact and the proposals are historical, extend `Q-86-state-machine.md`'s `## Prototype status` section to mark its `:16` Candidate-A recommendation superseded by the synthesis in the same way its proof claims were marked historical. Whichever is chosen, the three label systems need one mapping sentence in the artefact the human is directed to.

## NR1C-3 (low). The Q-88 sidecar injects a second document-level H1 into the generated plan

**Evidence.** `docs/plans/agent-scaffold.questions/Q-88.md:1` is `# Q-88: narrow the Q-86 proof scope at the review cap`. `question_details_section` inlines each question sidecar verbatim (`src/plan/render.rs:591-602`), so that H1 lands in the generated plan:

```sh
# every H1 outside a fenced code block (the plan's other `# ` lines are shell comments in fences)
awk '/^```/{f=!f; next} !f && /^# /{print FNR": "$0}' docs/plans/agent-scaffold.md
# 3: # agent-scaffold plan
# 5114: # Q-88: narrow the Q-86 proof scope at the review cap
```

(`sed -n 5108,5116p docs/plans/agent-scaffold.md` shows 5114 as ordinary prose, between the Q-86 body and `## Decision`.) The two other non-empty question sidecars carry no heading at all — `Q-78.md:1` and `Q-86.md:1` both open with prose — and step sidecars open at `###` (`render.rs:569-571`).

**Consequence.** The generated plan's title is its only H1. A second one at 5114 outranks the `## Question Details` heading it sits under, so every heading-derived outline or table of contents nests the remainder of the document — including `## Success Criteria` at 5155 — beneath "Q-88: narrow the Q-86 proof scope at the review cap". This is presentation only: `src/plan.rs:140-165` ends a `## ` section at the next `## ` and is not confused by a `# `, and this repo is TOML-primary so the generated view is not parsed. It is nonetheless a structural inconsistency introduced into a generated file by a hand-authored sidecar that departs from the convention its two siblings follow.

**Correction.** Demote the Q-88 sidecar's first line to `## Q-88: narrow the Q-86 proof scope at the review cap` (its own subsections are already `##`, so they would then need demoting to `###`), or drop the title line as `Q-78.md` and `Q-86.md` do. Re-render and run `render --check`.

## NR1C-4 (low). The C column of the cost table is underivable from the narrowed artefact

**Evidence.** The only reviewer-per-batch rate the narrowed synthesis states is two: `:85` prices A's maximum "with two reviewer calls ... per phase" per batch, `:154` gives one batch as two calls, `:155` gives A two batches as four calls, and `:154-156` price B's `n_q + 1` batches at `2(n_q + 1)` calls. The C column breaks that rate without explanation:

```sh
grep -nE "reviewer call" docs/plans/workflow-calibration.explorations/Q-86-synthesis.md
# 85  With two reviewer calls, at most one triage, ...
# 155 | Risky plan or work phase | Two batches and four reviewer calls | ... | Two batches and three reviewer calls |
# 156 | Acceptance phase | One batch and two reviewer calls | ... | Two batches and three reviewer calls |
grep -niE "one reviewer|single reviewer" docs/plans/workflow-calibration.explorations/Q-86-synthesis.md
# (no output)
```

The pre-narrowing synthesis derived the figure explicitly, and `e8cc8ba1` dropped that sentence:

```sh
git show d24cf02b:docs/plans/workflow-calibration.explorations/Q-86-synthesis.md | sed -n 210p
# ... A risky plan or work phase and acceptance require at least discovery plus blind closure,
#     two batches and three reviewer calls. ...
```

**Consequence.** The number is still correct under C's design — discovery at two reviewers plus a single-reviewer blind-closure batch — but the narrowed artefact never says the blind-closure batch takes one reviewer, so a human cannot reconstruct `3` from the text. Applying the artefact's own stated rate gives `4`, so C appears to enjoy an unexplained 25 percent minimum-cost advantage over A on the risky and acceptance rows, in the table the human uses to compare ordinary running cost. Round-2 T6 established that omitting minimum ordinary review cost from the decision comparison is a defect; here the figure survived and its basis did not.

**Correction.** Restore one sentence to the Option C section stating that a risky or acceptance phase minimum is discovery plus a single-reviewer blind-closure batch, hence two batches and three reviewer calls, or annotate the C column of the table with the same.

## NR1C-5 (low). The reclassified scripts carry no in-file prototype caveat, unlike the two proposals

**Evidence.** This pass reclassified both scripts as adversarial prototypes and warned specifically against reading their counters as proof (`Q-86-synthesis.md:41-56`; `Q-86.md:20`: "No human-facing decision should treat the prototype's exact graph counts, zero-valued controls, or conditional replay totals as proof"). It gave both proposal documents an explicit quarantine section for exactly that reason (`Q-86-state-machine.md:3-5`, `Q-86-safety-process.md:3-5`). The scripts themselves received nothing:

```sh
grep -c "^#" docs/plans/workflow-calibration.explorations/q86-controller-proof.py
# 1                      (the shebang; the file has no docstring and no comments)
grep -niE "prototype|not a proof|limitation|caveat|adversarial" \
  docs/plans/workflow-calibration.explorations/q86-controller-proof.py \
  docs/plans/workflow-calibration.explorations/q86-q78-scope-replay.sh
# (no output)
```

The file is named `q86-controller-proof.py`, and its reporting lines print all-zero red-control counters (`:1258`, `:1315`, `:1365`, `:1414`, `:1474` emit `bad_delivery=%d bad_unverified_delivery=%d bad_critical_clear=%d bad_bound=%d ...`).

**Consequence.** The narrowing's central claim is that these two artefacts are not proofs. Every document that points at them now says so, but the artefacts a reader is most likely to open or run say nothing: a file called `-proof` that prints a wall of `bad_*=0` counters is precisely the "zero counters as proof" reading the decision material forbids, and the future proof-of-concept author is the reader most likely to start there. Severity is low because the documents are covered and the gap is only reached by opening or running the scripts directly.

**Correction.** Add a short header comment to both scripts — a docstring in the Python file, a comment block in the shell script — stating that they are adversarial prototypes retained as evidence, that their zero-valued controls and counts are not recommendation-eligibility or safety proof, and pointing at `docs/plans/agent-scaffold.reviews/q86-synthesis-r5-triage.md` and `Q-86-synthesis.md`'s prototype boundary. Renaming the file is not required and would break the citations in five triages.

---

## Projection fidelity

The three changed regions of the generated plan were rebuilt from source and compared. All three match, so no hand-edit or stale-render defect is present in this change (this substitutes for `render --check`, which cannot run here; it does not certify the unchanged regions):

```sh
# Q-86 queue line == "- `Q-86` (open) " + one_line(ask)   [render.rs:434-445, 555-557]
# differs only by the trailing newline of the constructed file.

# Question Details == Q-78.md + Q-86.md + Q-88.md, trailing-blank-trimmed, joined by a blank line
awk '/^## Question Details$/{f=1;next} /^## Success Criteria$/{f=0} f' docs/plans/agent-scaffold.md \
  | awk 'BEGIN{s=0}{if(!s&&$0=="")next;s=1;a[++n]=$0}END{while(n>0&&a[n]=="")n--;for(i=1;i<=n;i++)print a[i]}' > /tmp/qd_actual.txt
for f in Q-78 Q-86 Q-88; do
  awk '{a[NR]=$0}END{n=NR;while(n>0&&a[n]~/^[[:space:]]*$/)n--;for(i=1;i<=n;i++)print a[i]}' docs/plans/agent-scaffold.questions/$f.md; echo;
done | head -n -1 > /tmp/qd_bodies.txt
diff /tmp/qd_bodies.txt /tmp/qd_actual.txt          # QUESTION DETAILS: FAITHFUL

# workflow-calibration Step Detail == its sidecar; Success Criteria section == its sidecar
#   STEP DETAIL: FAITHFUL / SUCCESS CRITERIA: FAITHFUL
```

The derived header count is also consistent: `3` `open` plus `4` `exploring` equals the rendered "7 open questions", and 88 `[[question]]` entries match the ledger's count.

## Evidence checks that passed

```sh
jq -s 'map(select(.type=="round" and .task=="q78-design-pass" and .phase=="acceptance"))
       | {passes: length, valid_shortfalls: map(.valid_findings)}' docs/metrics/workflow.jsonl
# {"passes":10,"valid_shortfalls":[7,10,5,6,5,5,4,2,1,0]}          matches Q-86-synthesis.md:29

jq -c 'select(.type=="round" and .task=="q78-design-pass" and .phase=="acceptance") | .severities' \
   docs/metrics/workflow.jsonl
# passes 3-6 carry the highs -> ":209" ("passes three through six") holds;
# passes 8-9 are ["low","low"] and ["low"] -> ":95" ("three later low shortfalls") holds;
# passes 4-10 sum to 23 including highs -> ":148" holds.

jq -s '[.[]|select(.type=="round" and .outcome=="clean" and (.valid_findings//0)>0
       and (.consecutive_clean//0)>0)] | length' docs/metrics/workflow.jsonl
# 19                                                               matches ":35"

ls docs/plans/agent-scaffold.reviews/ | grep -c q78
# 6                                                                matches ":35"

jq -c 'select(.type=="decision" and .q_id=="Q-88")' docs/metrics/workflow.jsonl
# options are the six Q-88 labels in order; recommendation == chosen == "Narrow the proof scope";
# chosen is a member of options; task == folded_into per AGENTS.md:145.

grep -rn "n_a\|809/949\|1386/1648\|794/863\|659/711" docs/plans/workflow-calibration.explorations/
# (no output)                                          round-5 T8 and T9 are closed.
```

## Traceability spot-check of the proof gate

`Q-86-synthesis.md:197` makes the traceability matrix cover every valid verdict in all five triages, with a controlled escape (`inapplicable` needs a cited architecture-specific reason) and a durable-text rule for planning and documentation findings, so coverage is total by construction. I sampled it against the 51 valid verdicts (13 + 12 + 9 + 8 + 9) and every one is either repaired in the current text or reachable through gate items 1-12; I found no valid finding that the gate silently drops. Round-5 T3's extra requirement — that the floor consequence of carried serious findings appear "in the Q-86 decision material rather than leaving it to an implementer" — is met at `:69` and gate item 4, not merely deferred.
