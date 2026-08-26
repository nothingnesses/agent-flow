# Q-78 acceptance pass 7, adoption and executability lens (Claude)

Reviewed artifact: branch `review/q78-acceptance-r7-claude` at `ecc342e5`, whose product content is the pass-6 planner repair `11e129ed` plus the Q-85/Q-86 scheduling fold `222fba5a` and their ancestors. Baseline `main` at merge-base `332fb5c2`, 104 changed files, all under `docs/` (`git diff --name-only 332fb5c2..HEAD | grep -v '^docs/'` returns nothing), so the product under acceptance is the planning artefact, not code. Lens: does the pass-6 repair close its five dispositions, do Q-85 and Q-86 equip a later explorer, and can a fresh implementer execute what the plan now says against this repository's own committed log.

## Verification actually performed

THIS PASS RAN THE FULL GATE SET, INCLUDING THE TWO FAMILIES PASSES 3 THROUGH 6 COULD NOT RUN. Those passes recorded that `cargo test` and `cargo clippy` were unavailable because no crate sources were present offline. Network access is available in this container, so I fetched the dependency set against the committed `Cargo.lock` and built the binary from HEAD myself rather than adopting a pre-existing store binary. Toolchain: `cargo 1.95.0` / `rustc 1.95.0` from `/nix/store/9l9lclxjw8ns5q4k13lxld7pl90paa3g-rust-mixed/bin`, with `cc` supplied by `/nix/store/3d1c302vw7kc8a5vknhmn34c0pd7zm6m-gcc-wrapper-15.3.0/bin` (bare `cargo` fails with `linker 'cc' not found`). `CARGO_HOME` and `CARGO_TARGET_DIR` both point inside the authorised scratch mount, so no build artefact and no registry cache reached the reviewed tree; `git status --porcelain` is empty at the end of this review and no `target/` exists in the worktree. All gates run from the repository root.

- `cargo fetch --locked`: exit 0.
- `cargo test --locked --offline`: exit 0. 470 passed, 0 failed, 0 ignored across 12 suites.
- `cargo clippy --all-targets --locked --offline -- -D warnings`: exit 0.
- `validate --source docs/plans/agent-scaffold.plan.toml`: exit 0, `472 records, valid`, `114 steps, 86 questions, valid`.
- `validate --workflow --source docs/plans/agent-scaffold.plan.toml`: exit 0, `workflow invariants hold`.
- `render --check --strict docs/plans/agent-scaffold.plan.toml`: exit 0, `up to date`.
- `agent-flow checks` through a scratch-only `PATH` shim: `1 passed, 0 failed, 0 skipped`.
- `git diff --check` and `git diff --check 332fb5c2..HEAD`: exit 0.
- ASCII: `LC_ALL=C grep -cP '[^\t\x20-\x7e]'` sums to 0 over all 104 files changed since the merge-base.

THE BINARY IS HEAD'S OWN, so the parser and checker results above are not adopted on trust: `$CARGO_TARGET_DIR/debug/agent-flow` reports `agent-flow 0.0.4` and was compiled from this worktree in the same invocation that produced the passing test suite.

ONE ASCII OBSERVATION THAT IS NOT A SHORTFALL. `LC_ALL=C git grep -lP '[^\t\x20-\x7e]'` returns 13 tracked files, all transient findings and triage records under `docs/plans/agent-scaffold.reviews/`. Every one was added before the merge-base (verified with `git log --diff-filter=A` plus `git merge-base --is-ancestor`), none is in this branch's diff, and all are scheduled for commit-before-delete cleanup at task close. No product file carries a non-ASCII byte.

Everything below is reproduced with GNU grep, `awk`, `jq`, `sed`, `sha256sum`, `git` and `curl`. All copies and mutations stayed inside the authorised scratch mount; no worktree was created, pruned or removed.

## The six pass-6 dispositions

### R6-G1 (`high`, the thirteen Q-81 identities could not hold both a preserved plan-review history and a live delivery declaration): CLOSED

`structured-risk-class-source.md:26` adds a migration-only `[[step.historical_increment_plan_review]]` row type that parses as `HistoricalRoadmapIncrementPlanReview` rather than `LoopDeclaration` and "cannot be selected, reopened, inherited, waived, used for W3 delivery convergence, or fed into live foreclosure/cap", while `:30` keeps the thirteen existing `[[step.increment]]` ids and classes byte-exact and gives them `phase = "work_review"`. `:18` states the two namespaces explicitly: "The same lexical `(step, increment)` may appear in a closed, selector-bounded Q-81 plan-review history and a live work-review declaration, but no declaration carries two phases and no event can cross between them."

