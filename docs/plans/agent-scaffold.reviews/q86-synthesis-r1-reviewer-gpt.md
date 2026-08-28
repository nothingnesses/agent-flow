# Q-86 synthesis round 1 review: formal model and mechanism distinctness

## Finding Q86-R1-GPT-1 - high - The exhaustive oracle cannot observe an earlier unresolved critical

**Evidence:** `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:103`, `:183`, and `:213` rely on exhaustive enumeration to say Options A and C terminate without critical completion and that all three mechanisms pass every red control. The cited checker does not retain open-finding state: Option A assigns `critical = 0` on every later `C`, `O`, `R`, `L`, or `H` observation (`docs/plans/workflow-calibration.explorations/Q-86-state-machine.md:441-455`), and the fixed-depth checker replaces `critical` with the current observation on every stage (`:475-487`). Its own explanation concedes that a later noncritical observation clears a pending critical in the toy model and that production would need an explicit repair plus verified disposition (`:554`). Therefore the oracle at `:537-540` can only ask whether the latest observation was critical, not whether any earlier critical remains open.

Reproduction, after extracting the fenced checker exactly as directed in the proposal:

```sh
awk 'BEGIN{found=0;inblock=0} /Save the following as `q86_exhaustive.awk`/{found=1} found && /^```awk$/{inblock=1; next} inblock && /^```$/{exit} inblock{print}' docs/plans/workflow-calibration.explorations/Q-86-state-machine.md > /tmp/q86_exhaustive.awk
printf '%s\n' KC KCC | awk -v mode=A -v phase=acceptance -v risk=risky -v report=1 -f /tmp/q86_exhaustive.awk
printf '%s\n' KCC | awk -v mode=A -v phase=work_review -v risk=risky -v report=1 -f /tmp/q86_exhaustive.awk
printf '%s\n' KCC | awk -v mode=B -v phase=acceptance -v risk=risky -v report=1 -f /tmp/q86_exhaustive.awk
```

Observed output:

```text
KC Complete 2 1 0
KCC Complete 2 1 0
KCC Complete 3 2 0
KCC Complete BlindClosure 3 0
```

Here explorer mode B is the fixed-depth protocol synthesised as Option C. The output is not itself proof that the prose mechanisms ship an unresolved critical; it is proof that the cited exhaustive oracle cannot distinguish an explicitly repaired-and-verified critical from an earlier critical erased by an unrelated later observation. Thus it cannot establish the safety property for which the synthesis cites it.

**Consequence:** The decision artifact declares the critical red control proved even though its executable oracle omits the load-bearing open-finding disposition. A human can select A or C on a false formal assurance about the exact condition the brief says a budget must never conceal.

**Smallest safe correction:** Replace the scalar with prospective finding/disposition state, make repair and verification explicit transitions, permit only verified resolution or removal from delivery to clear an open critical, and re-run exhaustive checks for the exact synthesised A and C controllers. Until that passes, describe termination as proved but the unresolved-critical invariant as specified rather than mechanically proved, and do not claim all red controls passed.

## Finding Q86-R1-GPT-2 - high - Option B's cited 107-state proof is a fixed-cap proxy, not the synthesised derived-budget controller

**Evidence:** The recommended Option B introduces initial obligation attempts, one prospective reopen, phase ownership and partitioning, a reserved blind closure batch, and the bound `2|O| + 8` (`docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:124-132`). It then says the safety proposal exhaustively checked the obligation controller (`:144`) and concludes every red control passed (`:213`). The cited safety proposal states `C2 = |O| * (r + 1) + 1` in prose (`docs/plans/workflow-calibration.explorations/Q-86-safety-process.md:313-317`), but its executable `m2` model has no reopen counter, obligation-attempt identity, phase partition, or blind-closure state. It hard-codes `CAP = 4` and `OBL0 = 2` (`:568-580`) and decrements the open-obligation count on `round_low` and `round_medium` as well as on `round_clean` (`:626-636`), even though a valid low or medium finding does not by itself settle the obligation under the synthesis. With `|O| = 2` and the synthesis's `r = 1`, the claimed post-freeze ceiling is 5, while the enumerated proxy's independent ceiling is 4.

