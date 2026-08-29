# Q-86 decision-fold plan review, round 5 (reviewer: claude-opus-5, lens: proof-plan executability and adoption)

Target: `main...e1d8a767` (11 commits, 19 files). Read independently: `AGENTS.md`, `.agents/prompts/reviewer.md` (byte-identical to `pack/prompts/reviewer.md`), the proof step `docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md`, the Q-86/Q-91 decision sources (`agent-scaffold.questions/Q-86.md`, `Q-91.md`, plan TOML asks, both JSONL receipts), the retained synthesis and safety proposal (`Q-86-synthesis.md`, `Q-86-safety-process.md`, `Q-86-state-machine.md`, `Q-86-convergence-mechanism-brief.md`), the four prior decision-fold triages (r1 through r4), the five retained Q-86 synthesis triages, the scheduler sidecar `workflow-ready-frontier-scheduler.md`, `workflow-calibration.md`, the Success Criteria, the ledger retention record, and the generated projection. I did not read any other round-5 reviewer's output.

## Reproduction, and what holds

Every mechanical gate reproduces green on this worktree:

```text
nix develop --command cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
# docs/metrics/workflow.jsonl: 500 records, valid
# docs/plans/agent-scaffold.plan.toml: 115 steps, 91 questions, valid
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
# docs/plans/agent-scaffold.plan.toml vs docs/metrics/workflow.jsonl: workflow invariants hold
git diff --check main...HEAD
# exit 0
```

All four round-4 corrections verify:

- **T1 (blind-closure scope product).** The scope table, owner table, and dismissal axis at `bounded-convergence-option-b-proof.md:86-110` now compose `OwnerRoute x ScopeDisposition x TriageDisposition` per stable id, with fixtures (`:118-128`), acceptance criterion 4 (`:215`), and killing mutation classes (`:188`). The retained synthesis (`Q-86-synthesis.md:125-127`) and safety proposal (`Q-86-safety-process.md:332-349,441-444`) carry the same product.
- **T2 (skipped proof bypass).** The typed `[[step.blocker]] policy = "complete-only"` contract is stated in the proof step (`:21-29`), owned by the scheduler (`workflow-ready-frontier-scheduler.md:9-19`, acceptance 3 at `:35`), and propagated to Q-86 (`questions/Q-86.md:47`), the synthesis (`Q-86-synthesis.md:190`) and the Success Criteria. No `[[step.blocker]]` is declared in the live plan, so the not-yet-implemented schema cannot break the parser. See Finding 1 for the residue.
- **T3 (lock-bound Python).** The five commands at `:197-201` now use `nix shell --inputs-from . nixpkgs#python3 -c python3 ...`. I ran the form and it resolves through the repository lock: `PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 <script>` printed `3.13.13` from `/nix/store/l9k0anq0z7zz81zcwy035jfwap9ga6rl-python3-3.13.13`. `flake.nix` declares the `nixpkgs` input that `--inputs-from .` binds.
- **T4 (owning sidecar minima).** `workflow-calibration.md:26` now qualifies both minima as clean, ordinarily delivering `Complete`-domain minima and admits shorter legal early-terminal paths.

Also verified by reproduction rather than assumed:

- The traceability gate's `valid_findings=51` (`:204`) is the true source-derived count: r1 13 valid of 17, r2 12 of 13, r3 9 of 9, r4 8 of 10, r5 9 of 9.
- The algebra is internally derivable, not just asserted: `L_B = r_plan + sum_{m+1}(n_q + 1) = r_plan + |O| + m + 1`; `R_B = 7 + sum_{m+1}(4n_q + 1) = 4|O| + m + 8`; and `I_B = 34 + sum_{m+1}(4(4n_q + 1)) + 2|O| = 18|O| + 4m + 38` (four agent calls per batch plus one initial and one reopen repair per obligation).
- The `L_q` domain repair is sound. The domain conditions at `:160` are observable from the final state, and the two-owner cross-credit mutant at `:176` genuinely lands in-domain at two batches against an unmutated minimum of three.
- The Q-78 selector in `Q-86-synthesis.md:24` still returns ten passes and `[7,10,5,6,5,5,4,2,1,0]`; the nineteen clean-with-findings records and the six surviving Q-78 triage files both reproduce.
- No production authority is taken. The diff touches no `src/`, `pack/`, `.agents/`, `README.md` or `CHANGELOG.md`; the only metrics change is the two append-only `type:"decision"` receipts, whose options, recommendation and chosen values match Q-86 and Q-91 exactly.
- Roadmap order 117 is unique and maximal, the TOML block is declared last, and no older Roadmap row moved (`agent-scaffold.md:304` is the final table row). The new sidecar's opening line carries no Roadmap status token, so it does not move the Q-87 selector snapshot of 17.

