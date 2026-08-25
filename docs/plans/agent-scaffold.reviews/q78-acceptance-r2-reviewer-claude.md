# Q-78 acceptance pass 2, Claude reviewer

## Verdict

**Five shortfalls: two `medium`, three `low`.** All seven triaged shortfalls T1 through T7 are CLOSED, and I falsified rather than read the two whose repairs are executable (T1's waiver removal and T2's receipt-source arm). The Q-58 ablation is genuinely reopened, and the staged visibility / typed-fleet / ready-frontier work is actionable and does not duplicate the existing driver architecture.

The five shortfalls are all in the NEW work this pass added, not in the seven repairs. Two are `medium`: one newly added Success Criterion, applied to the repository it governs, would make `validate --workflow` reject this repo's own round log, and the owning step's acceptance criterion asserts the opposite; and T1 removed the duplicate waiver record but left the shipped guidance that instructs writing it, unqualified, in three files.

`Q-78`'s `open` status is not filed as a shortfall, per the brief.

## Scope

Artifact: the complete plan branch at `review/q78-acceptance-r2-claude` tip `040e6cc`, whose product content is commit `866d793` on top of the first acceptance pass. Measured against the plan's Success Criteria (`docs/plans/agent-scaffold.success-criteria.md`, now 37 criteria including the five this pass added), the `Q-78` / `Q-80` / `Q-81` / `Q-82` decisions, the Q-58 refinement, the Project Principles and documentation currency.

Read in full: `AGENTS.md`; both first-pass acceptance reports and `q78-acceptance-triage.md`; `q78-acceptance-fix-brief.md`; `866d793` in full diff; `docs/plans/agent-scaffold.plan.toml` and the generated `docs/plans/agent-scaffold.md`; all eight new step sidecars plus the four modified ones; `docs/plans/step-intent-encoding.explorations/Q-78.md`; the `Q-58`, `Q-78`, `Q-80`, `Q-81`, `Q-82` and `Q-46`/`Q-47` question blocks; the ledger from `RESUME HERE` (`agent-scaffold.ledger.md:535-560`); and all 463 records in `docs/metrics/workflow.jsonl`.

Review briefs and transient findings files are excluded from the product.

Product scope confirmed clean: `git diff --stat main...HEAD -- src/ Cargo.toml Cargo.lock pack/ tests/ build.rs` is EMPTY. `git status --porcelain` is empty apart from this file.

## Harness, stated rather than glossed

**The Nix development environment is unavailable in this container, so I could not use `direnv` as the brief directs.** `direnv`'s store path is on `PATH` but absent from the filesystem (`/nix/store/gv6dc61q6sprcm3hr69yxnwjn3gwcvsc-direnv-2.37.1/bin`: no such file or directory), and `nix` is absent the same way. Rather than report the gates unrun, I built against a toolchain already in the store: `cargo`/`rustc` 1.95.0 from `/nix/store/9l9lclxjw8ns5q4k13lxld7pl90paa3g-rust-mixed`, `cc` from `gcc-wrapper-15.3.0`, and `SSL_CERT_FILE` repointed at `/nix/store/206m56yfhycp91zp3y6ry3ddirqflnxs-nss-cacert-3.126/etc/ssl/certs/ca-bundle.crt` because the bundle the environment names is a dangling path. The crate declares `rust-version = "1.88"` (`Cargo.toml:5`), so 1.95.0 satisfies the MSRV; the flake pins fenix `latest`, so this is not byte-identical to the project toolchain and the gate results should be read with that caveat. `CARGO_HOME` and `CARGO_TARGET_DIR` were both inside the authorised scratch, and `cargo fetch` was the only network call.

GNU grep 3.12 was used for every figure, at `/nix/store/gn94gpcp5q08x4v6g8mvw8v4r65rcjzk-gnugrep-3.12/bin/grep`. Bare `grep` in this harness resolves to **ugrep 7.5.0**, whose `-c`, `-o` and `-r` behaviour is not GNU's, so this needs recording exactly as the first pass recorded it.

