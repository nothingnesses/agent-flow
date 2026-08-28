# Q-86 synthesis round 1 triage

## Scope and reproduction

I independently read `AGENTS.md`, `.agents/prompts/triager.md`, the complete Q-86 brief, both explorer proposals, the synthesis, its Q-86 TOML/sidecar/generated-plan fold, the Success Criteria source, the ledger resume anchor, and both reviewer reports. The reviewed change is `main..HEAD`: five planning files, including the new synthesis. No reviewed product was edited.

I reproduced the relevant evidence in this worktree. Extracting and running the state-machine proposal's checker returns `KC Complete 2 1 0`, `KCC Complete 2 1 0`, `KCC Complete 3 2 0`, and `KCC Complete BlindClosure 3 0`; the exhaustive runs still report zero failures because they retain only the latest `critical` scalar. Extracting and running the safety proposal's `m2` model reports `ceiling=4`, `obligations=2`, and 107 reachable states. The Q-78 selector returns ten passes with `[7,10,5,6,5,5,4,2,1,0]`; its scope-addition selector identifies passes 2, 4, 7, and 8. `nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` and `... validate --source docs/plans/agent-scaffold.plan.toml --workflow` pass. Those general checks do not prove the design properties below.

## Deduplication and result

Nineteen raw reviewer findings consolidate to seventeen: `Q86-R1-GPT-2` and `CR-1` are one missing/contradictory Option B controller proof, and `Q86-R1-GPT-3` and `CR-8` are one stale Success Criterion. Thirteen consolidated findings are valid: three high, seven medium, and three low. Four are invalid. No finding is accepted as residual.

**Round outcome: `new_valid`.**

No high- or critical-severity finding was dismissed. Therefore **no independent dismissal backstop re-check is owed**.

## Consolidated verdicts

### T1 — The A/C exhaustive oracle erases an unresolved critical

- **Reviewer source IDs:** `Q86-R1-GPT-1`
- **Verdict and severity:** valid, **high**.
- **Reproduced evidence:** `docs/plans/workflow-calibration.explorations/Q-86-state-machine.md:441-455` assigns `critical = 0` for every later `C`, `O`, `R`, `L`, or `H`; `:475-487` replaces it on every fixed-depth observation. The extracted checker consequently completes `KC`, `KCC`, and the fixed-depth `KCC`, although a first critical has received neither a repair nor verification. The proposal explicitly concedes the abstraction at `:554`. The synthesis nevertheless says the enumerations proved no critical completion for A and C at `Q-86-synthesis.md:103,183` and that all red controls pass at `:213`.
- **Reasoning:** the checker demonstrates termination of its toy observation stream, not the required unresolved-critical invariant. A later unrelated observation cannot settle an earlier critical. The brief requires a toy state machine to demonstrate that invariant before recommendation eligibility, so the synthesis cannot present this one as that proof.
- **Required correction:** replace the scalar with prospective finding/disposition state in the actual A and C transition models; allow an open critical to leave the open set only through explicit repair plus verification, or an explicit non-delivery terminal disposition; exhaust those models. Until then, state only the termination proof and remove the claim that the critical red control mechanically passed.

### T2 — Option B has no single controller whose bound or proof matches its text

