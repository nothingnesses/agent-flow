# Q-86 decision-fold plan review, round 3 — reviewer (Claude)

## Scope and method

Independent review of the Q-86/Q-91 decision fold and the new `bounded-convergence-option-b-proof` Roadmap unit at branch tip `5845ece6` against `main` (`e62197b3`). I read `AGENTS.md`, `.agents/prompts/reviewer.md`, the proof step sidecar, `docs/plans/agent-scaffold.plan.toml`, the rendered projection, the Q-86/Q-88/Q-89/Q-90/Q-91 question sidecars, the JSONL receipts, the retained synthesis, safety-process, state-machine and brief explorations, the five retained Q-86 synthesis triages, and the round-1 and round-2 decision-fold triages. I did not read the other round-3 reviewer's output.

I reviewed the current sources on their own terms and simulated an implementer building the specified proof artefacts; the proof files themselves do not exist yet, so behavioural claims below are about the specification, evidenced by exact citation, command output, or a derivation an implementer must follow.

## Mechanical reproduction

```text
nix develop --command cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
# docs/plans/agent-scaffold.plan.toml: up to date            (exit 0)
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl
# docs/metrics/workflow.jsonl: 498 records, valid
# docs/plans/agent-scaffold.plan.toml: 115 steps, 91 questions, valid   (exit 0)
nix develop --command cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
# docs/plans/agent-scaffold.plan.toml vs docs/metrics/workflow.jsonl: workflow invariants hold   (exit 0)
git diff --check main...HEAD
# exit 0
```

ASCII check over all fifteen changed files: `LC_ALL=C grep -cP '[^\t\x20-\x7e]' <file>` prints `0` for every one.

## Round-2 fix verification

All four round-2 upheld findings are repaired.

- **T1 (declaration position vs unique `order = 117`) — fixed.** The `[[step]]` block moved from declaration position 36 to 115, the last of 115 (`docs/plans/agent-scaffold.plan.toml:1784-1806`). The migration's own prescribed detector now prints one row again:

  ```text
  awk '/^slug = /{s=$3} /^order = /{sub(/order = /,""); if ($0+0 < p) print "out of place:", ps; p=$0+0; ps=s}' docs/plans/agent-scaffold.plan.toml
  # out of place: "rename-to-agent-flow"
  ```

  `rename-to-agent-flow` is declaration 84 and renders 98, so `plan-order-array-position.md:17,87-91` ("differs at exactly one place", "stands 84th ... renders 98th") is true again. The proof step declares 115th and renders 115th. Order values are unique (`... | sort -n | uniq -d` prints nothing) and the only absent values in `1..117` are still `84` and `91`, so the `:279` position/citation partition (≤83 safe, 85–90 drift one, ≥92 drift two) holds unchanged. No new numeric position citation for the step was introduced: `grep -rnoE '\b([Oo]rder|[Ss]tep|[Pp]osition) (11[0-9])\b'` over the sidecars and front matter returns nothing.
- **T2 (`FutureOwnerPending` phase-completion deadlock) — fixed.** `Q-86-safety-process.md:330` now scopes the no-live-route condition to family delivery and permits phase completion with retained pending components; `:332` adds the fixture/mutation obligation and `:434` adds the terminal-choice row. The step agrees at `bounded-convergence-option-b-proof.md:35,57` and criterion 4 at `:161`. The old sentence "A settled complete map with no prior- or future-owner route finishes the phase or family as applicable" is gone from the file.
- **T3 (unscoped minima) — fixed in the step,** at `bounded-convergence-option-b-proof.md:108,120,122,150,167` and `Q-86-safety-process.md:344`. See F1 and F3 for two residues of this repair.
- **T4 (false ledger-currency assertion) — fixed.** `bounded-convergence-option-b-proof.md:130` now states the anchor is an orchestrator integration duty and that the planner neither asserts currency nor edits the ledger, which matches the disposition the source finding itself required (`q86-synthesis-r1-triage.md:113`).

I also independently re-derived the traceability input set rather than accepting the stated 51. Parsing `### T<n>` headings against their verdict records gives valid/invalid counts of 13/4, 12/1, 9/0, 8/2 and 9/0 for rounds 1 to 5, so 51 valid identities over 58 sections, with a 1:1 heading-to-verdict pairing in every file and no stray `### T` heading outside the verdict sections. The algebra also reproduces: `R_B = 7 + sum(4n_q + 1) = 4|O| + m + 8`, and `4(4|O| + m + 8) + 2|O| + 6 = 18|O| + 4m + 38 = I_B`.