Scratch: `.../scratchpad/q78-acceptance-r2-claude`, the authorised read-write mount. Nothing was written to bare `/tmp`, and nothing outside that directory and this one committed file.

## Gates, all green

| Gate | Result |
| --- | --- |
| `validate --source docs/plans/agent-scaffold.plan.toml` | `463 records, valid`; `113 steps, 82 questions, valid`; exit 0 |
| `validate --workflow --source docs/plans/agent-scaffold.plan.toml` | `workflow invariants hold`; exit 0 |
| `render --check --strict docs/plans/agent-scaffold.plan.toml` | `up to date`; exit 0 |
| `cargo test` | 470 passed, 0 failed, across 12 binaries |
| `cargo clippy --all-targets --all-features -- -D warnings` | exit 0 |
| `LC_ALL=C grep -cP '[^\t\x20-\x7e]'` over all 18 files `866d793` touched | `0` for every file |

## T1 through T7, each verified closed

**T1, the duplicate JSONL waiver: CLOSED, and I falsified it rather than read it.** `jq -r '.type' docs/metrics/workflow.jsonl | sort | uniq -c` now returns `310 round`, `133 decision`, `17 escalation`, `2 intake`, `1 dismissal_recheck` and NO `waiver`, which is exactly the five-type event set `success-criteria.md:20` names. The TOML waiver survives at `agent-scaffold.plan.toml:1627` (`step-intent-encoding-w1`) and both backing escalations survive (`task:"step-intent-encoding-inc1"`, `human_decision` `resume` and `decision`, both `ts:"2026-08-24"`). Nothing else was pruned: the log went 459 -> 463 records, minus one waiver plus three decision receipts and the counted delta agrees.

**T2, the decision-receipt source route: CLOSED, and this is the strongest repair in the pass.** I extracted the R2 script verbatim from `step-intent-encoding.md:629-708` into scratch and ran it against the real log with a stubbed `agent-flow status --step`. Every control the sidecar promises fired, on real data:

| Row | Source | R2 output |
| --- | --- | --- |
| `transcribed`, `task` matches | `866d793:docs/metrics/workflow.jsonl#L462` | passes, `rows=1 transcribed=1 paraphrased=0 bad=0` |
| bare metrics path | `866d793:docs/metrics/workflow.jsonl` | `RECEIPT LINE REQUIRED` |
| receipt whose `task` is another step | `...#L463` (`Q-82`, `task` `workflow-loop-visibility`) | `RECEIPT NOT THIS STEP` |
| a `round` record, not a decision | `...#L1` | `RECEIPT NOT THIS STEP` |
| absent line | `...#L99999` | `UNRESOLVED RECEIPT LINE` |
| fragment on a prose path | `866d793:docs/plans/agent-scaffold.md#L10` | `UNSUPPORTED SOURCE FRAGMENT` |
| malformed selector | `...#Lzero` | `BAD RECEIPT LINE` |

The passing row is a genuine end-to-end proof, not a shape check: the complete value occurs in the selected receipt's decoded `chosen`, and the earliest-commit arm resolves `git log --reverse -S"$receipt_record" -- docs/metrics/workflow.jsonl` to `866d793`, which is the cited commit. The whole log is never admitted as a blob, in either R1's `case` ladder (`:590-596`) or R2's. Rule 5, rule 6, criterion 8 and the exploration's rules 2 and 3 all carry the same grammar, so the three documents agree.

**T3, Roadmap ownership: CLOSED.** Four new steps carry the previously unowned obligations, in a declared dependency order: `structured-risk-class-source` (order 109, decision `Q-78-risk-class-source`, `chosen` verified `Use structured risk_class only`), `review-loop-class-inheritance` (110, `blocked_by` the former, `[step.provenance].decisions = ["Q-80"]`), `review-loop-foreclosure-enforcement` (111, `blocked_by` the former, decision `Q-78-foreclosure-enforcement`, `chosen` verified `Report and enforce foreclosure plus the round cap`) and `sidecar-status-authored-openings` (112, `blocked_by sidecar-status-opening-drift`). `Q-80` is `decided -> folded into review-loop-class-inheritance`, and its receipt repeats `Q-78-classinherit`'s options, recommendation and `chosen` byte-for-byte; I diffed the two records and only `task` and `ts` differ, so no new human choice was invented and W4's join is satisfied. No redundant `Q-81` prose fold was added, as the triage directed.