I reproduced the population rather than reading the claim. Records 387-430 contain exactly 41 `plan_review` rounds over exactly the thirteen ids `:28` lists, with the ordinal map matching row for row (`sidecar-status-opening-drift-inc1` 387/400/413/418; `ledger-order-citation-currency-inc1` 388/401/414; `plan-order-array-position-inc1` 389/402; `-inc2` 390/403/415; `step-intent-encoding-inc1` 391/404/416/419/423/425/427/428/430; `inc2a` through `inc2f` two rounds each at 392-397/405-410; `step-intent-encoding-inc3` 398/411/417/420/424/426; `validate-missing-source-exit-inc1` 399/412). Every one snapshots `risky`, as `:28` asserts. The only three non-round lines in 387-430 are the escalations at 421, 422 and 429, matching `:20`. All thirteen ids are still declared as live `[[step.increment]]` entries in the TOML.

### A (`medium`, three plan-review identities had no authorised declaration route): CLOSED

All three routes now exist in the committed source. `decision-folder-currency-fold` is declared as a second `[[step.increment]]` under `decision-folder-currency` at `agent-scaffold.plan.toml:1265` with `risk_class = "low_risk"`, matching the observed class of its five rounds (records 210-214, all `low_risk`, peak `consecutive_clean` 1). `q77-fold` and `step-intent-fold` are now in `[meta].orphan_tasks` (`agent-scaffold.plan.toml:5-27`), so `:12`'s requirement that a `[[task_loop]]`'s `task` "must equal `[meta].title` or resolve through `[meta].orphan_tasks`" is satisfiable for both.

The whole partition the criterion states reproduces exactly. Using the tool's own join (a round's step is its structured `step` id else `task` with a trailing `-inc<alnum>` stripped; its increment is its structured `increment` id else the full `task`): 99 `plan_review` records total; 63 Roadmap-resolving over exactly 18 identities; 36 non-Roadmap over exactly 14 task identities. The 63 partition as seven exact-step records (`checks-runner-worktree-name-collision` 4, `structured-skeleton` 3), 41 Q-81 records, and 15 on the three live plan-review increment declarations (`decision-folder-currency-fold` 5, `workflow-enforcement-tier-fold` 5, `workflow-enforcement-tier-endproperty-fold` 5). The record ids criterion 5 pins for the two newly registered tasks reproduce byte for byte: `q77-fold` at 358/361/362/364 and `step-intent-fold` at 368/369/370/373/374/376, all `low_risk`. The eight unowned `work_review` records reproduce at 1, 47, 48, 164, 173, 177, 178 and 379 over seven distinct tasks, all `low_risk`, matching `:38`.

All 15 digest pins reproduce. `sed -n "${n}p" docs/metrics/workflow.jsonl | tr -d '\n' | sha256sum` matches `:34` for records 98, 99, 115, 217, 219, 220 and 221, and matches `:38` for records 1, 47, 48, 164, 173, 177, 178 and 379.

### B (`low`, the 45/36/28/19 drift measurement was stale): CLOSED AT `11e129ed`, RE-OPENED AT `222fba5a`

The repair did what the pass-6 triage asked: it remeasured, named `workflow-driver` as the moved member, and re-put the changed premise through the decision path as Q-84. Run at `11e129ed` the sidecar's own commands print exactly `relaxed=44 anchored=35 strip-relaxed=27 strip-anchored=18`, so the repair's figures were correct when authored.

They are no longer correct at HEAD. See findings A and B below.

### R6-G2 (`low`, stale Stage-3 guidance in the retained architecture note): CLOSED

All three cited sites now carry an explicit pre-Q-82 supersession and bound the surviving gates to Stages 4-6. `r2-architecture-build-path.md:239` reads "PRE-Q-82 ORDERING HISTORY ... The current scheduled path is `0a -> 0b -> 1 -> 2 -> 3`; only Stages 4 through 6 remain gated"; `:253` reads "PRE-Q-82, the near-term path stopped at 0a/0b/1/2 and called the scheduler gated. Q-82 superseded that part"; `:264` reads "PRE-Q-82 RECOMMENDATION HISTORY ... Q-82 supersedes only the Stage-3 hold." The two gates the triage required to survive are preserved verbatim at each site: the Stage-5 write path behind measured advisory adoption plus reopening Q-24, and Stage-6 authoritative driving behind a measured-low override rate. `:281`'s YAGNI list carries the same bound.