## Finding 1 - A self-declared `review-skipped` waiver makes the proof `complete` with zero review rounds, satisfying the very gate the round-4 high finding created

**Severity: high.**

The fold's central safety mechanism is that a bounded-convergence production unit is unblocked only by proof status `complete`. `bounded-convergence-option-b-proof.md:21` says "this proof authorises production only in status `complete`"; `questions/Q-86.md:47` says "`skipped` and every other non-`complete` proof state remain blocking"; `workflow-ready-frontier-scheduler.md:17` says "The scheduler satisfies `complete-only` only when the target is exactly `complete`", enumerates all seven statuses, and adds a validation rule "closing a manual status-advance bypass" on the *dependent*.

Nothing anywhere in the fold constrains how the *target* reaches `complete`. `AGENTS.md:147` defines W3 as convergence-OR-waiver: "a `complete` step with no round records is exempt when a `step`-unit waiver covers it", and `reason = "review-skipped"` is `evidence_tier = "self-declared"`, requiring no backing record. Grepping the whole fold for waivers returns nothing: `bounded-convergence-option-b-proof.md`, `workflow-ready-frontier-scheduler.md`, `questions/Q-86.md`, `questions/Q-91.md`, `Q-86-synthesis.md` and `workflow-calibration.md` never mention the waiver mechanism.

**Reproducible demonstration** (run in a scratch copy outside the repository, per the validate-in-scratch rule; the live tree was untouched, `git status --porcelain=v1` empty before and after):

```sh
SCRATCH=$(mktemp -d) && mkdir -p "$SCRATCH/docs/plans" "$SCRATCH/docs/metrics"
cp docs/plans/agent-scaffold.plan.toml "$SCRATCH/docs/plans/"
cp docs/metrics/workflow.jsonl "$SCRATCH/docs/metrics/"
# In the copy, set `bounded-convergence-option-b-proof` (plan.toml:1791) to
# status = "complete" and leave waiver = [].
agent-flow validate --source "$SCRATCH/docs/plans/agent-scaffold.plan.toml" --workflow
# exit 1
# ... Roadmap step `bounded-convergence-option-b-proof` is `complete` but has no
# round records and no covering waiver; log its review rounds, or record a
# `type:"waiver"` for it if it predates logging or its review was skipped

# Now replace `waiver = []` (plan.toml:1795) with the self-declared waiver:
#   [[step.waiver]]
#   id = "bounded-convergence-option-b-proof-w1"
#   unit = "step"
#   reason = "review-skipped"
#   evidence_tier = "self-declared"
agent-flow validate --source "$SCRATCH/docs/plans/agent-scaffold.plan.toml" --workflow
# exit 0
# ... 115 steps, 91 questions, valid
# ... workflow invariants hold
```

The control (exit 1) proves the waiver is exactly what flips the result. The proof step is then `complete` and workflow-valid having never been reviewed or performed, so the typed `complete-only` blocker resolves ready and the planned workflow validation rejects nothing. The same route exists at increment granularity: `AGENTS.md:147` exempts an increment whose peak `consecutive_clean` falls short of its risk class when an `increment`-unit waiver names it, which reaches `bounded-convergence-option-b-proof-inc1` and its declared two-clean-round bar.