**T4, the stale single-line recommendation: CLOSED.** The live ask now reads "two required non-empty fields ... each containing one or more paragraphs, with a single paragraph valid and no sentence, line or character cap" and the cost paragraph reads "two non-empty prose values". The remaining `single-line` hits in the tree are RULE 2's TOML source-representation clause and `Q-78.md`'s explicit supersession note, both correct.

**T5, the fixed totals: CLOSED.** `DECIDED TWELVE TIMES`, `six plus six` and `THE SIX THAT BEAR` are all gone from both the TOML and the generated view; the reproducible selector and the "this item maintains no inventory total or fixed partition" instruction remain.

**T6, the changelog foreclosure: CLOSED.** `validate-missing-source-exit.md:124-129` adds a `DOCUMENTATION IMPACT` section that states the boundary and the upgrade action, and criterion 10 (`:120`) now lists `CHANGELOG.md` in the exact path set and adds "the exact set must never force a correct documentation update out of the increment", which generalises the fix. The README exclusion is preserved and re-stated as a re-measurable claim. Every other step this pass authored that promises a changelog entry also names `CHANGELOG.md` in its path set, so the defect class is not reproduced (but see shortfall 4 for an arithmetic slip in one of them).

**T7, the residual-set overclaim: CLOSED.** All three sites now say "design residual" and disclaim inventorying the separately owned review residuals: `Q-78.md:324`, the `Q-78` ask, and `step-intent-encoding.md:1075`.

## Q-58 and Q-82, verified as the brief directs

