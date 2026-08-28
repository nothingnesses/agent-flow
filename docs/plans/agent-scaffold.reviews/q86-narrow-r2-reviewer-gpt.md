# Narrowed Q-86 round 2 review — proof boundary and implementation gate

Reviewed risky artefact `aa6ee1d2...98e54e04` (`main...98e54e04`). I read `AGENTS.md`, the reviewer prompt, the Q-86 and Q-88 structured records and sidecars, the narrowed synthesis, the owning step and Success Criteria, both retained proposals and prototypes, the prior narrowed reviews and triage, and the round-5 synthesis triage. I did not require the deferred selected-option implementation proof.

## Result

**Zero findings.** Counts: critical 0, high 0, medium 0, low 0.

## Round-1 fix verification

1. **The change boundary is now exact.** `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:7` distinguishes unchanged workflow/production behaviour from the one Q-88 decision event and the required generated-plan projection.
2. **Proposal labels are mapped locally.** `Q-86-synthesis.md:15` maps synthesis A/B/C to state-machine Candidate A/Candidate B and safety M1/M2, while keeping M3 excluded and preserving the prototype caveat.
3. **The Q-88 heading hierarchy is repaired.** `docs/plans/agent-scaffold.questions/Q-88.md` now starts at `## Decision`; an outside-fence H1 scan of `docs/plans/agent-scaffold.md` returns only the plan title at line 3.
4. **Option C's minimum is derived.** `Q-86-synthesis.md:146` states the two-reviewer Discovery batch plus one-reviewer BlindClosure batch, yielding two batches and three calls.
5. **Both scripts carry local caveats.** `q86-controller-proof.py:2-4` and `q86-q78-scope-replay.sh:2-3` say their outputs are not safety or recommendation-eligibility proof and point to the synthesis boundary and round-5 triage.

## Fresh scope-boundary sweep

- **Prototype evidence is quarantined.** The narrowed synthesis explicitly rejects proof from zero counters (`Q-86-synthesis.md:41`), lists the prototype defects (`:43-58`), labels the shared package as requirements rather than established results (`:62`), and says the B premises remain unproved (`:127`). The retained proposals carry the same local status boundary at `Q-86-state-machine.md:3-5` and `Q-86-safety-process.md:3-5`. Running one controller mode and the replay self-test was a smoke check only; their output was not used to establish safety. The prior narrow triage's T6 disposition remains settled, and I found no new evidence that defeats it.
- **The option bounds are algebraically stated and qualified as proposed.** A derives `7(m + 2)` batches and `34(m + 2)` calls from fixed seven-batch slices (`Q-86-synthesis.md:79-93`). B states `n_q = |O_q|`, `C_q = 4n_q + 1`, `p = m + 1`, and derives `7 + sum(4n_q + 1) = 4|O| + m + 8`, with minimum and call bounds beside it (`:101-127`). C states four batches and fifteen calls per each of `m + 2` phases (`:133-146`). Each section routes its unproved safety premises to the selected-option proof rather than the retained prototype.
- **Every production implementation path remains blocked.** The authoritative synthesis makes the proof a separate risky Roadmap unit and an explicit blocker for every production implementation unit (`Q-86-synthesis.md:184-205`), permits implementation planning only after it passes (`:217-219`), and says the human choice authorises proof only (`:238-242`). The same gate and failure path appear in `agent-scaffold.questions/Q-86.md:23-29`, `agent-scaffold.steps/workflow-calibration.md:26`, and `agent-scaffold.success-criteria.md:41`. Failure returns Q-86 to the human with no automatic architecture or floor fallback.
- **Q-88 is exact.** There is exactly one `type:"decision"`, `q_id:"Q-88"` record. Its six options exactly match `agent-scaffold.questions/Q-88.md:5-12` in order; `recommendation` and `chosen` are both exactly `Narrow the proof scope`; `task` and `folded_into` are `workflow-calibration`; Q-86 remains `open` and Q-88 is `decided` with receipt `Q-88` in the TOML.
- **No current behaviour is authorised.** `Q-86-synthesis.md:17,219-242`, `agent-scaffold.questions/Q-86.md:41`, and the owning step at `workflow-calibration.md:20-30` consistently leave the architecture, floor, constants, cap/reset/acceptance changes, pack changes, and code changes undecided. `git diff --name-only main...98e54e04` contains planning, metrics, exploration, and generated-plan files only—no production source, pack, workflow-spec, README, or changelog path.
- **Documentation is current.** The structured sources and generated projection agree, the sidecar hierarchy is valid, and the implementation-impact inventory remains explicitly deferred until proof completion.

## Reproduction

- `nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` — up to date.
- `nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` — 486 metrics records and 114 steps / 88 questions valid; workflow invariants hold.
- Exact Q-88 `jq`/sidecar-label comparison — one matching receipt, six labels in order, exact recommendation/chosen/task.
- `git diff --check main...98e54e04` — clean.
- `q86-controller-proof.py --mode A ...` and `q86-q78-scope-replay.sh --self-test` — executable smoke checks passed; as their local headers and the synthesis state, this does not prove controller safety.