### R6-G3 (`low`, the ledger's duplicated queue inventory omitted Q-83): CLOSED

`agent-scaffold.ledger.md:551` now replaces the inventory with a pointer: "THE STRUCTURED OPEN-QUESTIONS QUEUE IS AUTHORITATIVE. Do not restate its moving membership here. Read the branch's `[[question]]` entries or project them with `agent-flow status --source docs/plans/agent-scaffold.plan.toml --json`". I ran that command against the HEAD-built binary: it exits 0 and `.plan.open_questions` carries all 86 items, including Q-80 through Q-86 with their current statuses (Q-86 `exploring`, the rest `decided -> folded into <slug>`). The generated Status line's "8 open questions" also reproduces from that projection (Q-44, Q-56, Q-58, Q-68, Q-69, Q-78, Q-79, Q-86).

### Q-84: RECORDED CORRECTLY, PREMISE NOW FALSIFIED BY THE BRANCH ITSELF

The receipt exists and is well formed: `{"type":"decision","task":"sidecar-status-opening-drift","q_id":"Q-84","options":["Continue with the measured set of 18","Retain the original set of 19","Reopen the drift design"],"recommendation":"Continue with the measured set of 18","chosen":"Continue with the measured set of 18","ts":"2026-08-26"}` at record 471, with `chosen` a member of `options`. The `[[question]]` carries `status = "decided"`, `folded_into = "sidecar-status-opening-drift"`, `receipt = "Q-84"`, and the owning step carries `[step.provenance] decisions = ["Q-84"]`, which `render` projects into the Roadmap Notes cell as `why: decisions Q-84; commits e8b2992, 5ca89bb`. The mechanics are right. The measured premise is not; see findings A and B.

## Q-85 and Q-86: SUFFICIENT, ACCURATE, AND BOUNDED

This is the cleanest part of the branch and I could not falsify it.

THE DECISION BOUNDARY IS EXPLICIT AND HELD IN THREE PLACES. `Q-86-convergence-mechanism-brief.md:5` states that Q-85 "decided only where this investigation belongs" and "did not select a convergence mechanism", `:7` enumerates what the fold does not change (the five-round per-artifact cap, the reset-after-human-resume branch, the single-pass acceptance rule, any convergence constant, any Roadmap status, any existing review identity), and `:91` forbids inferring approval from Q-85. The same boundary is repeated in the `[[question]]` Q-86 ask and at `workflow-calibration.md:20`. Q-86 is `exploring` with no `folded_into` and no receipt, which is the correct shape for an owed design pass.

THE LOCAL EVIDENCE IS REPRODUCIBLE AND THE BRIEF PREFERS THE SELECTOR TO THE COPIED COUNT. `:28`'s command returns `{"passes": 6, "valid_shortfalls": [7,10,5,6,5,5]}` exactly as `:31` states, and `:31` names the selector as the authority "if the log grows" rather than freezing the list. Every cited adjudication file exists (`q78-acceptance-triage.md` and `q78-acceptance-r2-triage.md` through `-r6-triage.md`), as do both retained calibration records at `:35`.

THE EXTERNAL EVIDENCE IS CHARACTERISED ACCURATELY. I fetched both primary sources rather than trusting the summary. The gist's setup table gives R1 an informed brief ("files + a list of 7 claimed properties to verify"), R3 an informed brief ("files + a description of all 9 changes made in R2"), and R5 "**files only** - no history, no claims, no changelog"; its section 3 table reads `R1 (informed) | 10`, `R3 (informed, given change list) | 12`, `R5 (blind) | **17**` with `~6` defects present during R3 that the informed reviews missed. That is exactly what `:45` and `:47` state. `:47`'s hedges also reproduce: the gist calls the anchoring result "the strongest single result of the experiment" at its section 5.5 and separately records "n = 1. One artifact, one domain, one session, three review rounds" and "Scope was uncontrolled - the single largest confound". The article page confirms the "perfect, non-trivial" prompt that `:49` names as a confound. The brief's derived instruction, "price blind artifact-wide discovery separately from informed fix verification rather than treating either allocation as universally superior", follows from both halves rather than from the headline alone.

