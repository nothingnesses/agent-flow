# Narrowed Q-86 round 2 triage

## Scope and reproduction

I independently triaged the risky narrowed Q-86 decision artefact at `main...HEAD` (`21f33fa6...d0fa9dfb`). I read `AGENTS.md`, `.agents/prompts/triager.md`, the Q-86 and Q-88 structured records and sidecars, the narrowed synthesis, the prior narrowed triage, and both round-2 reviews. I did not edit the reviewed product, plan, metrics, or prior findings.

`nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` passed, and `nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` passed with 486 valid metrics records, 114 steps, 88 questions, and workflow invariants holding. The targeted selectors reproduced all three reported low claims: the Q-86 sidecar has C's pass-three/23-shortfall tail but only a qualitative A comparison, Option A's source allocation is absent from the narrowed decision artefact, and the rendered Q-88 block follows Q-86's `## No-decision boundary` as an unqualified `## Decision` heading.

## Deduplication and no-relitigation check

`q86-narrow-r2-reviewer-claude.md` raises three distinct findings; `q86-narrow-r2-reviewer-gpt.md` raises zero. There are three raw findings and no duplicates.

None re-raises a settled finding without new evidence. The sidecar balance is a new omission in the expanded Q-86 sidecar, while the prior synthesis and structured ask already contain both tails. The Option A allocation is distinct from round-1 T4, which adjudicated only C's previously unexplained three-call minimum; the round-1 correction made C explicit and left A as the only unallocated comparative row. The Q-88 hierarchy is the direct presentation side effect of the T3 correction made in `9071fb5d`, which removed its H1.

## Verdicts

### T1 — the Q-86 question sidecar omits A's quantified late-discovery tail

- **Source:** `docs/plans/agent-scaffold.reviews/q86-narrow-r2-reviewer-claude.md`, finding 1.
- **Verdict:** valid, **low**.
- **Evidence:** `docs/plans/agent-scaffold.questions/Q-86.md:7` says only that A preserves more bounded late discovery than C. Its C entry at `:9` states that C stops at pass three and leaves 23 later shortfalls, including further highs. The authoritative narrowed synthesis supplies A's missing symmetric figure at `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:97`: it stops at pass seven and leaves three later low shortfalls. The structured Q-86 ask also supplies both figures at `docs/plans/agent-scaffold.plan.toml:2565-2567`, projected into the queue at `docs/plans/agent-scaffold.md:179`.
- **Reasoning:** The sidecar is a human-facing Q-86 detail and presents C's quantified consequence alongside only a favorable qualitative A comparison. Its reader therefore cannot compare the two replay tails from that detail alone. This is a documentation-balance defect, not a request to treat either replay or prototype as recommendation-eligibility proof; the complete information remains in the authoritative synthesis and structured queue, so the impact is low.
- **Correction:** Add A's existing qualified replay result to `Q-86.md`: “On the descriptive Q-78 replay it stops at pass seven and leaves three later low shortfalls undiscovered.” Re-render the projection.

### T2 — Option A's acceptance allocation is not stated in the narrowed decision artefact

- **Source:** `docs/plans/agent-scaffold.reviews/q86-narrow-r2-reviewer-claude.md`, finding 2.
- **Verdict:** valid, **low**.
- **Evidence:** The shared package requires blind closure evidence for every ordinarily completing acceptance path at `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:72`. Option A states an acceptance settled-pass condition at `:79`, and the comparison table prices it as one batch and two reviewer calls at `:158`, but neither explains that allocation or how it provides the shared blind evidence. In contrast, the round-1 T4 correction makes C's two-reviewer Discovery plus one-reviewer BlindClosure allocation explicit at `:146`. The mapped Option A source specifies the missing allocation at `docs/plans/workflow-calibration.explorations/Q-86-state-machine.md:171`: its first batch uses one broad blind seat and one rubric-focused seat with no finding history.
- **Reasoning:** The two-call bound is not wrong, and the retained proposal gives it a coherent basis. But the narrowed synthesis is the current decision artefact and its cost table leaves A's cheapest acceptance row unexplainable there, particularly after C's corresponding minimum was made explicit. A reader cannot tell whether A lacks blind closure or supplies it within its single batch. This only documents a proposed allocation and preserves the Q-88 selected-option proof gate, so it is low severity.
- **Correction:** State in Option A or its cost-table row that the single settled acceptance batch has one broad blind seat and one rubric-focused or informed seat, and that its blind seat supplies the required closure evidence. Do not change the stated bound.

### T3 — the H1 repair leaves the rendered Q-88 detail block without an identity boundary

- **Source:** `docs/plans/agent-scaffold.reviews/q86-narrow-r2-reviewer-claude.md`, finding 3.
- **Verdict:** valid, **low**.
- **Evidence:** `docs/plans/agent-scaffold.questions/Q-88.md:1` now begins `## Decision`. `question_details_section` copies question sidecars verbatim without inserting a question heading or identifier at `src/plan/render.rs:586-602`. The rendered plan consequently proceeds from Q-86's `## No-decision boundary` at `docs/plans/agent-scaffold.md:5110` to Q-88's generic `## Decision` at `:5114`. `git diff 4e19c4e9..9071fb5d -- docs/plans/agent-scaffold.questions/Q-88.md` reproduces the specific round-1 T3 correction: it removed the only `Q-88` title to eliminate the invalid nested H1. The strict render check confirms faithful rendering but does not add an identity boundary.
- **Reasoning:** The prior repair correctly removed the second H1, but a generic same-level `Decision` section immediately after Q-86 reads as more Q-86 detail, especially because Q-86 remains open. The Q-88 identity is therefore not locally self-contained in the rendered detail block. The structured queue and receipt remain unambiguous, so this is a low presentation defect only.
- **Correction:** Add a Q-88-identifying introductory sentence before `## Decision`, for example “Q-88 records how the human closed the capped Q-86 proof-before-choice artefact.” Keep the H1 removed and re-render.

## Outcome and counts

**Outcome: `new_valid`.** Three raw findings deduplicate to **three valid low findings**. Counts: critical 0, high 0, medium 0, low 3, invalid 0. No residual risk was accepted.

## Backstop

No high- or critical-severity finding was dismissed. The zero-findings second review is not a dismissal. **No independent dismissal backstop re-check is owed.**
