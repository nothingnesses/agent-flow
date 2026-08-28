# Narrowed Q-86 round 1 triage

## Scope and reproduction

I independently reviewed `main...HEAD` (`e4817a07...045c4ded`) as the narrowed, risky Q-86 decision artefact. I read `AGENTS.md`, the triager prompt, Q-86, Q-88, the narrowed synthesis, both retained proposals and prototypes, all five prior Q-86 synthesis triages, the Q-88 receipt, both round-1 reviews, the planning fold, and the generated projection. I did not edit the reviewed product, plan, metrics, prototypes, or prior findings.

I reproduced the documentary evidence with `git diff --name-only main...HEAD`, `git show d24cf02b:...Q-86-synthesis.md`, `rg`, and the supplied selectors. The Q-88 receipt is one `type:"decision"` record with the six recorded labels, recommendation, and chosen value. The narrowed synthesis contains no source-label map, while the retained proposals still use `Candidate A`/`Candidate B` and `M1`/`M2`/`M3`. The generated plan contains two non-fenced H1 headings: its title and the Q-88 sidecar title. Neither prototype contains a caveat beyond its shebang; the controller run emits zero-valued `bad_*` counters.

`nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` and `nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` passed. The latter reports 485 valid metrics records, 114 steps, 88 questions, and workflow invariants hold. I also ran the controller in C/risky-acceptance/high mode and the Q-78 replay with `PYTHONDONTWRITEBYTECODE=1`; both reproduced their published output without changing the tree.

The Q-88 decision is respected: these verdicts do not require a complete proof for all options. The valid corrections preserve its selected-option-only proof gate and improve the current decision material's provenance and prototype-status boundaries.

## Deduplication

Seven raw reports consolidate to six findings. `NR1C-1` and narrowed reviewer finding 2 are the same false no-change claim. The other five reports are distinct.

## Verdicts

### T1 — false no-change claim

- **Source IDs:** `NR1C-1`; narrowed reviewer finding 2.
- **Verdict:** valid, **low**.
- **Evidence:** `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:7` says that no `metric` or `generated plan` changes in this pass. `git diff --name-only main...HEAD -- docs/metrics/workflow.jsonl docs/plans/agent-scaffold.md` returns both paths; `bedbf095` appends the Q-88 decision record to the former, and the latter is the required rendered projection. `render --check --strict` passes, confirming that the generated-plan change is legitimate but does not make the no-change sentence true. The exact Q-88 receipt is present in `docs/metrics/workflow.jsonl`.
- **Reasoning:** This repeats the round-2 T10 boundary defect, now also concealing the append-only decision event that makes Q-88 auditable. It is low rather than medium because the receipt and generated projection are correctly present and linked from the current plan, so this wording does not alter implementation authority or the human decision.
- **Correction:** State that no workflow or production behaviour changes; that this pass appends exactly the Q-88 decision event and changes no metrics schema or behaviour; and that the generated plan changes only as the required projection of Q-86/Q-88 planning sources.

### T2 — no provenance map connects the retained proposal labels to the human-facing options

- **Source ID:** `NR1C-2`.
- **Verdict:** valid, **low**.
- **Evidence:** `rg -n 'state-machine|safety-process|Candidate [AB]|M[123]' docs/plans/workflow-calibration.explorations/Q-86-synthesis.md` produces no output. The retained state-machine proposal still labels its alternatives `Candidate A` and `Candidate B` and recommends Candidate A (`Q-86-state-machine.md:13-16`), while the safety proposal recommends `M2` (`Q-86-safety-process.md:476`) and excludes M3 (`:515`). The prior narrowed source had the map at `d24cf02b:docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:13`, but the narrowing removed it.
- **Reasoning:** The Q-88 prototype boundary rightly preserves the proposals as design inputs rather than executable eligibility evidence. It does not make their incompatible labels self-explanatory. A human following the retained material can otherwise mistake state-machine Candidate B for synthesis Option B or read its Candidate-A recommendation without knowing the synthesis's mapping. This is a documentation/provenance risk only; the narrowed synthesis still names the three choices and remains the authoritative decision artefact.
- **Correction:** Add one sentence to the narrowed synthesis mapping Option A to state-machine Candidate A and safety M1, Option B to safety M2 plus the state-machine sealed authority envelope, Option C to state-machine Candidate B, and safety M3 to excluded. Retain the existing prototype caveat so the map does not revive any proof claim.