THE DESIGN SPACE IS BOUNDED WITHOUT BEING DECIDED. `:53-79` require a non-resettable task-level budget as an explicit alternative to the current resettable windows, define four finding lineages, require a scope firewall that cannot relabel an in-scope defect as optional, and require terminal human choices at exhaustion. `:71` carries the invariant the human asked for: "No budget may conceal an unresolved `critical` finding." `:85-91` require more than one viable mechanism including the current one as baseline, trade-offs against all eight Project Principles by name (I checked the eight names against the `[[principle]]` rows; they match exactly and in order), falsifiable stopping properties with red controls, a YAGNI boundary, and a later human decision through the contract. `:95` forbids mutating the live log, statuses, identities, spec, pack or code during the investigation.

Criterion 41 of the Success Criteria is met on every clause except the receipt clause; see finding C.

## Shortfalls

### A. `medium` - the Q-85/Q-86 fold authored a corrected status label, which is the form the human rejected, in the file the plan schedules two steps to clean

`docs/plans/agent-scaffold.steps/workflow-calibration.md:3` opens `In progress.` at HEAD. Commit `222fba5a` authored that opening; at `222fba5a~1` the same line read `Not started (deferred).`

THE RULE THIS BREAKS IS A RECORDED HUMAN DECISION, NOT A REVIEWER PREFERENCE. `Q-78-statusform` (record 372; receipt `{"q_id":"Q-78-statusform","options":["Delete the token, record the 24","Keep the label, name the exclusion","Keep the label, route to Q-78","Delete the justification prose"],"chosen":"Delete the token, record the 24"}`) chose deletion over both keep-the-label options. `sidecar-status-opening-drift.md:13` records the reasoning the human accepted: "A replacement restores hand-maintained copies of a field the TOML owns, which is the mechanism that produced this drift in the first place." `:15` extends it to the widened set in one sentence: "the widened files get the same deletion, not a corrected label." `:5` forecloses the accuracy defence in advance: "the DUPLICATION is the defect, independent of whether the copy currently happens to be right, and writing accurate labels would not close the class."

IT ALSO CONTRADICTS THE PLAN'S OWN LIVE RULE, which that step exists to make true. `docs/plans/agent-scaffold.documentation-protocol.md:5`, rendered at `docs/plans/agent-scaffold.md:26`, ends: "The Step Details below carry each step's design, decisions, and (once done) outcome and evidence, and do not repeat the status label." The drift sidecar quotes that sentence as its governing fact in its own opening paragraph. `workflow-calibration.md:3` is a fresh violation of it, rendered into `docs/plans/agent-scaffold.md:701`.

THE BRANCH ITSELF SHOWS THE CORRECT DISPOSITION ONE FILE OVER. `workflow-driver.md`'s opening was a status-labelled stale sentence until commit `4ac0677c`, which replaced it with "The umbrella carries a delivered foundation and scheduled successors" - token-free, so it left the selector entirely and needed no successor work. `sidecar-status-opening-drift.md:28` records that as the model outcome. The Q-85/Q-86 fold had the same opportunity on the same kind of file and took the opposite route.

THE INSTRUCTION CAME FROM THE FOLD BRIEF, so the repair should reach the brief pattern and not only the file: `docs/plans/agent-scaffold.reviews/convergence-investigation-fold-brief.md` says "Correct the `workflow-calibration` sidecar's stale status wording against the TOML while preserving completed historical records." That directive is what a planner executed.

WHY THIS IS A SHORTFALL AND NOT A NIT. Three measured consequences follow, and none of them is cosmetic. First, the plan now carries one more hand-maintained copy of a field the TOML owns, created after the human ruled that form out, so the next status change on `workflow-calibration` reproduces the exact drift class the step exists to end. Second, it silently moved the file between two steps' worklists: `comm -23 anchored.txt handover.txt` at HEAD puts `workflow-calibration` in `sidecar-status-opening-drift`'s own 18-member mechanical worklist, whereas at `11e129ed` it was in the successor step's 17-member handover, so ownership of that file changed with no decision and no record. Third, it is the direct cause of finding B. It is `medium` rather than `high` because the dynamic selectors remain the implementation authority, so both steps still execute correctly against whatever they measure at their own base; and it is `medium` rather than `low` because it contradicts a recorded human decision rather than merely going stale.