## Findings

**No `critical` findings. No `high` findings.** Two `medium` and one `low` below.

### F1 — The scoped `L_q` domain excludes the very execution the mandatory scheduled-owner-credit mutation produces, so that mutation cannot falsify `L_q` as the step requires

- **Severity:** `medium`.
- **Evidence.** The round-2 repair defines the minimum domain at `docs/plans/agent-scaffold.steps/bounded-convergence-option-b-proof.md:108`:

  > `L_q` ranges only over phase-`q` segments of ordinarily delivering family executions that eventually construct `Complete`: the sealed plan review converged, freeze produced finite exact ownership, phase `q` is scheduled, no terminal or non-delivery transition ends the family before that phase closes, **every member of `O_q` receives its scheduled initial-attempt batch**, the phase's own obligations settle, and its blind closure settles.

  The same section then requires, at `:122`:

  > A mutation that grants initial credit to a non-scheduled owner must falsify the scoped `L_q`

  and `:134` makes `scheduled-owner-only initial credit` a mandatory mutation class, while criterion 10 at `:167` restates the pairing ("only the scheduled owner receives initial-attempt credit, preserving scoped `L_q = n_q + 1`").

  Take the mutation the step names and the model it specifies (`:47`, `:49`, `:55`: each initial-review batch names exactly one `ScheduledOwner`; every other untested owner "remains `Untested` until its own scheduled batch"). Let `O_q = {A, B}`, so `L_q = 3`. Under the mutation, batch 1 is scheduled for `A` and also advances `B`'s initial attempt; `B` is then no longer `Untested`, so the scheduler never names a batch for `B`; blind closure is batch 2. The phase closes in 2 batches on a path that still constructs family `Complete`.

  That witness is the intended killer, but it does not satisfy the domain clause quoted above: `B` received initial credit and never received *its scheduled initial-attempt batch*. Read as the definition it is written as (the colon at `:108` introduces the clauses that define the domain), the oracle filters the witness out. Under the mutated model the domain still contains the ordinary path in which no cross-owner observation occurs and each owner is scheduled in turn, and that path still costs `n_q + 1`, so the scoped `L_q` remains satisfied and the mutation survives. `:136` says "Any surviving mutation fails", so the specification as written cannot be discharged.

  The paragraph is also internally ambiguous, which is the sharper half of the defect: its headline condition ("ordinarily delivering family executions that eventually construct `Complete`") *includes* the witness, while its enumerated clause *excludes* it. Two implementers reading `:108` will build oracles that disagree on whether a mandatory mutation is killed, and nothing in `:122`, `:134` or `:167` resolves which reading governs. The retained source proposal does not have this problem: `Q-86-safety-process.md:344` states the same domain as "a valid freeze and exact ownership, a scheduled phase whose own obligations and blind closure settle, and no terminal or non-delivery transition before that closure" and does *not* assume the per-owner scheduled batch.
- **Reasoning.** This is not a wording nit: the scheduled-owner-only credit rule is the sole premise that keeps `L_q = n_q + 1` true after round 1's T6, and `L_q` is the named oracle that is supposed to police it. Folding that premise into the domain of its own oracle makes the check partly vacuous and puts a mandatory mutation class in a state where it either survives (step fails) or is silently redirected to another oracle in violation of `:122`. It is `medium` rather than `high` because the failure is loud and fail-closed — a surviving mutation blocks the proof rather than passing an unsound one — and because no production behaviour depends on it yet.
- **Exact correction.** Define the minimum domain by properties that do not presuppose the transition rule under test: an execution that constructs family `Complete` by ordinary delivery, from a converged sealed review and a valid freeze, with phase `q` scheduled and its own obligations plus blind closure settled, and no terminal or non-delivery transition before that closure. Drop "every member of `O_q` receives its scheduled initial-attempt batch" from the domain and make it the *conclusion* the scoped `L_q` derives, so the mutated short path stays inside the domain and falsifies the bound. Keep the separate `untested-obligation completion` mutation as it is, and state which oracle owns which kill.

### F2 — The mandatory traceability gate reads five transient findings files that this project's own cleanup rule deletes, and the step records no retention obligation

