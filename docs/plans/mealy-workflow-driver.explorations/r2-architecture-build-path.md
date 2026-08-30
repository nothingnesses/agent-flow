# Q-51 round 2 exploration: architecture and incremental build path

Lens: the concrete Rust ARCHITECTURE for the FULL driver (the human's target, Option B) AND a STAGED, reviewable path to it. This note answers the round-2 brief carried in the Q-51 ask: keep the workflow LOGIC DATA-DRIVEN (a spec the tool interprets, not hardcoded Rust) so the workflow can still evolve without heavy code churn, and stage the build so the advisory tier is the first increment on the path to the full driver, reusing the W3 / `state-queries` / `render` machinery already shipped. It builds on the round-1 model: `fsm-concurrency-model.md` supplies the hierarchical-fleet FSM this note types out; `tool-vs-prose-boundary.md` supplies the `workflow.toml` + generation approach this note makes concrete; `io-contract-and-adoption.md` supplies the `next` surface; `yagni-skeptic.md` supplies the evidence gates the staging respects.

Numbering note: "Principle N" below is the plan's numbered Project Principles (1 cleaner-long-term-architecture, 2 minimal-by-default, 3 safe-on-existing-projects, 4 idempotent, 5 illegal-states-unrepresentable, 6 evidence-first, 7 reproducible, 8 structured-data-first). Where I mean an AGENTS.md workflow principle (for example small-and-reviewable changes) I say "Workflow Principle".

Grounding (files this design reuses or extends): `src/plan/source.rs` (the `PlanToml` / `Step` / `Increment` / `StepStatus` schema, authoritative `[[step.increment]].risk_class`, scheduled `[[task_loop]]` declarations, migration-only Q-81 increment-plan, exact-step-plan, and unowned-work-review rows, the `[[active_work]]` union, `step_views` / `question_views`, and the ordinary `blocked_by` plus typed blocker-policy DAG); `src/plan/render.rs` (the render closure: `render_plan`, `assemble`, and the already-working generated fragments `vocabulary_section` / `status_line` / `principles_section`, plus the `render --check` byte-compare); `src/metrics.rs` (`RiskClass`, auditable `Round.risk_class`, phase-bearing `Round`/`Escalation`, `RoundOutcome` / `Decision` / `Waiver`, `parse_rounds`); `src/workflow.rs` (W3/W4/W5 and the scheduled shared `ReviewProcessHistory` reconstruction); `src/main.rs` (the clap subcommand surface); `src/manifest.rs` + `src/main.rs::build_assets` (the pack `{{...}}` slot mechanism that generates `AGENTS.md` at scaffold time). Q-83 supersedes this retained design's earlier first-round-authority assumption: the applicable Roadmap increment or task-plan declaration exists before round one, while Q-81 increment-plan and exact-step-plan history are digest-pinned and non-active; phase stays in the loop identity; every convergence snapshot must match; and missing declarations fail closed. The exact active-work row, not declaration order or round recency, identifies an open loop.

## 1. The load-bearing architectural facts

Three facts from the grounding set the whole design.

- The convergence relation is ALREADY reconstructed forward from the durable files. `round_log_consistency_problems` walks an increment's rounds in file order recomputing the implied streak (`clean` adds one, `new_valid` resets to zero); `w3_problems` takes the peak against `class.required_streak()`. The driver's transition function IS that arithmetic run forward to emit the next move rather than to check a completed history. So the FSM core is not new logic; it is the checker's relation with a next-move projection (the fsm lens's central claim, now grounded in the exact functions).
- There are TWO generation sites, not one, and the tool-vs-prose lens conflated them. `plan::render_plan` renders `<task>.md` from `<task>.plan.toml` + sidecars (this is where `vocabulary_section` / `status_line` live). `AGENTS.md` is generated separately, at SCAFFOLD time, by `build_assets` filling the pack guidance template's `{{principles}}` / `{{instrument}}` / `{{modules}}` slots (`src/main.rs:231`). The workflow control fragment therefore belongs to the PACK mechanism (a new `{{workflow_control}}` slot), not to `plan::render`. The two share the "generate the WHAT, hand-author the WHY" pattern but are distinct code paths; the design must target the right one.
- `required_streak` is the only convergence constant already in code, and it is a hardcoded Rust `match` (`src/metrics.rs:130`). Single-sourcing it is the smallest real change that closes the live `required_streak`/AGENTS.md prose duplication AND establishes the data-driven substrate the human asked for. It is the natural first increment.