SMALLEST SAFE DISPOSITION. Replace `workflow-calibration.md:3`'s leading `In progress.` with a token-free opening in the shape `workflow-driver.md` already uses, or restore the pre-fold opening and leave the file to `sidecar-status-authored-openings`, whichever the human prefers; then correct the fold-brief pattern so a later planner fold is not told to correct a status label again.

### B. `low` - four live plan sites and the ledger state a handover size the plan's own reproduction commands contradict

`sidecar-status-opening-drift.md:19` says "Reproduce the current four figures with the commands under ACCEPTANCE below", and `:21-24` state 44 relaxed selections, 35 anchored selections, 27 relaxed stripped openings and "18 anchored handover openings. THE CURRENT AUTHORED-REPLACEMENT POPULATION IS 18."

MEASURED AT HEAD, using criterion 1's anchored selector (`:130-131`), criterion 12's relaxed selector (`:142-143`) and the H1 script transcribed verbatim from `:172-187`, the commands print `relaxed=44 anchored=35 strip-relaxed=26 strip-anchored=17`. Two of the four figures are wrong. Reproduce with:

```
#!/usr/bin/env bash
# Run from the repository root; pass a scratch directory.
set -u
S="$1"; mkdir -p "$S"
ANCH='^(Not started|In progress|Complete|Skipped|Next|Optional|Deferred)([.;,:]|$| \(| (and|by|but|or|nor|for|so|yet|until|unless|pending|while|after|before|because|since|though|although|then|with|without|on|in|at|to|from|as|per)\b)'
RELAX='^(Not started|In progress|Complete|Skipped|Next|Optional|Deferred)([.;,: ]|$)'
sed -n 's/^| `\([a-z0-9-]*\)` | \([a-z ]*\) |.*/\1/p' docs/plans/agent-scaffold.md > "$S/slugs.txt"
: > "$S/anchored.txt"; : > "$S/relaxed.txt"
while read -r slug; do
  line=$(sed -e '/^#/d' -e '/^[[:space:]]*$/d' "docs/plans/agent-scaffold.steps/$slug.md" | head -1)
  t=$(printf '%s' "$line" | grep -oE "$ANCH" | grep -oE '^(Not started|In progress|Complete|Skipped|Next|Optional|Deferred)')
  [ -n "$t" ] && printf '%s\t%s\n' "$slug" "$t" >> "$S/anchored.txt"
  printf '%s' "$line" | grep -qE "$RELAX" && printf '%s\tx\n' "$slug" >> "$S/relaxed.txt"
done < "$S/slugs.txt"
h1() { SELECTED="$1"; COPY="$2"
  cp -r docs/plans/agent-scaffold.steps "$COPY"
  while IFS=$'\t' read -r slug token; do
    n=$(grep -nvE '^#|^[[:space:]]*$' "$COPY/$slug.md" | head -1 | cut -d: -f1)
    sed -i "${n}s/^\(Not started\|In progress\|Complete\|Skipped\|Next\|Optional\|Deferred\)[.;,:]\{0,1\}[[:space:]]*//" "$COPY/$slug.md"
  done < "$SELECTED"
  while IFS=$'\t' read -r slug token; do
    line=$(sed -e '/^#/d' -e '/^[[:space:]]*$/d' "$COPY/$slug.md" | head -1)
    case "$line" in [A-Z]*|'`'*) ;; *) printf '%s\t%s\n' "$slug" "$(printf '%s' "$line" | cut -c1-46)" ;; esac
  done < "$SELECTED"
}
rm -rf "$S/ca" "$S/cr"
h1 "$S/anchored.txt" "$S/ca" > "$S/handover.txt"
h1 "$S/relaxed.txt"  "$S/cr" > "$S/handover-relaxed.txt"
printf 'relaxed=%s anchored=%s strip-relaxed=%s strip-anchored=%s\n' \
  "$(wc -l < "$S/relaxed.txt")" "$(wc -l < "$S/anchored.txt")" \
  "$(wc -l < "$S/handover-relaxed.txt")" "$(wc -l < "$S/handover.txt")"
