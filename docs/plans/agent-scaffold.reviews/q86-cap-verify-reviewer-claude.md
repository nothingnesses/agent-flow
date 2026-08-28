# Q-86 cap-closure focused verification (claude)

## Scope, method, and reproduction

I ran the human-authorised focused verification of the Q-89 `Fix, verify once, then close` decision, independently and in my own worktree, at tip `1419a2de` against `main` (`d9f1f1de`). Per the Q-89 authority I checked **only** the two round-5 low fixes, their direct residue, the exact receipt, and the specific-fix closure path. I did not open the other reviewer's file and I changed nothing outside this file.

I read `AGENTS.md`, the Q-89 structured record and sidecar, the Q-89 receipt, `q86-narrow-r5-triage.md`, the three corrected floor surfaces, the narrowed synthesis, the owning `workflow-calibration` step sidecar, the Success Criteria, the mapped `Q-86-state-machine.md`, and the generated projection.

Baseline checks, both passing:

```sh
nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date
nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
# 492 records, valid; 114 steps, 89 questions, valid; workflow invariants hold
```

`git diff --name-only main...HEAD` touches only `docs/metrics/workflow.jsonl` and `docs/plans/`. No `src/`, `tests/`, `pack/`, `.agents/`, `README.md`, `CHANGELOG.md`, or workflow-spec path changed, so the artefact's own no-behaviour-change claim at `Q-86-synthesis.md:9` holds for this repair as it did for the narrowing pass.

## Fix 1 (round-5 T1): the serious-floor rationale now uses plan Project Principles

**Closed on every surface the correction named, in substance and not only in shape.**

- The affirmative half is now, verbatim and identically, on all three source surfaces — `Q-86-synthesis.md:219`, `Q-86.md:37`, `agent-scaffold.plan.toml:2580`: "`high` is recommended under Make illegal states unrepresentable because an unresolved serious finding has no delivery state, and Safe on existing projects because the stricter boundary fails closed on adoption." Both names are in the plan's set (`[[principle]]` 5 and 3 at `agent-scaffold.plan.toml:2636-2674`). The cost half is preserved unchanged under Ground decisions in evidence and Minimal by default, exactly as `q86-narrow-r5-triage.md:24` required.
- The mapping is sound, not merely nominal. Principle 5 is "work out the valid inputs and outcomes first and encode them": floor `high` removes the delivery state for an open high, which is the illegal-state form of the argument. Principle 3 is the adoption-safety principle, and the artefact already applies it to adoption behaviour in its own comparison table (`Q-86-synthesis.md:173`, `LegacyNoRubric` fails closed / historical stage adoption routes to a human), so the "fails closed on adoption" clause is consistent with the artefact's established use of that name rather than a fresh stretch. This is the wording the round-5 triage itself proposed.
- Both projections carry it: `agent-scaffold.md:179` (the queue line from the structured `ask`) and `:5111` (the Q-86 sidecar section).
- **No residual use of the out-of-set names anywhere live.** `grep -rn 'Make failure and absence explicit\|Correctness before performance'` over the tree returns only (a) the frozen round-5 review and triage records that filed the defect, and (b) the harness-agnostic AGENTS guidance set, which is a different namespace by design: `AGENTS.md:123,128`, `.agents/AGENTS.reference.md:123,128`, and `pack/principles.toml:154,270` with its generated `.agents/principles.toml` copy. No decision surface uses them.
- The contract itself is satisfied at the level it applies. `AGENTS.md:41` requires reasoning "judged against the plan's Project Principles by name"; the Q-89 decision judges itself against **all eight** by name at `Q-89.md:27-34` and `agent-scaffold.plan.toml:2632`, and the floor sub-recommendation now names four in-set principles, two for and two against.

## Fix 2 (round-5 T2): Option C's fifteen-call maximum now derives locally

**Closed, arithmetic correct, published bound untouched.**