- **Severity:** `medium`.
- **Evidence.** The proof's traceability command hard-codes five working-tree paths under `docs/plans/agent-scaffold.reviews/` (`bounded-convergence-option-b-proof.md:146`), `:21` requires the checker to reject "a missing, duplicate, malformed, or unparsed triage", and criterion 11 at `:168` makes parsing all five a pass condition. `:9` justifies `blocked_by = []` on the premise that "every input needed for the proof is already durable in ... the five retained synthesis triages; there is no unfulfilled proof dependency to add."

  That premise is not backed. The standing rule for exactly these files is the opposite:

  - `AGENTS.md:67`: "The orchestrator owns cleanup: when a round is fully resolved, or at task close, it commits the findings files at least once and then deletes them as a committed deletion (the commit-before-delete rule), so the review record survives in git history."
  - `docs/plans/agent-scaffold.steps/findings-files.md:9` ships the same rule as implemented behaviour.
  - The plan schema documents the consequence and declines to guard it — `src/plan/source.rs:245-248`: "The findings artifacts (task-relative paths) that justify this step. Shape-checked via `is_safe_sidecar_ref`, **NOT existence-checked** (a findings file is committed then deleted at task close, so a valid historical pointer may name an absent path)." So the `[step.provenance] findings` entries at `docs/plans/agent-scaffold.plan.toml:1795-1801` cannot detect the deletion, and `validate` stays green after it.

  The five Q-86 synthesis rounds are already "fully resolved" — Q-90 closed the narrowed artefact — so they are already eligible for deletion under that rule, and nothing in this fold exempts them. Contrast the one comparable case the project *did* record: the ledger at `docs/plans/agent-scaffold.ledger.md:551` states "Commit-before-delete cleanup removed the transient Q-78 review artefacts except the six acceptance triages that Q-86 names as its fixed local evidence sample." No equivalent sentence exists for `q86-synthesis-r1..r5-triage.md`. The project also has a worked mitigation for precisely this hazard when durable text must depend on a findings file — `checks-runner-worktree-name-collision.md:32` quotes the evidence verbatim into the sidecar "because its findings file is transient and will be removed under the commit-before-delete rule".

  Failure mode: the orchestrator applies ordinary cleanup to `workflow-calibration`'s review artefacts before `bounded-convergence-option-b-proof` runs (nothing orders the two — `blocked_by = []`, and the step's own sequencing rule at `:9` only forbids production units from preceding it). The traceability command then exits non-zero on a missing input, criterion 11 cannot be met, and by `:176` the proof fails and every production implementation stays blocked — on a housekeeping action the workflow explicitly authorises and the validator is documented not to catch.
- **Reasoning.** The traceability gate is the sole mechanical closure for the 51 adversarial verdicts, and this step is the blocker for all bounded-convergence production work. A gate whose inputs the workflow is free to delete, with an unguarded pointer and an asserted-but-unrecorded "durable" premise, is a real specification defect rather than a hypothetical. It is `medium`, not `high`: the failure is loud, the files are recoverable from git history, and no unsound proof can pass because of it.
- **Exact correction.** Record the retention explicitly and durably, in the same shape the Q-78 acceptance sample already uses: state in the step (and in the orchestrator-owned ledger note when this fold integrates) that `docs/plans/agent-scaffold.reviews/q86-synthesis-r1-triage.md` through `-r5-triage.md` are a fixed retained evidence sample exempt from commit-before-delete until `bounded-convergence-option-b-proof` completes. Either that, or make the proof independent of the live tree — pin the five inputs by `<commit>:<path>` and have the checker read them from git — and correct the `:9` claim so the durability premise names the mechanism that makes it true.

### F3 — The round-2 minimum-domain repair was not carried into the retained synthesis or the structured Q-86 ask, which still publish `L_B` as an unqualified whole-family minimum