- **Reviewer source IDs:** `Q86-R1-GPT-2`, `CR-1`
- **Verdict and severity:** valid, **high**.
- **Reproduced evidence:** Option B gives each obligation an “initial closure attempt” and at most one reopen at `Q-86-synthesis.md:126`, but then permits a reopen only for materially new evidence and says a finding against a *closed* obligation uses it at `:130`. It never says which transition gives an obligation whose first attempt produces a valid finding its next attempt. Its cited M2 oracle hard-codes `CAP = 4` and `OBL0 = 2` at `Q-86-safety-process.md:568-580`; it has no per-obligation attempt/reopen, phase, or blind-closure state. Its M2 branch decrements the obligation count for clean, low, and medium observations at `:626-640`, rather than representing the synthesis's typed attempt/disposition transitions. The reproduced run reports the claimed 107 states, but that proxy neither uses `r` nor derives `2|O| + 1`.
- **Reasoning:** these are one cause and consequence: the recommended composed controller is neither unambiguous nor the controller the 107-state run checked. Thus the stated derived ceiling and its claimed red-control proof are not established. This is decision-material because B is the recommendation and its derived bound is presented in the human ask.
- **Required correction:** specify one finite `FrozenObligationCampaign` state machine before treating B as recommendation-eligible. It must distinguish an initial attempt from a reopen; define every valid-finding, repair, verification, close, reopen, serious-block, blind-closure, and terminal transition; retain finding dispositions; bind attempts to obligation and phase identities; and derive `2|O| + 1` and `2|O| + 8` from those transitions. Exhaust the actual parameterized controller and either validate the claimed bounds or withdraw them and B's recommendation pending the proof of concept.

### T3 — The Success Criteria still require the superseded `exploring` state

- **Reviewer source IDs:** `Q86-R1-GPT-3`, `CR-8`
- **Verdict and severity:** valid, **medium**.
- **Reproduced evidence:** `docs/plans/agent-scaffold.success-criteria.md:41` says the in-progress step “keeps Q-86 `exploring`” and schedules the brief. The current fold says Q-86 is `open` in `docs/plans/agent-scaffold.plan.toml:2560-2573` and `docs/plans/agent-scaffold.steps/workflow-calibration.md:20`; the rendered plan projects both claims. Strict render passes only because it faithfully projects the stale Success Criteria sidecar.
- **Reasoning:** the plan's acceptance condition now contradicts the changed plan state and the completed synthesis. This is durable documentation staleness, not a renderer problem.
- **Required correction:** update the Success Criteria source to require the completed synthesis and Q-86 `open`, while retaining the block on implementation until the human decision is receipted and folded; re-render and run strict render check.

### T4 — The recommended Option B was not replayed against the Q-78 scope changes it claims to address

- **Reviewer source IDs:** `CR-2`
- **Verdict and severity:** valid, **high**.
- **Reproduced evidence:** the Q-78 selector identifies scope additions on acceptance passes 2, 4, 7, and 8. Option B freezes `O` after plan review at `Q-86-synthesis.md:126`, makes scope-expanded work unable to enlarge `O` at `:130`, and promises mechanical “no scope mutation” at `:151`. The synthesis contains no B replay assigning a typed transition and durable result to those four events, despite relying on the moving-target diagnosis at `:143,226`.
- **Reasoning:** each event must either end the family/replan, be a legitimate pre-existing obligation, or be an illegal addition. The recommended mechanism's adoption cost and safety outcome on the only local sequence cited to justify it are therefore unknown. The lack is not repaired by the generic red-control row, which does not replay the historical events.
- **Required correction:** after T2 supplies the actual B controller, replay all ten Q-78 passes against it. For each of the four scope additions, record the exact transition, whether delivery is terminally replanned or otherwise blocked, and the resulting finding/obligation state. Put the result and its cost in the option's trade-offs and the human-facing summary.

### T5 — The human-facing comparison omits the quantitative A/C replay and overstates its ranking

- **Reviewer source IDs:** `CR-3`
- **Verdict and severity:** valid, **medium** (reduced from high).
- **Reproduced evidence:** the state-machine proposal reports Candidate A terminal at pass seven with a medium finding at `Q-86-state-machine.md:221,357`, and Candidate B terminal at pass three with a high finding at `:316,357`. In the synthesis, C only carries the qualitative pass-three statement at `Q-86-synthesis.md:182`; A's result and both quantitative tails are absent. The plan ask nonetheless calls A the option with “the most bounded late discovery” at `docs/plans/agent-scaffold.plan.toml:2571`. From the live Q-78 counts, stopping A at pass seven leaves three later valid shortfalls, worst low. Stopping the fixed-depth C controller at pass three leaves 23 later valid shortfalls, worst high. The reviewer's alternative C pass-four/17 figure belongs to the safety proposal's separate pure-count M1 replay, not Option C, so it is not carried forward here.
- **Reasoning:** the synthesis does not need to reproduce every explorer table, but it does need to substantiate the comparative claim supplied to the human. The omitted exact A/C replays are the available local evidence for late discovery; B's result remains separately blocked on T2/T4.
- **Required correction:** add the corrected A and C Q-78 replay results to the red-control/trade-off comparison, add B's result once its controller is specified, and qualify or remove “most bounded late discovery” unless the same comparison establishes it across all three options.

