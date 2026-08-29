# Q-86 decision-fold plan review, round 3 triage

## Scope, reproduction, and deduplication

I independently read `AGENTS.md`, `.agents/prompts/triager.md`, the Q-86 proof-step sidecar, Q-86 question and synthesis, the five retained synthesis triages, both earlier decision-fold triages, the findings-file retention policy, both round-3 reviews, the plan source, and the ledger's retained-Q-78 precedent. The reviewed artifact is `main...5845ece6`; it is a risky planning artifact. I did not edit the reviewed product, ledger, or metrics log.

The mechanical gates reproduce:

```text
nix develop --command cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
# docs/metrics/workflow.jsonl: 498 records, valid
# docs/plans/agent-scaffold.plan.toml: 115 steps, 91 questions, valid
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
# docs/plans/agent-scaffold.plan.toml vs docs/metrics/workflow.jsonl: workflow invariants hold
git diff --check main...HEAD
# exit 0
```

The five traceability inputs are presently parseable and derive `13 + 12 + 9 + 8 + 9 = 51` valid round-qualified identities. That present-tense availability is not a retention guarantee: the cleanup rule deletes resolved findings after committing them (`AGENTS.md:67`; `docs/plans/agent-scaffold.steps/findings-files.md:9`), while the proof command reads live paths (`bounded-convergence-option-b-proof.md:146`). The plan's provenance entries name the same five paths (`agent-scaffold.plan.toml:1793-1801`), but provenance findings are deliberately not existence-checked because historical findings may have been deleted (`src/plan/source.rs:245-249`).

There are four raw findings and no duplicates. Claude F1 is a new mutation-domain defect, not a re-raise of round 2's terminal-path domain finding. Claude F3 is the distinct failure to propagate that round-2 repair into retained decision sources. GPT F1 is a separate blind-closure transition ambiguity.

## Verdicts

### T1 — Scheduled-owner credit is embedded in the `L_q` domain rather than proved by it

- **Sources:** Claude F1.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** `bounded-convergence-option-b-proof.md:108` limits the `L_q` domain to paths where every member of `O_q` receives its scheduled initial-attempt batch, while `:122` requires the mutation that grants a non-scheduled owner initial credit to falsify scoped `L_q`. For `O_q = {A, B}`, the ordinary witness is `A initial`, `B initial`, `blind closure` (three batches). A mutation that credits B during A's scheduled batch admits the delivering two-batch witness `A initial also credits B`, `blind closure`; B never receives its own scheduled batch. The domain clause excludes that witness, so the lower-bound oracle can still hold over the filtered ordinary path instead of killing the mutation.
- **Reasoning:** Scheduled-owner-only credit is the premise that supports `L_q = n_q + 1`; it cannot also be a membership condition that removes violations from the very lower-bound test assigned to detect them. The result is a proof specification that either has a vacuous mutation or leaves the mutation to an unstated different oracle. This fails closed before production authority, so medium is proportionate.
- **Required correction:** Define the `L_q` domain solely by independently observable delivery conditions: converged sealed review, valid freeze and exact ownership, scheduled phase, its own obligations and blind closure settled, no terminal or non-delivery transition before phase closure, and eventual family `Complete`. Remove the per-owner scheduled-batch condition from the domain. Derive that condition from the transition relation as the lower-bound proof's conclusion, retain the two-owner cross-credit witness inside the domain, and require its mutation to make `L_q < n_q + 1`. Align the algebra acceptance criterion and mutation description with that oracle; the already narrower safety-process domain at `Q-86-safety-process.md:344` is the appropriate model.

### T2 — The five live triage files required by the traceability gate have no recorded retention contract

