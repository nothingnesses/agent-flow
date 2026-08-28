# Q-86 convergence-mechanism design brief

## Status and decision boundary

The design pass specified by this brief is complete. Q-86 is now `open` against the decision-ready synthesis at `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md`. Q-85 decided only where this investigation belongs by adding the design pass to the existing `workflow-calibration` step. It did not select a convergence mechanism. The synthesis retains all three viable bounded architectures and the separate serious-floor choice for the human. A later human decision is required before implementation.

This pass changes no current workflow rule or implementation. In particular, it does not change the five-round per-artifact cap, the reset-after-human-resume branch, the single-pass acceptance rule, any convergence constant, any Roadmap status, or any existing review identity.

## The question

What bounded convergence mechanism should replace or constrain the current possibility of indefinitely repeated review, repair, acceptance, and human-resume cycles while preserving useful late defect discovery and making it impossible for a budget to conceal an unresolved critical finding?

## Reproducible evidence to start from

### Current local rules

Read the current Convergence and Accept phases in `AGENTS.md`, the control constants in `.agents/workflow.toml`, and the typed convergence/single-pass requirements already scheduled in `docs/plans/agent-scaffold.steps/review-loop-foreclosure-enforcement.md` and `docs/plans/agent-scaffold.steps/workflow-driver-typed-fleet.md`.

The current convergence cap is five rounds per artifact. Reaching it escalates to the human, but applying a human decision that resumes the loop resets both counters, so another five-round window can begin. Convergence takes precedence if the cap-reaching round also earns the required clean streak. The cap is currently advisory in `.agents/workflow.toml`; `review-loop-foreclosure-enforcement` is the scheduled enforcement work.

Acceptance is a single reviewers-then-triager pass with no convergence streak, round loop, or cap. A valid shortfall returns to planning or implementation and a later acceptance pass verifies the repair. Nothing currently bounds the number of those later passes across the task.

These two paths make the current mechanism a required comparison baseline but not an admissible bounded candidate: repeated human resumes can open arbitrarily many new five-round windows, and later acceptance repairs can produce arbitrarily many acceptance passes. Every proposal's baseline section must demonstrate and report both counterexamples rather than claim a finite bound or exact terminal event for them. The baseline is not recommendation-eligible.

### Q-78 acceptance sequence

The six recorded Q-78 acceptance passes are the local demonstration of the uncapped branch. Derive their current count and valid-shortfall sequence from the append-only metrics log rather than copying a permanent total:

```sh
jq -s 'map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | {passes: length, valid_shortfalls: map(.valid_findings)}' docs/metrics/workflow.jsonl
```

At this fold the selector returns six passes and `[7,10,5,6,5,5]`. The selector is the authority if the log grows. The corresponding adjudications are `docs/plans/agent-scaffold.reviews/q78-acceptance-triage.md` and `q78-acceptance-r2-triage.md` through `q78-acceptance-r6-triage.md`; use them to test proposed lineage, scope, and severity rules rather than inferring those rules from counts alone.

### Existing calibration work

Read `docs/plans/workflow-calibration.explorations/calibration-analysis.md` and `2026-08-13-audit-when-the-loop-turned.md`. Preserve and extend their sequential/survival framing: a clean-round rule is censored by stopping, and cap behavior must be analysed jointly with the clean-streak bar rather than as an isolated constant. Preserve the already-raised severity-trajectory candidate: stopping may depend on whether serious findings are decaying, not only on binary clean/new-valid outcomes. Do not silently adopt either idea; compare it with the other mechanisms.

### External experiment and discussion

Read these sources directly:

- <https://kevinmahoney.co.uk/articles/ai-review-loops/>
- <https://gist.github.com/KMahoney/3098f0f12638d0a83a5ef3b91bef601d>
- <https://lobste.rs/s/52povq/ai_review_loops_don_t_always_stabilise>

The article's linked experiment is one artifact, one model family, one session, and three reviews, so it is a design input rather than a population estimate. It reported 10, 12, and 17 defects across the three reviews. Fix rounds created defects, the public and review surface grew, and two defensible contract trade-offs could oscillate indefinitely. Its machine-checkable core algorithm converged while open-ended contract, conformance, and prose obligations did not.

Reviewer framing is load-bearing. Reviews R1 and R3 were informed by claimed properties or the prior change list. R5 was blind to that history, found 17 defects, and found six defects already present during R3 that the informed reviews had missed. The write-up calls anchoring its strongest result while also acknowledging that blindness is confounded with prompt breadth and that the sample is one artifact. Proposals must therefore price blind artifact-wide discovery separately from informed fix verification rather than treating either allocation as universally superior.

The Lobsters discussion adds two bounded observations, not general proof: an open-ended "make it better" approval process can rewrite forever without a named defect, and the experiment's vague request for "perfect" code is an important confound. This supports testing a fixed rubric and scope boundary, not assuming that every review loop behaves like the experiment.

## Design space every proposal must cover

### 1. Budget identity and reset behavior

Compare the current repeated five-round per-artifact windows with at least one non-resettable task-level review budget. Price phase-specific sub-budgets for plan review, implementation/work review, and acceptance so one phase cannot consume the whole allowance accidentally. Define what counts against each budget: reviewer pass, triage, backstop re-check, repair pass, acceptance pass, and post-escalation continuation. State whether replan, rebuild, narrowed scope, or a new artifact identity can ever replenish a budget and how the rule prevents a rename or human resume from laundering spent review work.

### 2. Novelty, severity, and finding lineage