### T6 — The serious terminal floor is a hidden human-policy choice

- **Reviewer source IDs:** `CR-4`
- **Verdict and severity:** valid, **medium**.
- **Reproduced evidence:** the synthesis selects `high` as the floor at `Q-86-synthesis.md:65`, making residual acceptance and ordinary narrowing illegal for open highs at `:69-70`. Its no-decision boundary at `:236` names the A and B numeric constants but not the floor; the TOML ask likewise does not name it. The safety proposal calls `F` a safety-appetite decision not derivable from the data at `Q-86-safety-process.md:516-520`.
- **Reasoning:** choosing an architecture would silently also choose a substantive terminal-menu restriction. A conservative default may be recommended, but the human-input contract requires the human to see the decision and its cost.
- **Required correction:** present `high` as a named co-decision with its Q-78 consequence and recommendation, or explicitly defer the floor to a separate human decision before implementation. In either case include it in the no-decision boundary and the Q-86 ask so it cannot be approved implicitly.

### T7 — Option B's no-transfer partition has no allocation or minimum-review rule

- **Reviewer source IDs:** `CR-5`
- **Verdict and severity:** valid, **medium**.
- **Reproduced evidence:** `Q-86-synthesis.md:128` partitions the whole post-freeze `C_O = 2|O| + 1` among `m` work loops and acceptance with no transfer, but states neither an allocation rule nor a relation between `|O|` and `m`. For the permitted but unspecified case `m = 3`, `|O| = 1`, there are three post-freeze batches for four sub-accounts; at least one account receives zero. The same line says an exhausted sub-account reaches the terminal decision.
- **Reasoning:** the stated controller can terminally foreclose a declared work loop before it receives a batch. This is distinct from the overall bound proof: even a correct total is insufficient if phase partitioning makes normal work impossible.
- **Required correction:** define a source-owned phase allocation for every obligation and blind-closure batch, require a legal minimum allocation for each declared post-freeze loop (or reject an impossible freeze), recompute the total/call bounds from that allocation, and include zero/one-allocation red controls in the B state model.

### T8 — Option B does not define a closed, mechanically enumerable source for `O`

- **Reviewer source IDs:** `CR-6`
- **Verdict and severity:** valid, **medium**.
- **Reproduced evidence:** the safety proposal deliberately defines exactly three source artifacts at `Q-86-safety-process.md:240-244`; the synthesis instead says the source “cites” eight broad categories at `Q-86-synthesis.md:56`, including unlocated invariants, trust boundaries, exclusions, and a reviewed baseline. Yet it claims `validate --workflow` will enforce exact source joins at `:151` and derives its bound from `|O|` at `:128`. No extraction/normalization rule states what finite rows any of the broad categories supply.
- **Reasoning:** widening the design may be sound, but the current wording leaves the cardinality and membership of `O` author-defined without a checkable boundary. That defeats the claimed exact joins and leaves the recommendation's central derived input underspecified.
- **Required correction:** define one closed source map and deterministic extraction rule for obligation rows, with stable source locators. It may retain broader coverage only if each category resolves to an explicitly finite structured source; otherwise restore the three-source boundary. Make the map and the resulting finite `O` an input to T2's model and validation claims.

### T9 — The severity-gate exclusion is not internally inconsistent