**The ablation is genuinely reopened, not relabelled.** Five independent things changed together: the 2026-07-24 shelf decision is retitled `HISTORICAL RUN DECISION` and its premise explicitly retired; a `REOPENED RUN DECISION` records the option set with a matching `type:"decision"` receipt (`q_id:"Q-58"`, `chosen` `Reopen Q-58 and run the ablation`); `q58-output-ablation` (order 108, one `risky` increment) owns the run and points at the retained design at `docs/plans/code-value-audit.explorations/Q-58-ablation-design.md`, which exists; `resume-state-currency-signal` moved from `blocked_by = []` to `blocked_by = ["q58-output-ablation"]` and its gating paragraph now follows the reopened experiment instead of the stale deferred premise; and Q-58 stays `exploring` with an explicit `exploring -> open -> human decides` boundary before any implementation. The step forbids authoring a second scoring design and preserves the oracle-circularity caveat verbatim as a requirement (`q58-output-ablation.md:6`, criterion 2's V4 control). That is the AGENTS.md design-space-exploration lifecycle applied correctly.

**The staged loop work is actionable and does not duplicate the driver architecture.** `workflow-driver.md` gains a forward-handover paragraph naming all three successors and keeping Stage 0a/0b/1 identities unchanged; the TOML confirms `workflow-driver` declares only `stage0a`, `stage0b` and `stage1` as `[[step.increment]]`, so Stage 2 and Stage 3 were never double-owned. `workflow-driver-typed-fleet` opens "This step implements the existing Stage-2 architecture; it does not redesign it", names `workflow-driver.md` plus the two `mealy-workflow-driver.explorations/r2-*` files as the authority in prose AND in `[step.provenance].findings`, and its documentation-impact section says "Do not duplicate the Stage-2 design in a new durable design note". `workflow-ready-frontier-scheduler` does the same for Stage 3. Scheduler authority is absent from the first stage by construction: `workflow-loop-visibility` criterion 8 rejects "`src/driver/` fleet, DAG scheduler, write command, worktree spawn or parallel execution" in a changed-path review, and criterion 4 pins `active_loop` to be one member of `active_loops` byte-for-byte.

**The motivating defect reproduces.** `agent-flow next --source docs/plans/agent-scaffold.plan.toml --json` selects `workflow-calibration` and reports `"state":"awaiting-first-review"` with `risk_class` null and no round records, while `workflow-driver` and `code-value-audit-static` are also `in-progress` and invisible. So criterion 39's premise is real and measured, not asserted.

## Shortfalls

### 1. The newly added over-cap criterion, applied to this repository, rejects this repository's own log, and the owning step's criterion 6 asserts the opposite (`medium`)

**The criterion**, added by this pass at `docs/plans/agent-scaffold.success-criteria.md:37`:

> `validate --workflow` and `next` share one ordered loop-window reconstruction that applies scoped escalation resets, convergence-first precedence, foreclosure arithmetic and the workflow spec's total-round cap; `next` escalates when convergence is impossible within the remaining rounds, and validation rejects a foreclosed, cap-reached-without-escalation or over-cap active window.

Its owning step spells the rule out at `review-loop-foreclosure-enforcement.md:9`: "`validate --workflow` rejects: a foreclosed active window with no following scoped escalation; a cap-reached unconverged window with no following scoped escalation; and **any window containing more rounds than the cap**." And it promises at `:22`:

> 6. Existing Q-78 and other historical multi-segment loops validate by joining their recorded escalation boundaries; no test deletes or rewrites history to make the check green.

**Measured, and it is the Q-78 pass's own loop that breaks it.** I reconstructed every window in the log by walking `round` and `escalation` records in file order, keyed on `.increment // .task`. Exactly one unit has a window longer than the cap of 5:

```
jq -rc 'select(.type=="round" or .type=="escalation") | [(.increment // .task), .type] | @tsv' docs/metrics/workflow.jsonl
```

`q78-design-pass` carries **eight** `round` records and **zero** `escalation` records. Seven are `phase:"plan_review"` at JSONL lines 380-386, all `outcome:"new_valid"`, all `consecutive_clean:0`, all `risk_class:"risky"`; the eighth is `phase:"acceptance"` at line 432. Even split by phase, the `plan_review` window is 7 rounds against a cap of 5, unbroken by any escalation. Every other unit in the log is inside the cap once its escalations segment it, including `step-intent-encoding-inc1` (9 rounds, segments 4 / 4 / 1) and `ship-v0-0-2-inc1` (7 rounds, segments 5 / 2).

**No escalation record can be joined to it, on any axis.** All 17 escalations in the log carry `task` values of `optional-modules-inc2cii`, `waiver-model`, `structured-skeleton-inc6`, `driver-output-generation-inc2`, `prompt-drift-guard-inc1`, `checks-runner-worktree-name-collision-inc1`, the six `workflow-enforcement-tier-*`, `ship-v0-0-2-inc1`, `step-intent-fold`, and `step-intent-encoding-inc1` (twice) and `-inc3`. None is `q78-design-pass`, none resolves to it by `leading_slug`, and none carries a structured `step`/`increment` that reaches it. The two escalations these rounds describe in their own `artifact` prose ("its SECOND ESCALATION" at line 383; "after the human directed a rebuild rather than a fifth repair" at line 384) were never logged as `type:"escalation"` records.

**So criterion 6 is unsatisfiable as written, by its own second clause.** There is no "recorded escalation boundary" to join for this loop, and the only remaining routes are to append the two missing escalation records (which criterion 6's "no test ... rewrites history to make the check green" is aimed at) or to scope the check to units that join to a Roadmap step, which the sidecar never says and which would leave the enforcement silent on the single worst over-cap window in the repository. `q78-design-pass` is not a Roadmap slug: `grep -c 'slug = "q78-design-pass"' docs/plans/agent-scaffold.plan.toml` returns `0`.

**Why this is the right time to raise it.** The step is `not-started`, so nothing is broken today, and `validate --workflow` is green precisely because it does not enforce the cap yet, which is the defect the step exists to fix. But this pass's own standard is that a criterion must name what it refuses and be measurable before the step opens, and this one was authored against data nobody measured. The repair is a plan edit: either state the scoping rule for units with no Roadmap join, or record the two missing `q78-design-pass` escalations as a named, reasoned addition and say so in criterion 6, rather than leaving an implementer to discover the contradiction with a red suite.

### 2. T1 removed the duplicate waiver but not the shipped guidance that instructs writing it, and that guidance ships to every scaffolded project (`medium`)

**The criterion**, `docs/plans/agent-scaffold.success-criteria.md:20`: the TOML holds "(per Q-46) the exemption waivers nested on their step ...; the append-only `docs/metrics/workflow.jsonl` holds only genuine events (rounds, escalations, decisions, intakes, dismissals)." `Q-46`'s own decision text states the same consequence: "the JSONL keeps only genuine events (`round`/`escalation`/`decision`/`intake`/`dismissal`)".

**Measured.** `pack/instrument.md:11` still documents `type: "waiver"` as a live JSONL record type, in full schema detail, with no TOML-primary caveat, and it ships verbatim into `AGENTS.md:147` and `.agents/AGENTS.reference.md:147`. Its sibling `baseline` bullet one line above (`pack/instrument.md:10`, `AGENTS.md:146`) carries exactly the caveat the `waiver` bullet lacks: "For the plan-TOML flow (`[meta].primary = "toml"`) the live cutoff is `[meta].w4_baseline` in the plan TOML ...; this JSONL record is the legacy form of the same cutoff that the TOML field superseded per Q-46." That same sentence then asserts, of the type this shortfall is about, "W3's historical exemption is carried by per-unit `type: "waiver"` records", which is false on a TOML-primary substrate.

**It is false for every scaffolded project, not just this one.** `pack/plan-template.plan.toml:15` ships `primary = "toml"`, so a fresh scaffold is TOML-primary by default, and `check_workflow_toml` sources waivers only from `waivers_from_toml(plan)` (`src/workflow.rs:192`) while it reads the JSONL for decisions and escalations alone. A scaffolded orchestrator following `instrument.md` writes an inert record. The pack DOES document the correct home, but only as a commented example inside the plan template (`pack/plan-template.plan.toml:39-47`), and the two documents never point at each other.

**This is the standing cause of T1, not a separate topic.** T1's finding was one instance of exactly this instruction; the fix brief's T1 says the removal "restores Q-46's event-only log", but the log-writing instruction that breaches it is untouched and will be followed again. The pass could not have repaired it: its own brief says "Do not implement code, edit `pack/`". So the correct disposition is new Roadmap ownership, not a re-run of this pass, and it composes naturally with `structured-risk-class-source`, which already edits `pack/instrument.md`'s neighbours.

**Stated so the triager can weigh it accurately: this fails CLOSED, not silently.** W3 is convergence-OR-waiver, so a waiver in the unread substrate leaves the step unexempted and `validate --workflow` exits non-zero naming the short streak. The cost is a confusing loud failure plus two documented homes for one concept, not an unsound exemption. I rate it `medium` because it is live contradictory guidance in a shipped doc on the exact subject a Success Criterion pins, and it has already produced one `medium` finding inside this pass.

### 3. The 727754-byte figure grounding the Q-58 reopening and Q-82 carries no selector and does not reproduce (`low`)

Eight sites in the plan source state it in the present tense, with no command anywhere: `agent-scaffold.plan.toml:2139` (the `Q-58` reopened decision), `:2479` and `:2485` (the `Q-82` ask and decision), `workflow-loop-visibility.md:5`, `resume-state-currency-signal.md:5` and `:9`, and `q58-output-ablation.md:3` and `:17`. It is the sole quantitative evidence for reopening `Q-58` and for `Q-82`'s "Ground decisions in evidence" reasoning.

**Measured at the branch tip**, from the worktree root: `agent-flow next --source docs/plans/agent-scaffold.plan.toml | wc -c` prints **730209**, and `--json` prints 733192. The figure is path-length sensitive (the source path is echoed twice), so I normalised across commits by rendering each commit's `plan.toml`, `ledger.md` and `workflow.jsonl` into one fixed scratch path: `d271b82` (main) 729072, every branch commit from `4d6f1b5` to `040e6cc` 730495, `3ad7b2b` (the commit before the intake was recorded) 727833. Nothing reproduces 727754; the closest state is 79 bytes away, which reads as a genuine measurement of a tree between commits rather than an invented number.

The conclusion it grounds is robust either way (~730 KB against the ~6 KB the shelf decision assumed), and `q58-output-ablation` criterion 1 already anticipates drift by admitting "or explains, with the exact command, source commit and input paths, why the current measurement differs". What I am filing is the missing selector, not the drift: every other measured figure in this pass carries the command that produces it, and this one is the only load-bearing figure a reader cannot re-derive.

### 4. `structured-risk-class-source`'s exact changed-path set contradicts its own enumeration (`low`)

`structured-risk-class-source.md:25` reads: "The changed-path set is exactly **the eight guidance/template files named above plus `CHANGELOG.md`**".

Measured against the `WHAT CHANGES` block it points at (`:15-18`), which names exactly eight files in total: `pack/AGENTS.md`, `AGENTS.md`, `.agents/AGENTS.reference.md`, `pack/prompts/orchestrator.md`, `.agents/prompts/orchestrator.md`, `pack/LEDGER.template.md`, `.agents/LEDGER.template.md` and `CHANGELOG.md`. That is **seven** guidance/template files, with `CHANGELOG.md` as the eighth entry, already named above.

So the criterion's arithmetic yields a nine-file set with an eighth guidance file that does not exist, while its enumeration yields eight. An exact changed-path criterion is the one criterion kind this pass treats as load-bearing (T6 was about precisely that), and a reviewer measuring the increment against `:25` cannot tell which set to hold it to. One word fixes it.

### 5. Authoring the successor step left the predecessor's handover paragraph stale, and the new step's documentation-impact section does not record it (`low`)

`sidecar-status-opening-drift.md:116` still reads, present tense: "The successor step, with its own increments, its own risk classes and their `AGENTS.md:56` grounds, and its own acceptance criteria over an authored opening, **is a planner's to author** against this sidecar as its input."

That was true before `866d793` and the first acceptance report cited it approvingly as a clean handover. It is false now: `sidecar-status-authored-openings` exists, declares one `risky` increment, and is `blocked_by = ["sidecar-status-opening-drift"]`. The paragraph also names no slug, deliberately, so after this pass the plan's only forward link from the drift step to its successor is the `blocked_by` edge on the other side.

`sidecar-status-authored-openings.md`'s own "Documentation impact" section says "No shipped documentation changes", and neither it nor any other part of `866d793` records that authoring the successor makes its predecessor's paragraph stale. That is the documentation-impact assessment the planner duties require of a folded change (`success-criteria.md:33`), applied to the plan's own prose. The rationale sentence that follows it ("a stub authored inside a fix pass is the crossing this loop already recorded once") stays true as history and should be kept.

## Recorded but not filed

- **The ledger's `RESUME HERE` is one orchestrator step behind.** `agent-scaffold.ledger.md:535` still reads "Q-78 ACCEPTANCE SHORTFALLS READY FOR PLANNER REPAIR" and "THE IMMEDIATE NEXT ACTION IS ONE PLANNER PASS that repairs T1 through T7", which `866d793` performed. This is the orchestrator's round-boundary update, owed after this review rather than before it, and the fix brief explicitly barred the planner from touching the ledger, so it is not a shortfall of the pass.
- **Two obligations from the ledger's historical list are still unowned**, and the fix brief did not route them: item (3), the routed-decision-tracking defect that "still owes a `[[question]]` and has none, after being recorded as owing one twice", and item (4), the `AGENTS.md:93` rebase-rule question that "is still unregistered and predates this pass" (`agent-scaffold.ledger.md:551`). The ledger itself classes both as planner work rather than human decisions. Not filed because neither is this pass's assigned product, but they should not fall off the queue.
- **`agent-scaffold._status-narrative.md` does not mention any of the eight new steps or five new criteria.** Not filed: `sidecar-status-opening-drift.md:111` already records that file as a named, reasoned exclusion ("a long historical accretion whose currency is a separate and much larger question"), so it is owned, not missed.
- **`Q-58` now carries three `type:"decision"` receipts while still `exploring`**, so the eventual closing receipt will be indistinguishable to W4's `d.q_id == question.id` join from the 2026-07-24 route receipts. Not filed: this is exactly the W4 weakness the `Q-78` item already records in full and assigns to its own future question, and the new receipt neither creates nor widens the rule.

## What I verified and found sound

- **The array-position migration oracle survives the eight new steps.** 113 `[[step]]` blocks; sorting by `order` and diffing against declaration order still yields exactly one transposition, `rename-to-agent-flow` declared 84th and ordered 98th, and the two `order` gaps still fall after 83 and after 90. The new steps take 108-115 in declaration order, so `plan-order-array-position`'s central byte-exact claim is untouched.
- **The waived increment's convergence accounting still holds.** `step-intent-encoding-inc1`: 9 rounds, segmented 4 / 4 / 1 by its two escalations, final segment clean at streak 1 against a `risky` bar of 2, exempted by `step-intent-encoding-w1` whose `record-backed` evidence joins the `human_decision:"decision"` escalation. Twelve of thirteen loops converged unwaived. No `high` or `critical` finding was dismissed anywhere in the pass, so no backstop re-check is owed here either.
- **Every receipt the new sidecars cite resolves, with the right `chosen` value.** `Q-78-risk-class-source` -> `Use structured risk_class only`; `Q-78-foreclosure-enforcement` -> `Report and enforce foreclosure plus the round cap`; `Q-78-classinherit` and `Q-80` -> byte-identical option sets; `Q-82` -> `Schedule visibility and scheduling in stages`; `Q-58` -> `Reopen Q-58 and run the ablation`. Each new step's prose matches its receipt rather than paraphrasing it.
- **The new steps' dependency graph is acyclic and every blocker resolves**, which `validate --source` confirms: `structured-risk-class-source` -> `review-loop-class-inheritance` -> `review-loop-foreclosure-enforcement`; `sidecar-status-opening-drift` -> `sidecar-status-authored-openings`; `q58-output-ablation` -> `resume-state-currency-signal` -> `workflow-driver-typed-fleet` -> `workflow-ready-frontier-scheduler`, with `workflow-loop-visibility` an independent parallel blocker of the typed fleet.
- **The eight new sidecars each carry a documentation-impact section and a grounded risk class.** All eight increments are `risky`, and each states its ground against the `AGENTS.md:56` risk test rather than asserting the class, including the two whose ground is process blast radius rather than code.
- **`q58-output-ablation` does not collide with the `Q-52` code-value work.** `code-value-audit-deletion-experiment` is the mutation/deletion signal over the crate; the ablation is over `next` output content. They share only the explorations directory the design record already lives in.
- **No shipped surface changed and none was made stale by the repair itself.** `git diff main...HEAD` touches no file under `src/`, `pack/`, `tests/`, and `CHANGELOG.md`'s section list is unchanged, so the doc-currency check has nothing to catch beyond shortfall 2, which predates this pass.

## Totals

- Raw findings: 5.
- Severity ceiling: `medium`.
- By severity: 0 critical, 0 high, 2 medium, 3 low.
- Backstop re-check: not owed (nothing dismissed at any severity).
- T1 through T7: all seven closed, two of them falsified by execution rather than read.
- Recorded but not filed: 4 items, above.