**Reasoning.** The round-4 triage (`q86-decision-r4-triage.md:31-37`) upheld at high that "a later production step with the only required proof dependency can become scheduler-ready after the proof is skipped", because a skipped proof "violates the selected decision's explicit 'completed proof' boundary". The repair closed every non-`complete` status but left the strictly more permissive route: a status that positively asserts doneness, reached by a self-declaration that needs no evidence. A gate whose sole predicate is `status == complete` inherits every path to `complete`, and acceptance criterion 14 ("The proof step converges as `risky` work with two consecutive clean review rounds") is prose that no check enforces once a waiver is present. This is not a general complaint about waivers: the whole point of this fold, post-r4, was that the generic dependency mechanism is too weak for this one safety contract, and the same argument applies unchanged to the generic exemption mechanism. It is mitigated only by a `[[step.waiver]]` being reviewed plan content rather than an orchestrator direct-on-main edit (unlike a status flip, which `AGENTS.md:91` does place in the orchestrator's direct set); high remains proportionate because the outcome is production authority for a widely used stopping and delivery mechanism whose blocking proof was never reviewed.

**Suggested correction.** State in the proof step, Q-86's authority boundary, and the scheduler's complete-only contract that this step's completion admits no convergence waiver, and give the scheduler a red control: a `complete` proof target covered by a `step`- or `increment`-unit waiver must leave a complete-only dependent blocked and must fail workflow validation. Alternatively, make the complete-only policy's satisfaction predicate "target is `complete` AND its convergence is round-backed, not waived", which is the property the decision actually intends.

## Finding 2 - The traceability checker never resolves a matrix row's named killing mutation, so per-row mutation coverage can be fabricated

**Severity: low.**

`bounded-convergence-option-b-proof.md:180` makes two named artefacts mandatory on every applicable row: "A row marked executable must name a property and at least one mutation that kills it. A row marked durable-text must cite the corrected planning source."

The checker's contract enumerates what it rejects, and the mutation is missing from both statements of that list. `:39`: "It rejects a missing, duplicate, malformed, or unparsed triage; any difference between the derived source set and the matrix rows; any duplicate row or count mismatch; any overlap, omission, or disagreement in the matrix's applicable and Option-B-inapplicable disposition sets; **an unresolved named assertion or durable-text pointer**; and any applicable verdict left open." Acceptance criterion 11 (`:222`) repeats the same list and again names only row-set, row-count, disposition-set and summary mismatches plus "resolves every applicable row".

The other oracle does not cover it either. `q86-option-b-mutations.py` (`:37`) "fails if a load-bearing transition or predicate has no mutation, if a mutation is not exercised, or if any mutation survives" - it checks the manifest against the model, never the matrix against the manifest.

**Failure scenario.** An executable row closing, say, `q86-synthesis-r5-triage.md` T4 (scope/dismissal products escaping `SeriousBlocked`) names assertion `prop_critical_scope_blocked` and mutation `M-critical-scope-escape`. The assertion resolves; the mutation identifier does not exist in the manifest, or exists under a different tag that kills a different property. `q86-option-b-traceability.py` reports `unresolved=0` because it only resolved the assertion, and `q86-option-b-mutations.py` reports `survived=0` because every manifest entry it does know about was exercised and killed. Both commands pass with the matrix claiming mutation coverage that was never bound to anything.

Low rather than medium because the manifest rule at `:188` ("A load-bearing tag without a mutation fails") still forces a killing mutation for every load-bearing predicate independently, so what is unenforced is the per-row attribution rather than the underlying mutation adequacy, and criterion 14 requires reviewers to inspect mutation adequacy rather than trust green output.

**Suggested correction.** Add the named mutation to both rejection lists: the traceability checker must resolve each executable row's named mutation against the mutation manifest and fail on an unknown, unexercised, or surviving mutation, the same way it already resolves the named assertion.

## Finding 3 - The updated architecture summary still states the superseded universal blocker rule two lines above its own correction

**Severity: low.**

`workflow-ready-frontier-scheduler.md:48` names `docs/plans/mealy-workflow-driver.explorations/r2-architecture-build-path.md` as one of the two "aligned scheduler summaries" that must be kept current, and this fold did edit that file's section 3.4. The prose at `r2-architecture-build-path.md:191` was corrected to "whose ordinary `blocked_by` targets are all `Complete` or `Skipped` and whose typed complete-only targets are all `Complete` ... and `Skipped` remains unsatisfied for complete-only."

The signature comment three lines above it was not:

```text
$ sed -n '184,191p' docs/plans/mealy-workflow-driver.explorations/r2-architecture-build-path.md
```

`:188` still reads `// a blocker is satisfied exactly when its status is Complete or Skipped.` That is now false for a `complete-only` edge and is directly contradicted by `:191`. A reader of the code block alone, which is the part an implementer copies into `src/driver/schedule.rs`, gets the pre-fold rule.

Low: it is a retained design record with an authoritative sidecar that controls (`workflow-ready-frontier-scheduler.md:3`), and the correct rule sits three lines below. It is still a stale line inside the exact passage this change rewrote, in a file the fold's own documentation-impact list names.

**Suggested correction.** Update `:188` to state the two policies, or delete the comment now that `:191` carries the rule.

## Finding 4 - The proof step's provenance pointers to the five retained triages are not repository-root paths, unlike the same fold's other provenance entry and the step's own text

**Severity: low.**

The same commit series wrote both forms. For `workflow-ready-frontier-scheduler` it appended a repository-root path (`docs/plans/agent-scaffold.plan.toml:1781`: `"docs/plans/agent-scaffold.reviews/q86-decision-r4-triage.md"`). For the new step it wrote bare `docs/plans/`-relative paths (`docs/plans/agent-scaffold.plan.toml:1799-1805`):

```toml
findings = [
  "agent-scaffold.reviews/q86-synthesis-r1-triage.md",
  ...
]
```

The step's own sidecar lists the identical five files with the prefix at `bounded-convergence-option-b-proof.md:13-17` and again in the traceability command at `:200` (`docs/plans/agent-scaffold.reviews/q86-synthesis-r1-triage.md ...`), so one fold now carries two path conventions for one file set. `src/plan/source.rs:643-649` only requires a task-relative path with no `..`, so both validate and neither is flagged.

The consequence is in the projection. `docs/plans/agent-scaffold.md:304` renders the new row as `why: ... findings agent-scaffold.reviews/q86-synthesis-r1-triage.md, ...` while all four neighbouring rows render `docs/plans/`-prefixed paths. `AGENTS.md:106` requires task-entry re-grounding to cite "a finding by path"; the path this step's structured provenance offers does not resolve from the repository root, and copying it from the rendered Roadmap fails.

**Suggested correction.** Use `docs/plans/agent-scaffold.reviews/q86-synthesis-r<n>-triage.md` for the five entries, matching the scheduler entry the same fold wrote and the step body's own citations, and re-render.

## Finding 5 - Resume and replay reconstruction has no acceptance criterion, though it is a named shared-safety-package property

**Severity: low.**

The proof body states the property twice as a requirement of the selected model. `bounded-convergence-option-b-proof.md:46`: "Reconstruction of the same ordered events yields the same selected architecture, floor, family, authority, findings, and terminal state." `:78`: "Resume reconstructs the same route from immutable phase identities and cannot reclassify, drop, transfer, or replenish it." `:154`: "Replan, rebuild, rename, narrowing, or human resume cannot replenish authority." It is one of the eight shared safety-package requirements (`Q-86-synthesis.md:66`: "Resume, rename, rebuild, and unchanged replan reconstruct the same authority") and is the Idempotent row on which Option B was judged (`Q-86-synthesis.md:174`).

The acceptance list does not carry it. Reading all fifteen criteria at `:212-226`, the only occurrence of reconstruction is criterion 2 (`:213`), scoped to the sealed plan review: "reconstruction without replenishment". Criterion 4 covers the post-freeze model, routes, closure and completion but says nothing about replay; criterion 13's "identical semantic summaries" is run-to-run determinism of the command suite, not event-replay reconstruction of model state. The mandatory mutation classes at `:188` likewise name "completed-prior-owner transfer, replenishment or delivery" but no resume or reconstruction class.

**Failure scenario.** A proof implementer satisfies all fifteen criteria and every mandatory mutation class without ever exercising a resume that replays the same ordered events, or a rename/rebuild/replan that must not replenish spend. The proof reaches `complete` and unblocks production authorisation for an architecture whose idempotent reconstruction, which is precisely the property that stops a resumed loop from buying fresh authority, was never demonstrated.

Low rather than medium: the body does state the requirement, and the blanket manifest rule at `:188` ("Every load-bearing transition and predicate is tagged in the reference model and appears in a manifest ... A load-bearing tag without a mutation fails") plus criterion 12 will catch it if the implementer treats reconstruction as load-bearing. The gap is that the acceptance gate does not force that judgement, in a plan that otherwise mirrors nearly every body requirement into a criterion.

**Suggested correction.** Extend criterion 4 (or add a criterion) to require that replaying the same ordered events reconstructs the identical architecture, floor, family, authority, finding map, owner routes and terminal state, and that resume, rename, rebuild and unchanged replan replenish no authority; add the matching mandatory mutation class.

## Severity summary

- **critical: 0.** I found nothing at critical severity. No path in this fold changes production behaviour, and the proof unit still fails closed before any implementation authority.
- **high: 1.** Finding 1.
- **medium: 0.** I found nothing at medium severity.
- **low: 4.** Findings 2, 3, 4, 5.

No finding re-raises a settled verdict. Finding 1 is a different mechanism from r4-T2 (a self-declared convergence waiver on the target, not a `skipped` status on it) and is demonstrated rather than argued. Finding 2 is distinct from r1-T3 (which was about deriving the 51-verdict source set, now fixed) and from r1-T4 (dismissed, and about tag-versus-mutation counts, not about the matrix resolving a named mutation). Findings 3, 4 and 5 concern text and criteria introduced or edited by this round's repairs.

Per `AGENTS.md:108` and the reviewer prompt, I raise no line-length or prose-wrapping finding. All changed files are ASCII-clean; I verified this with a byte-class grep over every file in `git diff --name-only main...HEAD`.