- **Reviewer source IDs:** `CR-7`
- **Verdict and severity:** invalid; no defect severity.
- **Reproduced evidence:** the exclusion at `Q-86-synthesis.md:218` concerns a multi-pass severity trajectory reconstructed from incomplete historical instrumentation. The shared floor instead uses prospective per-finding `Severity` state at `:59,65`. The synthesis already distinguishes the untrustworthy historical severity arrays at `:31-34` from prospective structured state.
- **Reasoning:** both policies consult a word named “severity,” but they do not consume the same evidence or make the same terminal inference. The proposed clarification could improve exposition, but the cited text establishes a coherent distinction and does not invalidate the option set.
- **Required correction:** none.

### T10 — The failed-proof fallback pre-authorizes a different architecture

- **Reviewer source IDs:** `CR-9`
- **Verdict and severity:** valid, **medium**.
- **Reproduced evidence:** `Q-86-synthesis.md:228` says that if B's focused proof of concept fails, “choose `A - Sealed phase budget`,” whereas `:232-236` and the TOML ask require the human to choose exactly one option and say no mechanism is approved until that decision.
- **Reasoning:** a failed B proof is new evidence against the recommendation and must return to the human; it cannot silently select A. The fallback is sensible advice, but not an authorized transition.
- **Required correction:** change the fallback to reopen the human decision with A as the recommendation, list the proof-of-concept gate in the human-facing ask, and require a new receipt before any A-specific planner fold.

### T11 — “Option C has the lowest maximum cost” compares incomparable parametric bounds as a universal

- **Reviewer source IDs:** `CR-10`
- **Verdict and severity:** valid, **low**.
- **Reproduced evidence:** the ask at `docs/plans/agent-scaffold.plan.toml:2571` calls C the lowest maximum cost. C's stated bound is `15(m + 2)` at `Q-86-synthesis.md:169`; B's is `5(7 + (2|O| + 1)) - 1 = 10|O| + 39` at `:128`. For permitted parameters `m = 3`, `|O| = 3`, those evaluate to 75 and 69 respectively.
- **Reasoning:** C has the lower fixed-depth proof, but its whole-task cost is not universally lower than B's independently parameterized bound.
- **Required correction:** replace the universal cost claim with the accurate per-phase-depth comparison, or state the parameter assumptions under which a whole-task ranking holds.

### T12 — The ledger resume anchor remains stale after Q-86 changed status

- **Reviewer source IDs:** `CR-11`
- **Verdict and severity:** valid, **low**.
- **Reproduced evidence:** the ledger's active `RESUME HERE` paragraph at `docs/plans/agent-scaffold.ledger.md:535` says Q-86 remains `exploring` and points to the brief, while the changed step sidecar says it is `open` and points to the synthesis at `docs/plans/agent-scaffold.steps/workflow-calibration.md:20`.
- **Reasoning:** the ledger is orchestrator-owned and outside this writer's reviewed diff, but it is explicitly a resume source. Leaving the stale anchor undermines durable reconstruction after this status transition.
- **Required correction:** when integrating the resolved synthesis, the orchestrator must move the resume anchor to Q-86 `open`, name the synthesis, and state that the next action is the human decision. This is an integration/ledger correction, not a planner repair to this triage worktree.

### T13 — The final-batch triage/re-check sentence is not a safety contradiction

- **Reviewer source IDs:** `CR-12`
- **Verdict and severity:** invalid; no defect severity.
- **Reproduced evidence:** in `Q-86-synthesis.md:128`, the qualifier “per non-final batch” grammatically applies to the final list item, repair. The separate shared rule at `:75` explicitly makes the re-check structurally available at exhaustion, and the `- 1` in the call formula is consistent with withholding only the final repair.
- **Reasoning:** an alternative reading is possible only by ignoring both ordinary list scoping and the explicit safety rule. The text is not contradictory and does not omit a required transition.
- **Required correction:** none.

### T14 — B has no defined adoption state for active legacy work without a frozen rubric