Define rules for at least these lineages: `pre-existing`, `fix-induced`, `scope-expanded`, and `relitigated`. Explain how a finding receives and retains identity across reviewers, triage, repairs, and later acceptance passes; how materially new evidence can reopen a settled finding; and how duplicate reviewer reports affect a budget. Keep lineage separate from severity: a pre-existing critical and a fix-induced critical are both critical, while a scope-expanded low may be a backlog candidate.

Compare binary clean/new-valid stopping with novelty and severity trajectories. A viable rule must distinguish decay in serious in-scope defects from churn in low-severity, optional, relitigated, or newly imported obligations without declaring genuine unresolved defects clean.

### 3. Fixed acceptance rubric and scope firewall

Specify when the task's acceptance rubric freezes and which durable artifacts define it. A reviewer may identify an optional improvement outside that frozen contract, but the mechanism must route a genuinely optional new obligation to a backlog rather than silently enlarging the current task. Define the test that distinguishes an optional scope expansion from a newly discovered violation of an existing Success Criterion, invariant, security boundary, or documentation-currency duty. The firewall must not become a way to relabel an in-scope defect as optional.

### 4. Terminal human choices

At budget exhaustion the human must receive explicit terminal choices through the human-input contract: accept residual risk, narrow scope, revert, replan, or abandon. Define the resulting durable state, receipts, waivers, and whether the task ends or a differently scoped task begins. No proposal may make "resume with reset counters" an unbounded default under a new name.

No budget may conceal an unresolved `critical` finding. Exhaustion must surface it explicitly, preserve its identity and evidence, and prevent a budget counter alone from treating it as resolved. Each proposal must say which terminal choices remain legal in that state and how revert, scope narrowing, or abandonment is represented without falsifying the finding's disposition.

### 5. Reviewer allocation and anchoring

Compare blind and informed allocation by phase and budget position. A blind reviewer receives the frozen artifact and rubric without prior findings or fix claims; an informed reviewer verifies a named fix and its affected region with lineage available. State when each is useful, whether at least one blind pass is reserved, and how model/harness diversity and cost interact with the allocation. Ground the trade-off in both the external anchoring result and this project's existing reviewer-attribution data, with their limits stated.

### 6. Sequential and severity-aware stopping

Carry forward the existing sequential/survival analysis and severity-trajectory ideas. For each mechanism, state what observations update confidence, what censoring remains, and what event stops the process. If the proposal uses a probabilistic threshold, define its data requirements and safe behavior when the sample is too small or the instrumentation is inconsistent. If it uses a deterministic budget, show why the selected structure is not merely another resettable cap.

## Required proposal output

Each explorer proposal must return:

1. The current mechanism as a required, explicitly non-admissible comparison baseline, plus more than one viable bounded mechanism. At least one viable bounded mechanism must be a non-resettable task-budget design. Do not count the baseline or cosmetic variants toward the viable-mechanism total.
2. Trade-offs for the baseline and every viable bounded mechanism against all eight Project Principles by name: Prefer the cleaner long-term architecture over the smallest diff; Minimal by default; Safe on existing projects; Idempotent; Make illegal states unrepresentable; Ground decisions in evidence; Reproducible; Structured data first, project for humans.
3. A recommendation, selected only from the viable bounded mechanisms, with reasoning, confidence, and the evidence that would overturn it. A mechanism is not recommendation-eligible until its stopping proof and red controls below pass.
4. A migration and enforcement plan for each viable bounded mechanism. Identify the single sources and projections that would move, including `.agents/workflow.toml`/`WorkflowSpec`, `ReviewProcess` reconstruction, metrics records, plan and ledger state, `validate --workflow`, `next`, pack guidance/prompts/templates, generated copies, README, changelog, and treatment of append-only historical records. Distinguish advisory guidance from mechanically enforced invariants.
5. Falsifiable stopping properties and red controls for each viable bounded mechanism. At minimum, model: repeated human resume; an unbounded acceptance-repair sequence; a fix-induced high finding near exhaustion; a scope-expanded low finding; relitigation without new evidence; narrowing/replan; and an unresolved critical at exhaustion. For each viable bounded mechanism, state a finite bound or the exact terminal event for every path. For the non-admissible baseline, instead demonstrate and report the repeated-resume and later-acceptance counterexamples that prevent such a proof; do not subject an already-disproved baseline to recommendation eligibility.
6. An explicit YAGNI boundary naming what not to build in the first implementation. Do not smuggle in a general issue tracker, autonomous risk judge, probabilistic defect oracle, reviewer marketplace, or rewrite of historical findings unless the chosen mechanism actually requires it and the human later authorises it.
7. The later human decision that implementation needs. Present only the synthesised viable bounded options through the human-input contract; keep the non-admissible baseline as comparison evidence and do not infer approval from Q-85.

## Local proof obligations for the design pass

Use scratch-only scripts or tables to replay the baseline and candidate mechanisms over the selected Q-78 acceptance sequence and over representative convergence histories from `docs/metrics/workflow.jsonl`. Keep scripts or exact commands with the proposal so another reader can reproduce every stated count. The baseline replay must exhibit the unbounded repeated-resume and later-acceptance paths. For each viable bounded mechanism, a toy state-machine or exhaustive transition table must demonstrate the stopping bound and the unresolved-critical invariant before that mechanism is recommendation-eligible. Do not mutate the live log, plan statuses, current review identities, workflow spec, pack, or code while investigating.

## Documentation impact

This scheduling fold changes only planning records, so no shipped pack or code documentation becomes stale now. Every proposal must nevertheless inventory the documentation and prompts its recommended mechanism would make stale, and its migration plan must keep the canonical pack sources and generated copies coherent. Implementation remains blocked on the later Q-86 human decision.