- **Severity:** `low`.
- **Evidence.** Round 2's T3 established that `L_q` and `L_B` are false as unqualified lower bounds because the same transition model admits legal early terminal paths that finish below them. The repair reached the step (`bounded-convergence-option-b-proof.md:108,120,122,167`), the Success Criteria (`docs/plans/agent-scaffold.success-criteria.md:41`) and the source proposal (`Q-86-safety-process.md:344`), but not the two artefacts the human-facing decision material actually publishes:

  - `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:108-115` introduces the block as "the proposed whole-family bounds" and prints `L_B = r_plan + |O| + m + 1` with no domain qualifier. The same document qualifies Option A's counterpart at `:89` — "The clean whole-family minimum is `r_plan + sum(r_work_q) + 1`" — and qualifies B's per-phase figure at `:101` as a "clean minimum", so the selected option's whole-family minimum is the one unqualified minimum left in the file.
  - `docs/plans/agent-scaffold.questions/Q-86.md:21`: "Its proposed whole-family minimum is `r_plan + |O| + m + 1`", which the renderer projects verbatim into `docs/plans/agent-scaffold.md:179`.

  This matters beyond currency because the same synthesis, at its item 9, requires the proof to "Prove every selected-option transition and algebraic bound"; an implementer taking `L_B` from `:114` as stated would be asked to prove a statement the authoritative step (`:108`) says is only true on a restricted domain.
- **Reasoning.** The step sidecar is authoritative and is correct, so no proof built to the step's own criteria can be unsound because of this; the impact is that the retained decision provenance and the structured ask contradict the corrected specification on the exact point round 2 upheld. That is documentation currency inside the decision material, hence `low`.
- **Exact correction.** Qualify `L_B` in `Q-86-synthesis.md:108` the way A's and B's other minima already are (a clean minimum over ordinarily delivering `Complete` paths, with legal early terminal paths outside it), and add the same one-clause qualifier to the whole-family minimum sentence in `Q-86.md:21`, then re-render.

## Areas checked with no finding

- **Order, declarations and the migration's premises.** Verified above; unique `order = 117`, single out-of-place row, unchanged position/citation partition, `workflow-calibration` still "order 35 and position 35 alike" (`plan-order-array-position.md:433`).
- **Current/prior/future/unowned owner routes.** `:34,35,51-60` are internally consistent with criterion 4 (`:161`), `Complete` (`:37`), `TerminalChoice` (`:36`), the fixtures (`:71`) and the mutation classes (`:134`). Acceptance is a phase in the frozen order, so acceptance-to-completed-work correctly takes `CompletedPriorOwner`, and a future route is unconstructible in the last phase.
- **Algebra.** `C_q`, `R_B` and `I_B` re-derive exactly from the stated per-batch and per-repair costs (shown above); `L_B` sums the per-phase minima over `p = m + 1` phases plus `r_plan`. `n_q = 0` correctly yields the blind-closure batch.
- **Commands.** The `nix shell nixpkgs#python3 -c python3 ...` form matches the repository's established invocation (`Q-86-safety-process.md:536-547`); `-c` consumes the remaining arguments, so `--suite`/`--floor` reach the script. `PYTHONDONTWRITEBYTECODE=1` on all five commands correctly forecloses the `__pycache__` artefact the mutation runner's import would otherwise create, which criterion 13's manifest would then flag.
- **Traceability parser contract.** Satisfiable against the actual sources: 1:1 heading-to-verdict pairing in all five files, no stray `### T` sections, 51 derived valid identities. Note for the implementer rather than as a finding: round 1 spells the record `- **Verdict and severity:**` while rounds 2 to 5 spell it `- **Verdict:**`, so a single-format parser fails closed on round 1, which is the specified behaviour.
- **Mutations and acceptance.** Criteria 1-15 map onto the body sections without a gap I could find; the tag/mutation count equality was settled invalid in round 1 (`q86-decision-r1-triage.md:48-54`) and I have no new evidence against that verdict.
- **Failure return.** Reopening Q-86 is legal under the plan schema: W4 requires a decision receipt for every `decided` item, not `decided` status for every receipt (`src/workflow.rs:309-345`), so returning Q-86 to `open` with `folded_into` dropped keeps `validate --workflow` green.
- **No production authority.** No file under `src/`, `tests/`, `pack/`, `README.md` or `CHANGELOG.md` is touched by the fold (`git diff --name-only main...HEAD` lists only `docs/`), the two appended records are `type:"decision"` receipts matching their structured questions exactly, and the step's boundary (`:3,5,24,172,182`) forbids production surfaces and blocks every later implementation unit on this proof.
- **Documentation impact.** The step and both folds correctly claim no shipped documentation is made stale; the retained brief, state-machine and safety-process status boundaries were all moved to the decided state.

## Summary

`critical`: 0. `high`: 0. `medium`: 2 (F1, F2). `low`: 1 (F3).