- **Reviewer source IDs:** `CR-13`
- **Verdict and severity:** valid, **medium**.
- **Reproduced evidence:** the B migration claim says only that active legacy work adopts at a digest boundary at `Q-86-synthesis.md:140,149`. B's ceiling and completion predicate require a frozen `O` at `:126-130`; no state or transition covers a legacy task already past plan review with no `O`. The safety proposal flags the precise compatibility rule at `Q-86-safety-process.md:426`: a tree with no frozen rubric must be exempt rather than failed.
- **Reasoning:** a digest boundary alone does not define `C_O`, phase ownership, or completion for that population. The design must neither manufacture a retrospective rubric nor accidentally make pre-adoption work unbounded or invalid.
- **Required correction:** specify a typed no-rubric legacy state. It must be explicitly historical/exempt rather than a false completion failure; it must not enter or resume a B work/acceptance campaign with undefined `C_O`; and it must state the terminal human-adoption or next-plan-review path that creates a prospective `O` before B starts. Add validation and replay controls for that state.

### T15 — The claimed missing Success Criteria template inventory entry is not established

- **Reviewer source IDs:** `CR-14`
- **Verdict and severity:** invalid; no defect severity.
- **Reproduced evidence:** the synthesis says the plan schema and template gain B obligation rows at `Q-86-synthesis.md:149`; it does not purport to be a path-by-path manifest. The safety proposal's own migration inventory names both `pack/plan-template.plan.toml` and `pack/plan-template.success-criteria.md` at `Q-86-safety-process.md:454`, but the reviewer supplies no evidence that B's stable obligation ids must be authored in the Success Criteria template rather than in the plan rows with source references.
- **Reasoning:** naming a broad template surface is not proof that an unchosen implementation omits a required file. This is a possible implementation consideration, not a demonstrated staleness defect in the decision artifact.
- **Required correction:** none.

### T16 — The synthesis lacks a label map for the proposals it asks the human to consult

- **Reviewer source IDs:** `CR-15`
- **Verdict and severity:** valid, **low**.
- **Reproduced evidence:** `Q-86-state-machine.md:9-12` calls its candidates A (sealed budget) and B (fixed-depth), while the synthesis calls the corresponding options A and C and creates a new B from the safety proposal's M2. The synthesis points readers to both proposals at `Q-86-synthesis.md:47` but supplies no mapping.
- **Reasoning:** the source state-machine proposal recommends “Candidate A,” while the synthesis recommends “Option B.” The mapping is inferable, but a decision document that directs a human to both sources should not require inference across three label systems.
- **Required correction:** add a short mapping near the source references: Option A = state-machine Candidate A; Option B = safety-process M2 plus the sealed envelope; Option C = state-machine Candidate B; and the safety-process M3 is excluded.

### T17 — The two-seat design is an explicit reconciliation, not a silently reversed rule

- **Reviewer source IDs:** `CR-16`
- **Verdict and severity:** invalid; no defect severity.
- **Reproduced evidence:** the safety proposal prefers free breadth at `Q-86-safety-process.md:282`, but the independent state-machine proposal explicitly says no candidate treats diversity as free and uses fixed seats at `Q-86-state-machine.md:149`. The synthesis makes its two-seat choices express at `Q-86-synthesis.md:87,118,128,132` and still states that model/harness diversity is preferred at `:79`.
- **Reasoning:** the synthesis has selected one documented design trade-off rather than hiding a contradiction. The brief requires the cost/diversity interaction to be stated, and exact seats plus preferred diversity meet that requirement. A separate rationale could be helpful, but its absence is not a demonstrated design flaw.
- **Required correction:** none.

## Verification record

- `nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` — passed (`up to date`).
- `nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` — passed (478 records; 114 steps; 87 questions; workflow invariants hold).
- Extracted Q-86 state-machine and safety-process AWK checks plus the Q-78 selectors described above — reproduced the evidence cited in the relevant verdicts.
- `git diff --check main..HEAD` — passed before this triage file was authored.