Reproduction:

```sh
awk 'BEGIN{found=0;inblock=0} /^### A[.]3 `statemachine[.]awk`$/{found=1} found && /^```awk$/{inblock=1; next} inblock && /^```$/{exit} inblock{print}' docs/plans/workflow-calibration.explorations/Q-86-safety-process.md > /tmp/q86_statemachine.awk
awk -v MECH=m2 -f /tmp/q86_statemachine.awk </dev/null
```

The output starts with `parameters: ceiling=4 ... obligations=2` and reports 107 reachable states. No `r` or reopen state participates in that enumeration. The sealed outer counter does make a finite terminal event easy to impose, but this run does not prove the synthesis's typed progress rule, phase partition, reopen behavior, blind closure, or the stated derived bound over those transitions.

**Consequence:** The recommended hybrid has not met the brief's recommendation-eligibility requirement that the actual mechanism pass a stopping proof and the required path controls. In particular, the current text leaves ambiguous whether a finding-bearing batch consumes an initial attempt, what consumes a reopen when verification fails without materially new evidence, and how those transitions compose with no-transfer phase sub-accounts.

**Smallest safe correction:** Add one explicit state machine for the synthesised Option B, including phase/sub-account identity, monotone total spend, per-obligation initial and reopen state, finding dispositions, blind closure, re-checks, and terminal choices. Derive `2|O| + 8` from that transition system and exhaust the required paths. Alternatively, remove the claim that the 107-state run proves B and keep B non-recommendation-eligible until the focused schema/reconstruction proof of concept named at `Q-86-synthesis.md:228` succeeds.

## Finding Q86-R1-GPT-3 - medium - The rendered plan still says Q-86 is exploring

**Evidence:** The authoritative TOML now marks Q-86 `open` (`docs/plans/agent-scaffold.plan.toml:2560-2562`), and the Q-86 sidecar and workflow-calibration sidecar agree. However, the Success Criteria source still says the step "keeps Q-86 `exploring`" and merely schedules the design pass (`docs/plans/agent-scaffold.success-criteria.md:41`), so the regenerated projection repeats that stale state at `docs/plans/agent-scaffold.md:5111`. This is reproducible with:

```sh
rg -n 'Q-86.*exploring|keeps Q-86 `exploring`' docs/plans/agent-scaffold.success-criteria.md docs/plans/agent-scaffold.md
```

`nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` still reports "up to date" because rendering faithfully projects the stale tail sidecar.

**Consequence:** The durable human-readable plan simultaneously presents Q-86 as `open` at `docs/plans/agent-scaffold.md:179` and `:5063-5069` and as `exploring` at `:5111`. A resuming human or agent cannot rely on the generated plan for the decision boundary, and the changed artifact leaves a plan document stale despite claiming decision readiness.

**Smallest safe correction:** Update the Success Criteria source to say Q-86 is `open` after the completed synthesis, with no mechanism or behavior chosen until the human decision is receipted and folded, then re-render and run `render --check --strict`.

## Counts

- Critical: 0
- High: 2
- Medium: 1
- Low: 0

## Other proof commands run

```sh
jq -s 'map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | {passes: length, valid_shortfalls: map(.valid_findings)}' docs/metrics/workflow.jsonl
jq -s 'map(select(.type == "round" and .outcome == "clean" and .valid_findings > 0)) | {rounds: length, streaks_advanced: (map(select(.consecutive_clean > 0)) | length)}' docs/metrics/workflow.jsonl
jq -s '{critical_rounds: (map(select(.type == "round" and ((.severities // []) | index("critical")))) | length), dismissal_rechecks: (map(select(.type == "dismissal_recheck")) | length), results: map(select(.type == "dismissal_recheck") | .result)}' docs/metrics/workflow.jsonl
nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml
nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow
git diff --check main..HEAD
```

The selectors returned the synthesis's 10-pass sequence, 19 inconsistent clean rounds, one critical round, and one overturned dismissal re-check. Render and workflow validation passed; those checks do not detect the semantic proof gaps or stale sidecar above.