- `Q-86-synthesis.md:141` now reads: "Across those four batches, the maximum comprises five reviewer passes (two at Discovery and one each at Verify1, Verify2, and BlindClosure), four triage calls, four backstop calls, and two repair passes, so `5 + 4 + 4 + 2 = 15`." That is `q86-narrow-r5-triage.md:31`'s correction applied word for word, in the triage's own vocabulary ("backstop calls").
- It is faithful to the mapped source rather than invented. The provenance map at `:17` sends C to state-machine Candidate B, and `Q-86-state-machine.md:312` gives "at most four review batches, five reviewer passes, four triage calls, four backstop calls, and two repair passes". The per-node seat split reproduces independently from `:153` ("two blind seats at discovery, one informed seat at each verification, and one blind seat at closure") and the node table at `:274-277`. `2 + 1 + 1 + 1 = 5`.
- The published bounds are unchanged: `R_C = 4(m + 2)` and `I_C = 15(m + 2)` at `Q-86-synthesis.md:144-145`, and the republished figures at `Q-86.md:9`, `agent-scaffold.plan.toml:2567`, `agent-scaffold.md:179` are byte-identical to before. `git diff 196f8e9a..1419a2de` shows no bound edited.
- **The derivation does not contradict anything else C states.** Its two repair generations match `:139` ("at most `Repair1` and `Repair2`"). Its Discovery-two / BlindClosure-one allocation matches the minimum at `:148` (two batches, three reviewer calls) and every C cell in the cost table at `:159,161,162`. The ranking claim at `:165` ("C has the lowest fixed per-phase maximum") is unaffected. The round-5 triage's evidentiary correction — that A's composition at `:89` is A's own allocation, not a rate C inherits — is respected; I did not re-raise it.

## Direct residue

- **Projection currency.** `render --check --strict` reports up to date. Independently, every non-blank line of `Q-86.md`, `Q-89.md`, `agent-scaffold.steps/workflow-calibration.md`, and `agent-scaffold.success-criteria.md` appears verbatim in `docs/plans/agent-scaffold.md` (0 missing of 27, 24, 18, and 40 lines). The Q-86 and Q-89 queue lines equal their structured `ask` with paragraph breaks collapsed, plus the renderer's ` Receipt: \`{receipt}\`.` suffix (`src/plan/render.rs:439`), matching how Q-85, Q-87, and Q-88 project. Anchors: `agent-scaffold.md:179,182,723,5111,5160-5197,5239`.
- **Every surface that had to move, moved.** The step sidecar gains the Q-89 paragraph and the `Q-85`/`Q-86`/`Q-88`/`Q-89` heading (`workflow-calibration.md:18,22,30`); the no-decision boundaries name Q-89's exact authority (`Q-86-synthesis.md:19`, `Q-86.md:43`, `agent-scaffold.plan.toml:2582`, `workflow-calibration.md:30`); the Success Criteria bullet records the five-option receipt and the conditional close (`agent-scaffold.success-criteria.md:41`); the Q-86 `ask` opens with the Q-89 summary (`agent-scaffold.plan.toml:2562`).
- **Nothing became stale.** Sweeping for surfaces that mention Q-88 but not Q-89 returns only the frozen narrowed-round review and triage records, `Q-88.md` itself, and the three exploration inputs — and those three record Q-88's *proof-scope* supersession (`Q-86-state-machine.md:5`, `Q-86-safety-process.md:5`, `Q-86-convergence-mechanism-brief.md:5,7`), which Q-89 does not touch. Q-89 changed only how the capped narrowed artefact is repaired and verified.
- Counts reconcile with the ledger's RESUME STATE claim: 492 log records, 114 steps, 89 questions. No non-ASCII and no wrapped paragraph was introduced in any changed file.

## The exact Q-89 receipt

Exact. There is one `type:"decision"` record with `q_id:"Q-89"`, at `docs/metrics/workflow.jsonl:492`, and commit `654a2b88` adds exactly that one line — which is what `Q-86-synthesis.md:9` claims ("each append exactly one `type: "decision"` event ... without changing the metrics schema or behaviour").