```

THE CAUSE IS BOUNDED TO ONE FILE AND ONE COMMIT, which distinguishes this from the pass-6 finding and is the new evidence that justifies raising it again. Running the same script against trees extracted per commit gives `11e129ed -> 44/35/27/18`, `222fba5a -> 44/35/26/17`, `HEAD -> 44/35/26/17`, and `comm -3` over the two handover lists names exactly one moved member, `workflow-calibration`. Pass 6's finding named `workflow-driver` and a prior acceptance repair; this one names `workflow-calibration` and commit `222fba5a`, which is one commit after the commit that recorded Q-84.

THE AFFECTED SITES, all live product rather than transient records:

- `docs/plans/agent-scaffold.steps/sidecar-status-opening-drift.md:23` (27) and `:24` (18), rendered at `docs/plans/agent-scaffold.md:2578` and `:2579`.
- `:28`, "Q-84 (human, 2026-08-26) chose `Continue with the measured set of 18`".
- `:119`, "THE HANDOVER LIST, CURRENTLY MEASURED AT 18", rendered at `docs/plans/agent-scaffold.md:2674`.
- `docs/plans/agent-scaffold.plan.toml:2528` and `:2534`, the Q-84 `[[question]]` ask and its decision paragraph, which states "The current commands reproduce 44 relaxed selections, 35 anchored selections, 27 relaxed stripped openings needing authoring, and 18 anchored handover openings", rendered into the human-decision queue at `docs/plans/agent-scaffold.md:177`.
- `docs/plans/agent-scaffold.ledger.md:551`, "THE HUMAN CONFIRMED THE DRIFT-SIZE REFINEMENT: continue with the measured set of 18".

WHAT MAKES IT A SHORTFALL RATHER THAN A DATED NOTE. The project has an established safeguard here, which the pass-6 triage named: "The decision was previously re-put when this measurement moved; leaving its current value unsupported defeats that established safeguard." Q-84's recorded ask is literally "whether the status-opening drift split should continue after the dynamic selectors remeasured the authored-replacement handover at 18 rather than the 19 confirmed by `Q-78-driftsize`", and its chosen option is the string `Continue with the measured set of 18`. The human's recorded choice now names a number that the plan's own commands do not produce, on the same branch, one commit later. It stays `low` because `:28` and `:119` both state that the figures are dated evidence and never acceptance conditions, and criterion 1's pass condition compares selector output against selector output with no figure in it, so implementation remains executable.

SMALLEST SAFE DISPOSITION. Fix finding A first, since the correct fix there changes the numbers again; then remeasure, correct the four plan sites and the ledger line together, and either re-put the changed premise through the Q-78 decision path or durably record the human-approved reason it does not reopen Q-84. Do not write any figure into a criterion.

### C. `low` - `workflow-calibration` records Q-85's decision but not its exact receipt, and carries no structured provenance, against the criterion this same fold authored

`docs/plans/agent-scaffold.success-criteria.md:41`, added by commit `222fba5a`, reads: "The in-progress `workflow-calibration` step records Q-85's decision and exact receipt, keeps Q-86 `exploring`, and schedules the tracked `docs/plans/workflow-calibration.explorations/Q-86-convergence-mechanism-brief.md` design pass with a later human decision required before any cap, acceptance, reset, pack, or code change."

Every clause holds except the receipt clause. `workflow-calibration.md:18` records the decision in prose ("Q-85 decided to add the design pass here, inside the existing calibration step, rather than create a standalone convergence-redesign step or implement a hard task-level cap immediately") but never names the receipt. The step's `[[step]]` block in `agent-scaffold.plan.toml` has no `[step.provenance]` sub-table at all, so it carries no `decisions = ["Q-85"]`. The receipt pointer exists only on the `[[question]]` Q-85 item, which is a different plan object; the step itself records nothing that resolves to record 472.

THE BRANCH'S OWN CONVENTION IS UNIFORM AND THIS IS THE ONE EXCEPTION. Every other Q-8x fold on this branch links its decision to its owning step: `review-loop-class-inheritance` carries `decisions = ["Q-80"]`, `step-intent-encoding` `["Q-81"]`, `workflow-loop-visibility` `["Q-82"]`, `structured-risk-class-source` `["Q-83"]`, `sidecar-status-opening-drift` `["Q-84"]`, and `workflow-driver-typed-fleet` and `workflow-ready-frontier-scheduler` both `["Q-51", "Q-82"]`. `workflow-calibration` is the only one of the six Q-80 through Q-85 folds with no link.

THE OBSERVABLE COST. `src/plan/render.rs:492-514` builds the Roadmap Notes cell from `[step.provenance]` as a `why: decisions ...` fragment. Measured in the committed plan, `docs/plans/agent-scaffold.md:285` reads ``| `sidecar-status-opening-drift` | not started | why: decisions Q-84; commits e8b2992, 5ca89bb |`` and `:291` reads ``| `structured-risk-class-source` | not started | why: decisions Q-83 |``, while `:219` reads ``| `workflow-calibration` | in progress |  |`` with an empty Notes cell. The plan's live criterion that "a step carries structured provenance links to the decisions, findings, and commits that justify it, which `render` presents as why the step exists" therefore produces nothing for the one step that just gained new scheduled work.

THIS ALSO WEAKENS THE RE-GROUNDING PATH THE PLAN REQUIRES. `AGENTS.md`'s task-entry re-grounding rule requires a brief citing "a decision by `q_id` ... and, when instrumentation is on, its `type: "decision"` round-log record carrying the human's `chosen`", drawn from durable artefacts reached by stable handle. Entering `workflow-calibration` from its Step Detail yields no handle to Q-85's receipt; the reader has to already know to search the queue for it. It is `low` because the information does exist, in the `[[question]]` and in the log, so nothing is lost, only harder to reach.

SMALLEST SAFE DISPOSITION. Add `[step.provenance]` with `decisions = ["Q-85"]` to the `workflow-calibration` `[[step]]` block and cite the receipt inline in the sidecar paragraph the way the sibling folds do, then re-render.

## Recorded but not filed

- **Criterion 5 of `structured-risk-class-source` hard-codes counts of a population that can still grow.** `:67` requires a fixture accounting for "all 99 `plan_review` records exactly once", with sub-counts 63, seven, 41, 15, 36 and fourteen. The seven and 41 halves are digest-pinned and genuinely fixed, but the 15 and 36 halves rest on live declarations, so a plan review on any of those identities before the migration lands makes the literal figures stale. Not filed: every figure reproduces exactly today, the criterion's own qualifier is "current-history fixture", and no acceptance repair since record 431 has appended a `plan_review` record. Worth a sentence of hedging when the step is next touched, given the pass-6 triage's own caution not to convert a moving count into a pass condition.
- **Ledger obligation items (3) and (4) remain unregistered.** `agent-scaffold.ledger.md` still records that the routed-decision-tracking defect "still owes a `[[question]]` and has none" and that the `AGENTS.md:93` rebase-rule question "is still unregistered". Neither has a `[[question]]` at HEAD. Not filed on the same ground the pass-2 Claude reviewer recorded: neither is this pass's assigned product and neither maps to a Success Criterion. Noting that the paragraph heads itself "RETAINED AS EVIDENCE AND NOT AS CURRENT INSTRUCTION" while its closing sentence routes two of its items through the acceptance planner repair, which reads two ways.
- **`next` still projects `workflow-calibration` as `awaiting-first-review` and echoes a 730204-byte resume block.** Measured with the HEAD binary. Not filed: these are exactly the two limits Q-82 and the reopened Q-58 schedule, `workflow-loop-visibility.md:39` explicitly declines to claim it solves carrier bloat, and the Q-58 criterion records the historical byte totals as evidence and never as a target.
- **The fresh-scaffold criteria hold.** `scaffold --output-dir <scratch> --write --principles default --vcs none` drops 31 files, its `docs/plans/TEMPLATE.plan.toml` validates and `render --check --strict`es clean, no active `w4_baseline` is declared (only an explanatory comment), and a default re-run refreshes the 18 reference assets while leaving all 13 working-ownership assets untouched, including a local edit to `AGENTS.md`.

## Result

Three acceptance shortfalls: one `medium` and two `low`. All three were introduced or left by the two commits after the pass-6 repair, and all three share one root cause in the `workflow-calibration` fold, so they are cheapest to repair together and in the order A, B, C. The five pass-6 dispositions R6-G1, A, R6-G2 and R6-G3 are closed and reproduce under independent measurement; pass-6 finding B was closed at `11e129ed` and re-opened at `222fba5a`. Q-85 and Q-86 give a later explorer accurate, reproducible local evidence, correctly hedged external evidence, a bounded design space and an explicit reservation of the human decision, and I could not falsify any part of that. No finding is dismissed and none is accepted as residual, so no high or critical dismissal re-check is owed by this reviewer.