### T3 — Q-88's sidecar creates a second document-level H1 in the generated plan

- **Source ID:** `NR1C-3`.
- **Verdict:** valid, **low**.
- **Evidence:** `docs/plans/agent-scaffold.questions/Q-88.md:1` is an H1. `question_details_section` inlines question sidecars verbatim (`src/plan/render.rs:586-602`), and the generated plan consequently has non-fenced H1 headings at `docs/plans/agent-scaffold.md:3` and `:5114`. The latter appears under `## Question Details`; Q-78 and Q-86 sidecars begin with prose rather than an H1.
- **Reasoning:** This is generated faithfully and does not affect TOML-primary parsing, but it breaks the rendered document hierarchy by placing an H1 beneath a level-two container. It is a presentation/document-structure defect only.
- **Correction:** Remove the Q-88 title line to follow the Q-78/Q-86 sidecar convention, or demote it and all descendant headings consistently. Re-render and retain the passing strict render check.

### T4 — Option C's three-reviewer minimum is not derived in the narrowed artefact

- **Source ID:** `NR1C-4`.
- **Verdict:** valid, **low**.
- **Evidence:** The narrowed synthesis states only a two-reviewer allocation at `Q-86-synthesis.md:85` and prices A and B at two reviewers per batch in the table at `:154-156`. The C risky-work and acceptance rows nevertheless state two batches and three reviewer calls (`:155-156`). Option C requires blind closure (`:135`) but never states that discovery has two reviewers and that blind closure has one. The pre-narrow synthesis had that derivation.
- **Reasoning:** The three-call number may be the intended design, but it is not reconstructible from the current decision artefact. That makes C appear to have an unexplained minimum-cost advantage in the cost comparison. This correction documents a proposed cost allocation; it does not complete the deferred selected-option proof.
- **Correction:** In Option C or the table, state that the risky and acceptance minimum is a two-reviewer discovery batch plus a one-reviewer blind-closure batch, hence two batches and three reviewer calls.

### T5 — retained prototypes lack an in-file limitation notice

- **Source ID:** `NR1C-5`.
- **Verdict:** valid, **low**.
- **Evidence:** The narrowed synthesis labels both scripts adversarial prototypes rather than proof at `Q-86-synthesis.md:41-56`, but `q86-controller-proof.py:1` and `q86-q78-scope-replay.sh:1` contain only shebangs and no `prototype`, `limitation`, or caveat text. Running the former reproduces zero-valued `bad_*` counters, and its filename contains `controller-proof`.
- **Reasoning:** The current landing documents correctly preserve the Q-88 decision, but a reader who opens or runs a retained script directly receives no local warning that its zero output is not recommendation-eligibility evidence. A short caveat reinforces the narrowed boundary without attempting the deferred proof.
- **Correction:** Add a short Python docstring and shell comment block saying that each is an adversarial prototype, its output is not a safety or recommendation-eligibility proof, and directing readers to the synthesis prototype boundary and round-5 triage. Do not rename the cited files or expand their executable scope.

### T6 — retained state-machine induction claim

- **Source ID:** narrowed reviewer finding 1.
- **Verdict:** invalid.
- **Evidence:** The reviewer correctly identifies the historical arbitrary-finite claim at `Q-86-state-machine.md:440`. However, the proposal's status boundary explicitly classifies later graph-based safety assurances as historical self-assessment rather than current assurance (`:3-5`), and the immediately preceding checker paragraph says the retained-map cap and missing products make the prototype incomplete (`:438`). The narrowed synthesis repeats the same boundary and makes the later selected-option proof the implementation blocker (`Q-86-synthesis.md:41-56,182-203`).
- **Reasoning:** The line is a retained historical claim that the current status boundary expressly withdraws as decision evidence; it does not authorize an architecture or implementation. Rephrasing it as withdrawn history would improve local readability, but the reviewer has not shown a current contradiction or missing safety gate after Q-88's explicit narrowing. Treating it as a live proof obligation now would conflict with the human decision to defer complete executable proof until an option is selected.
- **Correction:** None required for this round.

## Outcome and counts

**Outcome: `new_valid`.** Seven raw reports deduplicate to six findings: **five valid low findings** and **one invalid finding**. There are **zero critical, zero high, zero medium, and five low valid findings**. No residual risk was accepted.

## Backstop

No high- or critical-severity finding was dismissed. **No independent dismissal backstop re-check is owed.**