- **Sources:** Claude F2.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** The proof requires parsing five live files at `bounded-convergence-option-b-proof.md:20-21,126,146,168`; all five exist now and derive 51 valid identities. But ordinary findings cleanup commits then deletes resolved files (`AGENTS.md:67`; `findings-files.md:9`). No Q-86-specific retention/exemption statement is present in the proof step, plan provenance, or ledger. The plan's existing path entries cannot prevent deletion because they are shape-checked but intentionally not existence-checked (`src/plan/source.rs:245-249`). In contrast, the ledger explicitly records the Q-78 exception as a “fixed local evidence sample” (`agent-scaffold.ledger.md:551`).
- **Reasoning:** The traceability command is a mandatory blocking gate, yet normal, authorised cleanup can make it fail before the proof increment begins. Git history preserves recoverability but does not make a command reading working-tree paths reproducible. The failure is loud and recoverable, not an unsafe production pass, which makes this medium.
- **Required correction:** Before the proof increment can start, record these exact five Q-86 synthesis triages as a fixed retained evidence sample, exempt from routine cleanup until `bounded-convergence-option-b-proof` completes; put the proof-side requirement in the step and the concrete retention action in the orchestrator-owned ledger/integration record. The provenance list may remain a historical pointer but must not be treated as the retention mechanism. Alternatively, revise the traceability contract to read five immutable `<commit>:<path>` inputs via Git and pin those identities in the step; it must then reject an unavailable object or mismatched source. Either route must make the `blocked_by = []` durability claim true.

### T3 — The retained M2 blind-closure rule and the proof transition contract leave closure findings without one coherent disposition

- **Sources:** GPT F1.
- **Verdict:** valid, **medium**.
- **Reproduced evidence:** Retained M2 calls a blind-closure finding terminal (`Q-86-safety-process.md:420`). The proof sidecar gives general current-, prior-, future-, and unowned-owner routing (`bounded-convergence-option-b-proof.md:51-60`) and requires exactly one blind-closure batch (`:35,161`), but supplies no route table or fixture for a valid or seriously dismissed finding discovered in that batch. Its general current-owner rule can imply a deferred reopen; its future-owner rule permits continuation into a later campaign. Those outcomes conflict with M2's unqualified terminal sentence and have different implications for whether the one required blind closure remains valid evidence after a repair.
- **Reasoning:** This is a real missing selected-option transition, not merely a stale word: the model cannot simultaneously treat blind-closure discovery as terminal, allow a current-owner repair after the only closure batch, and preserve the repaired future-owner route. The proof remains blocking and its intended fixtures would reveal the ambiguity, so medium is proportionate.
- **Required correction:** Define blind closure as an explicit discovery stage with a route table for current, completed-prior, future, and unowned owners, plus upheld and overturned serious-dismissal outcomes. Reconcile M2's blanket terminal wording with the selected future-owner continuation: at minimum, prohibit a current-owner repair from delivering on stale closure evidence (terminalise it or require a newly specified closure cycle), retain `FutureOwnerPending` only where its canonical later campaign supplies its own closure, and keep prior/unowned routes non-delivering. Add current-owner and future-owner blind-closure fixtures and killing mutations for post-closure repair/delivery, accidental terminalisation or loss of a future-owner component, and completion without valid closure evidence.

### T4 — The minimum-domain qualification did not reach the retained synthesis or structured Q-86 decision material

- **Sources:** Claude F3.
- **Verdict:** valid, **low**.
- **Reproduced evidence:** The corrected authoritative step scopes both minima to ordinarily delivering `Complete` paths (`bounded-convergence-option-b-proof.md:108-122`). In contrast, the retained synthesis calls `L_B = r_plan + |O| + m + 1` the proposed whole-family minimum without a delivery-domain qualifier (`Q-86-synthesis.md:101-123`), and the same unqualified statement remains in the Q-86 sidecar (`questions/Q-86.md:21`) and structured ask (`agent-scaffold.plan.toml:2591`). Legal early terminal and non-delivery paths can complete below this number.
- **Reasoning:** The proof step is correct and blocks implementation, so this cannot make a conforming proof unsound. But the selected decision provenance and human-facing ask contradict the repaired specification on a formula the proof is explicitly required to establish. This is a documentation-currency defect, hence low.
- **Required correction:** In the synthesis, Q-86 sidecar, and Q-86 TOML ask, label `L_q` and `L_B` as clean/ordinarily-delivering `Complete` minima, and state that legal early-terminal and non-delivery paths are outside those domains and may be shorter. Re-render the generated plan; do not hand-edit the projection.

## Outcome, counts, and backstop

**Outcome: `new_valid`.** Valid findings: **4** — **0 critical, 0 high, 3 medium, 1 low**. Invalid findings: **0**. Accepted residual risks: **0**.

No high- or critical-severity finding was dismissed. **No independent dismissal backstop re-check is owed.** This risky plan-review round is not clean; the consecutive-clean streak remains zero and the valid corrections return to the planner.