## 2. The data-driven workflow spec (`workflow.toml`)

### 2.1 What it is and where it lives

A tool-owned reference asset shipped by the pack and scaffolded to `.agents/workflow.toml` (Reference ownership in `manifest.rs`, so it is always refreshed, like the role prompts). It is the SAME for every scaffolded project (it encodes THIS workflow), so it is a pack asset, not a per-task file; `agent-scaffold`'s own repo dogfoods its own scaffolded copy. It holds ONLY the deterministic CONTROL data the driver interprets and the checker reads: constants, enumerable sequences, path templates, tier order, role->prompt map. It holds NO judgment and NO transition logic (the KINDS of transitions stay Rust; only their CONSTANTS and orderings are data, per the tool-vs-prose lens's "a new constant value is a data edit; a new rule kind is a code change").

### 2.2 Proposed shape

```toml
[meta]
version = 1

[convergence]
# risk class -> required consecutive-clean streak (single-sources RiskClass::required_streak)
required_streak = { low_risk = 1, risky = 2 }
round_cap = 5
# the four-level severity scale, and the threshold at/above which a dismissal must be
# re-checked before it can count toward a clean round (the backstop gate)
severities = ["low", "medium", "high", "critical"]
backstop_severity = "high"

[phases]
# the fixed task phase order and which phases run the consecutive-clean loop
# vs a single reviewers-then-triager pass (acceptance / standalone review)
sequence = ["plan", "plan_review", "implement", "accept"]
loop_phases = ["plan_review", "work_review"]
single_pass_phases = ["acceptance", "review"]

[isolation]
# strongest-first preference order the driver RESOLVES and emits (it never isolates)
tier_order = ["container", "worktree", "file_safety"]

[roles]
orchestrator = ".agents/prompts/orchestrator.md"
planner      = ".agents/prompts/planner.md"
reviewer     = ".agents/prompts/reviewer.md"
triager      = ".agents/prompts/triager.md"
implementer  = ".agents/prompts/implementer.md"

[paths]
# string templates the driver fills; {task}/{step}/{role}/{disambiguator}/{q_id} are slots
ledger            = "docs/plans/{task}.ledger.md"
metrics           = "docs/metrics/workflow.jsonl"
findings_reviewer = "docs/plans/{task}.reviews/{step}-{role}-{disambiguator}.md"
findings_triage   = "docs/plans/{task}.reviews/{step}-triage.md"
findings_recheck  = "docs/plans/{task}.reviews/{step}-triage-recheck.md"
exploration       = "docs/plans/{task}.explorations/{q_id}.md"
review_report     = "docs/plans/{task}.review-report.md"
```

### 2.3 Single-sourcing: how validate, the driver, and render all read it

The spec is parsed once into a `WorkflowSpec` and threaded to every consumer. Concretely:

- `RiskClass::required_streak()` stops being a hardcoded `match`. It becomes `WorkflowSpec::required_streak(class) -> u64`, a lookup into `[convergence].required_streak`. `w3_problems` (which today calls `class.required_streak()` at `workflow.rs:457`) takes the spec and calls the spec accessor. The round cap (default five, today only in prose) becomes `spec.round_cap()`.
- A BUILT-IN DEFAULT spec (a `WorkflowSpec::builtin()` equal to today's constants) is used when a project ships no `.agents/workflow.toml`, so `validate --workflow` on an existing project is byte-for-byte unchanged (Principle 3). A compile-time / test assertion pins `builtin().required_streak(Risky) == 2` and `== 1` for low-risk, so the default cannot silently diverge from the historically enforced bar (Principle 5, 16).
- `render` (the pack build) projects the AGENTS.md control fragment from the same spec into a new `{{workflow_control}}` slot: the streak-per-class sentence, the cap, the backstop severity, the tier order, and the path conventions, exactly as `vocabulary_section()` already emits the status vocabulary "from the code constants, so it cannot drift". The hand-authored rationale (WHY two clean rounds, WHY the triager is never collapsed) stays prose in the guidance template around the slot. A `render --check`-style byte-compare guards the generated fragment against hand edits (the same guard `<task>.md` already has).

The result closes both drifts the ask names: agent-vs-prose (the agent runs the tool) and code-vs-prose (the constant lives once in the spec; validate and the driver execute it and the AGENTS.md sentence is generated from it).

### 2.4 What the spec deliberately does NOT hold

No finding-validity rule, no risk-classifier, no trivial/non-trivial decider (those are judgment INPUTS). No arbitrary transition graph as data (the transition FUNCTION is Rust; only the constants/sequences it reads are data). No isolation mechanism (the tool emits the resolved tier; the orchestrator isolates). This keeps the spec a fixed-schema control table, not a Turing-complete process DSL (Principle 2; the tool-vs-prose YAGNI line).

## 3. The engine architecture

### 3.1 Module layout

```
src/workflow.rs            existing W3/W4/W5 checker; Stage 2 extracts its streak arithmetic into a shared reconstructor
src/workflow/spec.rs       NEW (Stage 0): WorkflowSpec parse + accessors; the single source of the control constants
src/driver/mod.rs          NEW (Stage 1+): the `next` entry; output types (JSON + human); stateless recompute orchestration
src/driver/reconstruct.rs  NEW (Stage 2): build the per-unit fleet from PlanToml + round log + ledger + spec
src/driver/fsm.rs          NEW (Stage 2): disjoint Convergence ReviewLoop / SinglePassReview machines with total typed transitions; TaskMachine; QuestionMachine; StepMachine
src/driver/schedule.rs     NEW (Stage 3): the ready-frontier scheduler over blocker policies
src/driver/emit.rs         NEW (Stage 2): fill the next-instruction prompt from the spec's role/path templates
src/driver/record.rs       NEW (Stage 5): the guarded, transition-validating record-* write-path
```

The driver lives in its own `src/driver/` tree (parallel to `src/plan/`), reusing `plan::` (status, risk class, ordinary `blocked_by`, and typed blocker policies), `metrics::` (round parsing), `workflow::` (the shared reconstructor), and `workflow::spec::WorkflowSpec`. It owns no JSON parsing of its own (reuses `metrics::parse_rounds`) and no plan parsing of its own (reuses `PlanToml`), mirroring how `workflow.rs` already reuses both.

### 3.2 The review-process machines (the core types)

The core is one disjoint process enum, not one struct whose acceptance/review instances carry unused convergence fields. Plan and work review are convergence loops; acceptance and standalone review are single passes. Both retain the high/critical dismissal re-check, but only convergence has a class, streak, foreclosure, or cap.

```rust
// driver/fsm.rs
#[derive(Clone, PartialEq, Eq)]
enum ReviewProcess {
    Convergence(ReviewLoop),
    SinglePass(SinglePassReview),
}

enum ConvergencePhase { PlanReview, WorkReview }
struct ReviewLoop {
    id: ConvergenceLoopId,         // exact phase-bearing Roadmap/task identity
    phase: ConvergencePhase,
    risk_class: RiskClass,         // authoritative declaration fixed before round one
    round: u32,
    consecutive_clean: u32,
    awaiting: ConvergenceAwait,
    status: LoopStatus,
}
enum ConvergenceAwait { Round, Recheck, Human, None }
enum LoopStatus { Running, Converged, Escalated, Retired }

enum SinglePassPhase { Acceptance, Review }
struct SinglePassReview {
    id: SinglePassId,              // exact task/artifact + single-pass phase
    phase: SinglePassPhase,
    awaiting: SinglePassAwait,
    status: SinglePassStatus,
}
enum SinglePassAwait { Pass, Recheck, None }
enum SinglePassStatus { Running, Settled, Shortfall, Retired }

// JUDGMENT inputs the tool consumes; neither transition manufactures one.
enum ConvergenceInput {
    Open { declaration: LoopDeclaration },
    RoundResult { outcome: RoundOutcome, top_dismissed: Option<Severity> },
    RecheckResult(RecheckResult),
    HumanDecision(HumanDecision),
    Abandon,
}
enum SinglePassInput {
    Open,
    PassResult { result: SinglePassResult, top_dismissed: Option<Severity> },
    RecheckResult(RecheckResult),
    Retire,
}

enum Output { SpawnRound, SpawnPass, RequireRecheck, RouteFix, Settled, Converged, Escalate, Retire }

fn step_convergence(loop_: &ReviewLoop, input: ConvergenceInput, spec: &WorkflowSpec) -> (ReviewLoop, Output);
fn step_single_pass(pass: &SinglePassReview, input: SinglePassInput, spec: &WorkflowSpec) -> (SinglePassReview, Output);
```

`step_convergence` is the convergence table the FSM lens intended: clean advances the streak, `new_valid` resets it, convergence tests `spec.required_streak(risk_class)`, foreclosure/cap use the current segment with convergence-before-cap precedence, `HumanDecision::Resume` resets counters, and a dismissal at or above `spec.backstop_severity()` blocks in `ConvergenceAwait::Recheck`. Only `Open { declaration }` can supply `risk_class`, so the function has no branch that manufactures or lowers it.

`step_single_pass` never accepts a declaration or class. `SinglePassReview` has no round counter, current/required streak, foreclosure, cap, convergence, or escalation state, so those states are unconstructible. It still gates a high/critical dismissal in `SinglePassAwait::Recheck`: `upheld` settles the original pass result, while `overturned` routes the finding or acceptance shortfall as valid. A lower dismissal or zero-findings pass settles directly. Metrics events may retain descriptive acceptance/review snapshot fields for append-only compatibility, but reconstruction does not transfer them into this type.

Both functions are total over their own typed state/input product, and `ReviewProcess` dispatch is exhaustive. A cross-kind input is not a legal call; adding a process, state, or input variant produces a compile failure until handled. Neither function manufactures an outcome, risk class, re-check result, or human decision, so the type system enforces both the control/judgment boundary and the single-pass/convergence boundary (Principle 5, Principle 18).

The task and step machines nest a process rather than duplicating it:

```rust
struct TaskMachine { phase: TaskPhase, review: Option<ReviewProcess> }
struct QuestionMachine { id: QuestionId, status: QuestionStatus, phase: Exploration }
struct StepMachine { slug: String, status: StepStatus, phase: Option<StepPhase>, review: Option<ReviewProcess> }
```

These are the three legal active-work scopes established across `structured-risk-class-source` and `workflow-loop-visibility`: task review phases, question-scoped exploration independent of any Roadmap step, and step plan-review/exploration/implementation/work-review phases with their exact review identity. Task and live increment plan-review machines resolve live declarations; exact-step and Q-81 Roadmap-increment plan review are retained only as non-active historical reconstruction. Roadmap plan review never changes implementation status or becomes work review. Acceptance and standalone review instantiate `SinglePassReview` and cannot borrow any convergence class. `StepMachine::status == Complete` is reachable in reconstruction only through its embedded work-review `Convergence` process reaching `Converged` (or a covering waiver); a plan review does not complete implementation. Thus "complete without work-review convergence" stays unrepresentable by construction, the same invariant W3 checks post-hoc (Principle 5, 8).

### 3.3 The state-reconstruction layer

```rust
// driver/reconstruct.rs
struct Fleet { tasks: Vec<TaskMachine>, questions: Vec<QuestionMachine>, steps: Vec<StepMachine>, reviews: Vec<ReviewProcess> }
fn reconstruct(plan: &PlanToml, log: &str, ledger: Option<&str>, spec: &WorkflowSpec) -> Fleet;
```

`reconstruct` is stateless: it re-derives every instance each call from durable files, exactly as `workflow.rs` re-derives review state today (no `.fsm-state` file; Principle 4, 7; survives compaction). It consumes the shared `ReviewProcessHistory` from `review-loop-foreclosure-enforcement`, not its own grouping. A convergence process therefore already carries exact phase, Roadmap-increment/task declaration, selected active identity, matched snapshots, and segmented arithmetic. Acceptance/review arrive as `SinglePassHistory` with re-check state but no declaration/class/streak/cap fields. Digest-pinned Q-81 Roadmap-increment plan review, exact-step plan review, and unowned work review remain retired diagnostics and cannot become `ReviewProcess`. The selected Q-58 carrier supplies the transient the log alone cannot give: which artifact/pass is open and the applicable awaiting input. If durable sources disagree, `reconstruct` reports the disagreement rather than choosing one.

### 3.4 The dependency scheduler

The focused `docs/plans/agent-scaffold.steps/workflow-ready-frontier-scheduler.md` sidecar is the Stage-3 implementation authority; this architecture records the aligned shape and does not define a competing function.

```rust
// driver/schedule.rs
fn ready_frontier(steps: &[StepMachine]) -> Vec<&StepMachine>;
// candidates are exactly NotStarted/Next Roadmap steps;
// an ordinary blocked_by target is satisfied by Complete or Skipped;
// an unwaived complete-only proof target also requires round-backed convergence.
```

The pure function operates over one domain: declaration-ordered `NotStarted`/`Next` steps whose ordinary `blocked_by` targets are all `Complete` or `Skipped` and whose typed `complete-only-unwaived` proof targets are `Complete`, directly converged at their declared risk-class bar, and carry no step or increment convergence waiver. `Optional`, `Deferred`, `InProgress`, `NotStarted`, and `Next` blockers remain unsatisfied for either policy; `Skipped`, roundless or below-streak `Complete`, and waiver-backed `Complete` remain unsatisfied for the exceptional policy. Task/Roadmap plan review, task acceptance/review, question exploration, and in-progress step actions sit outside this pending-step frontier. An explicit active-unit action takes selected-action precedence and the ready frontier is reported beside it as advisory parallel work; only when no explicit unit is actionable does the first frontier member replace the Stage-1 pending fallback as serial selection. Therefore selected-action membership is conditional on selection origin, not universal. The tool proposes; the orchestrator decides fan-out against its isolation budget. Step granularity only: increments carry no blocker edge or policy, so no increment-level scheduling.

### 3.5 The instruction-emission layer

```rust
// driver/emit.rs
struct Instruction {
    unit: String, state: String, valid_transitions: Vec<String>,
    isolation_tier: String,          // resolved from spec [isolation].tier_order + the passed harness capability
    next: NextAction,                // role prompt path + filled context slots + principle reminders
}
fn emit(unit: &UnitState, plan: &PlanToml, spec: &WorkflowSpec, ledger: Option<&str>) -> Instruction;
```

`emit` fills a FIXED slot structure (no prose synthesis): the role prompt path from `[roles]`, the findings/ledger/exploration paths from `[paths]` with `{task}`/`{step}`/`{role}`/`{disambiguator}` substituted, the diff range and artifact from the ledger, and a short principle-reminder list keyed to the phase. It is parameterized assembly, exactly what the io-contract lens specified, and it removes a transcription-error surface (the path templates are single-sourced in the spec).

## 4. The I/O surface

Read-only advisory command, reusing the existing clap patterns (`--source`, `--metrics`, `--json` already exist on `status`/`validate`):

```
agent-scaffold next
  --source docs/plans/<task>.plan.toml     # PlanToml (step status, risk class, blocker policies)
  --metrics docs/metrics/workflow.jsonl     # round/escalation/decision log (defaulted)
  [--ledger docs/plans/<task>.ledger.md]    # the transient RESUME STATE + in-flight round
  [--workflow-spec .agents/workflow.toml]   # defaulted; falls back to WorkflowSpec::builtin()
  [--unit <step-slug>]                      # narrow to one unit
  [--isolation-tier container|worktree|file_safety]  # harness capability; echoed into instructions
  [--json]
```

Output (JSON and human text, sharing one structure): per-unit `ready` / `blocked` / `in_review` / `escalated` lists, each with current state, valid transitions, resolved isolation tier, and the filled `next_instruction` (role prompt path + context slots + principle reminders). `drive` is NOT a separate stateful REPL: it is the same stateless computation (reject the in-memory-state REPL, io-contract Option C, because a persistent process defeats crash/compaction survival). If a `drive` verb is wanted later it is a thin loop that re-invokes the same `next` computation, not a daemon.

Later write-path (Stage 5), guarded: convergence-only `record-round --outcome clean|new_valid`, single-pass `record-pass --result met|shortfall`, `record-recheck`, `record-decision`, `record-override --to <state> --reason <text>`, and `record-abandon`. Each validates the transition is legal from the reconstructed state (via `step`), APPENDS the existing `metrics` JSONL record (reusing the shipped schemas), and prints the new state; it exits non-zero on an illegal transition. Overrides are FIRST-CLASS recorded transitions (a logged event into `step`'s total landing state), so a forced move is audited, never a bypass (fsm lens's escape-hatch invariant).

## 5. The incremental build path

Each stage is a reviewable increment that ships value and de-risks the next. The spec (Stage 0) is what keeps the workflow editable-as-data, so the later stages do not harden a moving target (the skeptic's strongest objection, answered structurally).

- Stage 0a: the spec + single-sourced constants. Add `src/workflow/spec.rs` (`WorkflowSpec` + `builtin()`), the `.agents/workflow.toml` pack asset, and `--workflow-spec` on `validate`; replace `RiskClass::required_streak`'s hardcoded `match` with a spec lookup and thread the spec into `w3_problems`; add the round cap as `spec.round_cap()`. Risk class: RISKY (touches the safety-relevant convergence bar and adds a scaffolded asset all downstream projects inherit), but the change is behaviour-preserving and guarded by the existing W3 tests plus the `builtin()`-equals-old-constant assertion. Deps: none (builds on shipped structured-skeleton + validate). Value even if the driver is never built: closes the live `required_streak`/AGENTS.md duplication.
- Stage 0b: generate the AGENTS.md control fragment. Add a `{{workflow_control}}` slot to the pack guidance template and a `render_workflow_control(spec)` that emits the streak/cap/severity/tier/path fragment (constants only); guard it with the byte-compare check. Risk class: RISKY (the code-vs-prose closure; the generation-quality piece the skeptic flagged). Deps: 0a. Proves the generation approach on the smallest, highest-value content before it is widened (Stage 4).
- Stage 1: the advisory `next` MVP (read-only). For the SINGLE active loop, forward-project the streak/cap arithmetic (reusing the W3 reconstruction) to emit current state + valid transitions + next-action + principle reminders, JSON + human. No typed fleet, no scheduler, no prompt-filling beyond naming the role and paths from the spec. This is largely the already-planned `state-queries` step (Q-28/Q-34) plus the next-action reminder. Risk class: LOW_RISK (read-only, no write path, reuses parsers). Deps: 0a (reads the spec). Value: the point-of-action reminder that captures most anti-drift value, and the evidence-gathering tier for every later gate.
- Stage 2: the typed FSM engine. Consume the shared declaration/selection and disjoint review-process reconstruction delivered by focused predecessor steps; do not extract a second declaration lookup, phase/identity selector, process classifier, or streak/cap formula under `src/driver/`. Then add `driver/fsm.rs` (`ReviewProcess::{Convergence, SinglePass}` with total typed transitions), `driver/reconstruct.rs` (the full task/question/step fleet), and `driver/emit.rs` (filled instruction prompts from spec templates). `next` is driven by the typed fleet and emits filled prompts. Risk class: RISKY (core logic; must match the checker exactly). Deps: Stage-1 advisory surface plus focused visibility, Q-58/Q-59 carrier, and foreclosure-reconstruction predecessors named by `workflow-driver-typed-fleet`. Value: full per-unit state with illegal cross-process states unrepresentable.
- Stage 3: the dependency scheduler. Add `driver/schedule.rs`; `next` reports the focused sidecar's step-only ready frontier beside any explicit task/question/step action, with explicit-action precedence and the first frontier member as serial fallback only when no explicit action exists. Risk class: the scheduled focused increment declares `risky`; that declaration supersedes this retained design's earlier LOW_RISK estimate. Deps: Stage 2. Q-82 supersedes the former real-parallelism gate for the typed fleet and read-only scheduler only; write-path and authoritative-driving gates remain.
- Stage 4: widen the AGENTS.md generation. Extend 0b from the constants to the sequencing/paths/tiers fragments. Risk class: RISKY (generation quality across more content). Deps: 0b proven. GATE: only after 0b shows the generated constant fragment is correct and readable.
- Stage 5: the guarded write-path (`record-*`). Add `driver/record.rs`: transition-validating append subcommands. Risk class: RISKY (a runtime write dependency; deliberately reopens the Q-24 no-write-path stance). Deps: Stage 2 (needs `step` to validate transitions) + advisory-adoption evidence from Stage 1. GATE: only once agents demonstrably run `next` consistently and hand-writing JSONL is the remaining gap.
- Stage 6: authoritative driving. Docs instruct agents to obey the tool; escape hatches (`record-override`) mandatory; measure the override rate. Risk class: RISKY. Deps: Stage 5 + MEASURED residual control-drift after the advisory tier. GATE: the skeptic's full evidence gate (measured drift, workflow stability, real concurrency, generation proven).

PRE-Q-82 ORDERING HISTORY: the earlier recommendation was `0a -> 0b -> 1 -> 2 -> {3, 4, 5} -> 6`, stopped the committed near-term path at Stage 2, and held Stages 3/4/5/6 behind evidence gates. Q-82 supersedes that sentence for the typed fleet and read-only scheduler. The current scheduled path is `0a -> 0b -> 1 -> 2 -> 3`; only Stages 4 through 6 remain gated. Stage 4 waits on the constant-fragment generation proof, Stage 5's write path waits on measured advisory adoption and reopens Q-24, and Stage 6 authoritative driving waits on a measured-low override rate. Stage 3 neither writes nor drives authoritatively.

## 6. Key risks and pitfalls in the build

- State-reconstruction ambiguity. The round log gives completed rounds but not the `awaiting` field (waiting for the next round vs mid-recheck vs blocked on a human). Resolve via the ledger `## RESUME STATE` transient plus a TOTAL transition function so every replayed state is defined; if ledger and log disagree, REPORT it (do not silently pick one). Pitfall: inferring `awaiting` from the log alone would guess, and a wrong guess emits the wrong instruction.
- The control/judgment and process-kind boundaries in code. The primary failure modes are computing a verdict/risk class or smuggling convergence arithmetic into a single pass. Enforce by TYPES: risk reaches only `ReviewProcess::Convergence` through the authoritative phase-bearing declaration selected at `Open`; verdicts/re-check/human decisions arrive as typed inputs; and neither transition invents judgment. `SinglePassReview` cannot construct class, streak, foreclosure, cap, or convergence, while both variants retain the backstop re-check. Test judgment provenance and compile-fail cross-kind access. Get this wrong permissively and the tool hallucinates decisions/evidence; restrictively and it straitjackets.
- Test strategy for a state machine. (a) Exhaustive transition-table tests: every `(state, input)` pair has a defined image (the function is total). (b) A DIFFERENTIAL test against the shipped checker: replaying a round log forward through `step`/`reconstruct_loop` must yield the SAME streak `round_log_consistency_problems` computes, so the driver and the validator provably cannot diverge (this is the highest-value test and the reason to extract the shared reconstructor in Stage 2). (c) Golden fixtures for `next` output (JSON and human), like the render golden compares. (d) A round-trip: `reconstruct -> emit` yields paths that match the spec templates.
- Keeping it stateless. No persisted FSM store; recompute from plan + log + ledger + spec every call (Principle 4, 7; survives crash/compaction). Pitfall: any cache or `.fsm-state` file is a second source of truth that reintroduces the drift the initiative removes (Principle 8, 16).
- Spec bootstrapping. The spec is the source, but Rust needs `WorkflowSpec::builtin()` when no `.agents/workflow.toml` is present; a compile-time / test assertion must pin `builtin()` to today's constants so an un-migrated project validates identically (Principle 3, 5).
- Over-fitting the FSM to a molten workflow. Keep transition KINDS in Rust but all CONSTANTS / sequences / paths / tiers in the spec, so workflow evolution is a data edit and only a genuinely new transition KIND (rare) touches Rust. This is the concrete mechanism that answers the skeptic's "pouring concrete around a moving design": the concrete is the spec's fixed SCHEMA, not the workflow's values.

## 7. Trade-offs against the numbered Principles

- Principle 1 (cleaner long-term architecture): FOR the staged full driver. The `src/driver/` tree with a spec-parameterized total transition function, reusing `plan`/`metrics`/`workflow`, is the clean third stage of the structured-data direction. The staging keeps each increment reviewable (Workflow Principle small-and-reviewable) rather than one big-bang subsystem.
- Principle 2 (minimal by default): tension, resolved by staging and the YAGNI gates. PRE-Q-82, the near-term path stopped at 0a/0b/1/2 and called the scheduler gated. Q-82 superseded that part: Stage 3's focused read-only scheduler is scheduled after the typed engine. Generation widening, the write path, and authoritative driving remain Stages 4-6 behind their distinct gates, so no write or authority expansion ships early.
- Principle 3 (safe on existing projects): `WorkflowSpec::builtin()` and the read-only `next` keep existing projects byte-for-byte unaffected until they scaffold the new asset; the write-path (Stage 5) is the only stage that changes the runtime contract, and it is gated.
- Principle 4 (idempotent) and Principle 7 (reproducible): stateless recompute makes `next` deterministic and repeatable; the same files always yield the same output.
- Principle 5 (illegal states unrepresentable): the nested fleet + total `step` make "complete without convergence" and undefined transitions unrepresentable by construction, strengthening the post-hoc W3 check into a type-level invariant. This is the driver's strongest principled argument and the reason to type the engine (Stage 2) rather than stay ad-hoc.
- Principle 6 (evidence-first): the whole staging is the evidence gate. Stage 1 (advisory) is the pilot; Stages 5/6 escalate only on measured drift, mirroring the receipt/waiver pilots. Building 5/6 before Stage 1's measurement would invert this.
- Principle 8 (structured data first, project for humans): the spec IS this principle applied to the process (control data projected to the AGENTS.md human view); it reuses the render/pack machinery rather than inventing a parallel one.

Net: the principles about clean structure and unrepresentable illegal states (1, 5, 8) pull toward the typed full engine; the principles about minimalism and evidence (2, 6) pull toward staging and gating. The staged path satisfies both: build the data-driven core now, gate the concrete-pouring parts on evidence.

## 8. Recommendation

PRE-Q-82 RECOMMENDATION HISTORY: commit to 0a -> 0b -> 1 -> 2 and hold 3/4/5/6. Q-82 supersedes only the Stage-3 hold. The current recommendation is to complete the scheduled `0a -> 0b -> 1 -> 2 -> 3` path and hold Stages 4-6 behind their existing evidence gates: generation proof for Stage 4, advisory adoption plus Q-24 reopening for the Stage-5 write path, and measured-low override rate for Stage-6 authoritative driving.

- Build the `workflow.toml` spec and single-source the convergence constants FIRST (0a), then generate the AGENTS.md control fragment from it (0b). This closes the existing duplication, establishes the data-driven substrate the human asked for, and de-risks generation on the smallest content, all independently valuable even if the engine is never finished.
- Build the advisory `next` MVP (1) on the spec + the W3 reconstruction; it is barely-new scope over the already-planned `state-queries` step and is the point-of-action anti-drift tier plus the evidence source for every later gate.
- Build the typed FSM engine (2) on the already reviewed shared reconstructor, then add disjoint `Convergence(ReviewLoop)` / `SinglePass(SinglePassReview)` processing, task/question/step machines, and instruction emission. This realizes the full driver's core with illegal cross-process states unrepresentable.
- Treat the driver as COMPLEMENTING the re-grounding step and Q-50, not subsuming them; un-gate those (Q-50 is a prerequisite if generation and prompt-filling are to be correct).

This honours the human's "full driver as the target" while staging it so no stage hardens the still-evolving workflow (the workflow evolves by editing `workflow.toml`, not Rust), and so each increment ships value and de-risks the next.

## 9. YAGNI boundary (what NOT to build)

- No persisted FSM state and no stateful `drive` daemon/REPL; recompute statelessly from the files each call.
- No global product FSM and no Harel statechart; the nested fleet + stateless recompute has the needed power with less machinery.
- No increment-level DAG scheduling; the scheduler is step-granularity only (increments carry no blocker edge or policy).
- No general workflow DSL; `workflow.toml` holds THIS workflow's fixed constants/sequences/paths/tiers, not arbitrary process logic. A new transition KIND is a code change, not a spec field.
- No judgment in the spec or in `step`; verdicts and human decisions are only ever typed inputs, and a risk class enters only from the plan declaration selected for the exact convergence-loop identity. No first-round, declaration-order or latest-round inference.
- Do not generate the WHOLE AGENTS.md workflow section; generate only the control fragments and keep the rationale/role/contract prose hand-authored (0b/Stage 4 are the constant fragments, not the "why").
- Do not build Stages 4-6 before their gates: the constant-fragment generation proven for the widening (4); measured advisory adoption for the write-path (5, which reopens Q-24 deliberately); measured residual drift + workflow stability for authoritative driving (6). Q-82 has already lifted the former real-parallelism gate for the typed fleet and read-only scheduler only.
</content>
</invoke>