- `options` carries the five labels in the recorded order and matches `Q-89.md:9-13` and `agent-scaffold.plan.toml:2624-2628` label for label.
- `recommendation` and `chosen` are both exactly `Fix, verify once, then close`; `chosen` is a member of `options`, as `AGENTS.md:145` requires.
- `task` is `workflow-calibration`, which is the question's `folded_into`, following the descriptive convention that record states.
- `agent-scaffold.plan.toml:2618-2621` sets `status = "decided"`, `folded_into = "workflow-calibration"`, `receipt = "Q-89"`. `Q-89` is past the `[meta].w4_baseline` cutoff of `Q-44` (`agent-scaffold.plan.toml:3`), so W4 enforces the receipt, and `validate --workflow` passes.
- The escalation that precedes it exists (`workflow.jsonl:490`, `human_decision:"decision"`, `step:"workflow-calibration"`), and the Q-89 receipt is the log's last record.

## The specific-fix closure path

Sound and fail-closed.

- `AGENTS.md:57` provides exactly this branch: "if the decision instead ends the loop (accept the artifact, or send it back for a specific fix that closes this loop), the counters retire with it." Every surface says retire, none says reset: `Q-89.md:30,38`, `Q-86-synthesis.md:7`, `workflow-calibration.md:22`, `agent-scaffold.plan.toml:2630`.
- The closure condition is stated identically and completely on all durable surfaces: the focused verification checks only the two fixes and their direct residue; if it finds nothing new the capped narrowed artefact closes without a second clean round; **any new valid finding returns to the human**. There is no branch that spawns another automatic review round, so the path terminates in one step either way and creates no new unbounded route — which is what the Q-89 rationale claims under Make illegal states unrepresentable.
- The recommendation and the choice coincide and are both option 1 of 5, presented in the order the receipt records, with per-option trade-offs at `Q-89.md:19-23`. The human-input contract's four elements are all present.

## Deferred controller proof, and authority

- **The deferred proof is respected, not re-raised.** The r1-r5 synthesis proof obligations remain open by design; I raised none of them. The prototype boundary at `Q-86-synthesis.md:45-60` is untouched by both fix commits. Fix 2 adds an *allocation derivation* inside the artefact's "proposed" frame, not a proof: `:148` still requires the selected-option proof of concept to establish C's phase typing, every forward transition, both repair generations, mandatory acceptance blind closure, arbitrary finite finding products, scope and dismissal products, terminal floors, and all delivery blocks. Gate item 9 (`:202`) still requires every selected-option bound to be proved.
- **No architecture, floor, or implementation authority was selected.** Q-86 is `status = "open"` (`agent-scaffold.plan.toml:2561`). No surface in the tree records a chosen A, B, or C or a chosen floor. The recommendation "selects nothing" is stated at `Q-86-synthesis.md:186,219`, `Q-86.md:15,37`, `agent-scaffold.plan.toml:2569,2580`. The no-decision boundary explicitly limits Q-89 to "the two low repairs plus one focused mixed-model verification" and holds production implementation blocked until the selected proof closes every applicable valid finding (`Q-86-synthesis.md:19`, `Q-86.md:43`, `agent-scaffold.plan.toml:2582`, `workflow-calibration.md:30`, `Q-89.md:38`). The proof unit remains an explicit blocker for every production implementation unit, with no automatic fallback architecture or floor.

## Counts

**Zero critical, zero high, zero medium, zero low. Zero findings.**

Both round-5 corrections are applied exactly as the durable triage specified, on every surface it named; both derive from and agree with their cited sources; no published bound, count, receipt, or authority boundary moved; the projection is current under `render --check --strict`; and the closure path retires the capped counters and routes any new valid finding back to the human. Nothing outside the two fixes and their direct residue is reported, and no earlier settled verdict is reopened.
