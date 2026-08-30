# Option B proof work review round 3 triage

## Scope and reproduction

I independently read `AGENTS.md`, `.agents/prompts/triager.md`, the `bounded-convergence-option-b-proof` sidecar, the complete proof product, round-1 and round-2 triages, and both round-3 reviews. The reviewed change is `main...fba79947` / `HEAD` (`2c39216d`): the 13 authorised proof files under `docs/plans/workflow-calibration.proofs/`. `git diff --check main...HEAD` passes and the diff is planning-only.

I ran the five exact sidecar commands from the repository root with `PYTHONDONTWRITEBYTECODE=1` and external `HOME`, temporary, cache, and bytecode-cache paths. All passed: both all-suite invocations reported all nine counters at zero; algebra printed the five contracted formulas; traceability reported `valid_findings=51 executable_rows=30 resolved_rows=30 exercised_rows=30 killed_rows=30 unresolved=0`; and the manifest reported `discovered_tags=185 mutations=185 unexercised=0 survived=0`.

Every destructive reproduction below used a fresh `git archive HEAD` extract under `/tmp`, with only the stated mutation or probe, and the locked interpreter from `nix shell --inputs-from . nixpkgs#python3 -c python3`. Extracts and external state directories were removed after use. The standard command for a mutated model was `PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 docs/plans/workflow-calibration.proofs/q86-option-b-proof.py --suite all --floor high`; “all five” means the five exact commands in `bounded-convergence-option-b-proof.md:202-207`.

## Deduplication

There are 12 raw reviewer findings. Claude F5 and GPT F7 are the same public-runner bytecode leak and are one finding below. The remaining reports identify independently reproducible defects: the Claude delivery/mutation defects concern untested predicates and mutation-aware model code, while GPT F1 is a distinct actual `Complete` construction through a conflicting duplicate authority projection.

## Verdicts

### T1 — Family delivery-block predicate lacks a legal negative witness

- **Source:** Claude F1.
- **Verdict:** valid, **critical**.
- **Evidence:** In a scratch archive I replaced the sole `allowed = legal_campaigns and not any(blocks)` at `q86-option-b-proof.py:1454` with `allowed = legal_campaigns and not any(blocks[:0])`. All five exact commands still exited zero, including `185/185` killed mutations and `30/30` traceability rows. The eight blocker cases in `check_complete_gate` at `:3360-3410` append a record directly to a completed campaign history, so `_campaign_is_legal` rejects the unsupported receipt history before `FrozenFamily.complete` can exercise the `blocks` predicate at `:1428-1455`.
- **Reasoning:** The sidecar’s family-completion requirements explicitly forbid every listed live, pending, carried, terminal, and serious block. Neutralising their common gate without a failed proof command leaves the central safety assertion unproved.
- **Correction:** Construct each negative blocker through legal receipt-bearing transitions, then assert that the identified delivery conjunct rejects it. Cover at least live current/prior/future/unowned routes, carried state, both pending re-check axes, and terminal/serious scope; keep a positive control proving a clean legal family still completes.

### T2 — The reference model recognises mutation names and suppresses independent legality checks

- **Source:** Claude F2.
- **Verdict:** valid, **high**.
- **Evidence:** `FrozenFamily._campaign_is_legal` reads `ACTIVE_MUTATION` outside `point()` at `q86-option-b-proof.py:1363-1365`, `:1382-1383`, and `:1385-1395`. In a scratch archive I removed exactly those three conditionals. The high all-suite command remained green, but the manifest failed with ten survivors: `mut-family-exact-owner-keys`, `mut-family-legal-settled-attempts`, and the eight `mut-family-*-block` mutations. Thus the reported kills rely on mutation-name-specific bypasses rather than solely on ordinary property inputs.
- **Reasoning:** A mutation control must change the tested relation and be rejected by an independently constructed oracle. Reference-model branches that know the active mutation make the manifest self-certifying and, together with T1, overstate delivery coverage.
- **Correction:** Remove all direct `ACTIVE_MUTATION` reads from the model; retain mutation variation only through `point()`. Use the legal negative products from T1 so each individual delivery mutation fails at its named assertion without disabling sibling receipt checks.

### T3 — An oracle failure crashes category accounting and aborts the remaining suite

- **Source:** Claude F3.
- **Verdict:** valid, **medium**.
- **Evidence:** `ORACLES` registers `earlier-batch-referrals` at `q86-option-b-proof.py:2549`, but `run_suite`’s `categories` mapping at `:3798-3815` omits it before indexing `categories[name]` at `:3819`. In scratch I replaced the `earlier-recheck-opens-attempt` assignment at `:1037` with `opens = False`. The all-suite invocation exited 1 with the original `AssertionError`, followed by `KeyError: 'earlier-batch-referrals'`; it printed neither the architecture line nor the nine counters, and later oracles did not run.
- **Reasoning:** This fails closed, but violates the sidecar’s required failure report and hides subsequent independent oracle results whenever this assertion fails.
- **Correction:** Make the classification total (for example, assert `set(ORACLES) == set(categories)` before execution) and add `earlier-batch-referrals` to the intended category.

### T4 — The cross-owner earlier-referral reopen continuation is untested

- **Source:** Claude F4.
- **Verdict:** valid, **medium**.
- **Evidence:** In scratch I replaced only the second and third branches at `q86-option-b-proof.py:1044-1049` with `raise AssertionError("DEAD-BRANCH reached")`; both the high all-suite command and the complete mutation manifest still passed. The existing oracle at `:2549-2598` exercises only the first, same-scheduled-owner branch. A separate fresh probe created a two-owner `build` campaign: a high dismissed finding against `O-0-1` was retained in `O-0-0`’s initial batch, `O-0-1` then took its own initial batch, and the dismissal was overturned. It produced `O-0-1: OpenReopen`, then repair, verification, blind closure, and `Complete` in four batches.
- **Reasoning:** The sidecar requires the matching initial *or reopen* continuation. This legal delivering path and its no-authority rejection branch are neither exercised nor mutated.
- **Correction:** Add a fixture/oracle for this cross-owner referral, its `OpenReopen` accounting, and the rejection when no matching attempt remains; tag both currently unexercised branches.

### T5 — Conflicting duplicate reports erase a valid authority projection and permit `Complete`

- **Source:** GPT F1.
- **Verdict:** valid, **critical**.
- **Evidence:** `HistoryQuotient.extend` checks only root, parent, severity, discovery phase, canonical owner, and obligation at `q86-option-b-proof.py:402-429`; it omits scope and triage authority. In a scratch probe, one atomic initial batch supplied the same high finding id once as dismissed and once as valid. The quotient retained `AwaitingDismissalRecheck` from the first report while combining both reviewers. Upheld dismissal re-check, blind closure, and `family.complete` then produced `Complete`, despite the second report’s valid high finding.
- **Reasoning:** The sidecar’s quotient and induction argument permits duplicates to add only attribution or evidence under an exact authority check. Collapsing conflicting scope/triage state can suppress a blocker and directly defeats family delivery safety.
- **Correction:** Reject duplicate ids unless every authority-bearing projection agrees, including scope input/disposition, triage disposition, derived route, finding disposition, closure stage, lineage, ownership, and severity. Permit only attribution/evidence accumulation once that exact semantic identity check succeeds; add a killing conflicting-duplicate control.

### T6 — Decision-receipt validation accepts an action the human did not choose

- **Source:** GPT F2.
- **Verdict:** valid, **high**.
- **Evidence:** `GlobalRegistry.authorise_successor` requires only `receipt.chosen in receipt.options` at `q86-option-b-proof.py:1531-1547`, and `terminal_choice` has the analogous predicate at `:1690-1709`. In scratch, a successor receipt whose choices were `("replan", "revert", "abandon")` but whose `chosen` was `"revert"` nevertheless authorised `family-3`. A terminal receipt with durable choice `ABANDON` and chosen value `"replan"` also constructed `ABANDON` terminal choices.
- **Reasoning:** The sidecar requires a successor receipt with the chosen successor action and distinct receipted terminal choices. Accepting a replan or abandonment based on a different selected human action fabricates authority.
- **Correction:** Bind successor authorisation to the replan action and terminal authorisation to the requested terminal kind, not merely membership in presented options. GPT’s separate reuse-across-family demonstration does not independently establish a stated single-use terminal-receipt invariant; add receipt/family identity only if the planner explicitly makes that stronger constraint part of the selected model.

### T7 — Reconstructed family state can omit a prior successor receipt and mint another child

- **Source:** GPT F3.
- **Verdict:** valid, **high**.
- **Evidence:** `GlobalRegistry.add_existing` at `q86-option-b-proof.py:1512-1515` accepts a child record without validating the parent relation or receipt, while `authorise_successor` detects prior authority only in `self.receipts` at `:1517-1539`. In scratch I reconstructed terminal `P`, then existing child `C` with `parent_id="P"`, but no receipt. A new exact replan receipt for `P -> S` was accepted, leaving both `C` and `S` as children of `P`.
- **Reasoning:** The sidecar requires append-only exact ancestry with no omitted links and one chosen successor per predecessor. Reconstruction must conserve spent successor authority, not regain it when receipt history is absent.
- **Correction:** Validate reconstructed records and receipts together, reject an existing parent-child relation lacking its exact receipt, and derive the one-successor constraint from both receipts and existing ancestry. Add the reconstructed-child/second-successor negative case.

### T8 — Same evidence can reopen an initial finding and reach delivery

- **Source:** GPT F4.
- **Verdict:** valid, **high**.
- **Evidence:** `EvidenceRegistry.reopen` checks only its caller-provided set at `q86-option-b-proof.py:1580-1622`; `PhaseCampaign.initial_batch` never registers initial evidence, and receipt replay seeds its registry only from starting history at `:1139-1179`. In scratch, a low valid finding with initial evidence `E-old` was repaired and verified, then reopened with `E-old` against a new empty `EvidenceRegistry`. The campaign repaired, verified, blind-closed, and constructed `Complete`; its reopen receipt still named `E-old`.
- **Reasoning:** The sidecar requires globally fresh evidence, retention of old evidence, and rejection of same-evidence relitigation without reopen authority. This is a direct violation through ordinary campaign and completion APIs.
- **Correction:** Put evidence identity under immutable family/campaign authority, register every initial receipt’s evidence, and replay that registration before any reopen. Test a duplicate initial/reopen evidence id through the actual receipt-replay and delivery path.

### T9 — Replay checks agreement between shared reducers but not derived owner routes

- **Source:** GPT F5.
- **Verdict:** valid, **medium**.
- **Evidence:** `ReplayState.apply` derives and writes routes at `q86-option-b-proof.py:1781-1803`, while `check_replay` compares each view with another `reduce_replay` result at `:3090-3113`; the independent accountant checks only authority. In scratch I replaced the sole `self.routes[finding] = route.value` with `self.routes[finding] = OwnerRoute.CURRENT.value`. The high all-suite command and the complete 185-mutation manifest still passed, even though replay fixture `F-scope-high` is owned by `acceptance` and should be future-owned from `work-build`.
- **Reasoning:** The sidecar requires every compared route to be derived and route drift in every replay view to be killed. Shared agreement cannot prove route correctness.
- **Correction:** Independently derive expected route projections from the event stream and compare every snapshot to that derivation; add mutations before snapshot construction for each required route coordinate.

### T10 — The public `main` CLI handoff can silently replace the requested floor

- **Source:** GPT F6.
- **Verdict:** valid, **medium**.
- **Evidence:** `model_from_parsed_command` has a helper-level check at `q86-option-b-proof.py:3773-3785`, but `main` passes its parsed command directly at `:3877-3880` without a public-boundary oracle. In scratch I replaced `run_suite(command)` with `run_suite(ParsedCommand(command.suite, Floor.HIGH))`. `--suite all --floor critical` still printed `comparison_floor=critical` and all zero counters; the complete manifest also remained green.
- **Reasoning:** This reopens round-2’s label-only critical invocation at the actual command boundary, rather than only its helper boundary.
- **Correction:** Exercise `main` (or a subprocess of the exact public command) through a floor-sensitive model assertion and tag a mutation at the actual `main -> run_suite` handoff.

### T11 — Importing the documented public mutation runner creates planning-tree bytecode

- **Sources:** Claude F5; GPT F7.
- **Verdict:** valid, **low**.
- **Evidence:** `sys.dont_write_bytecode = True` runs inside `q86-option-b-mutations.py:8`, after Python has compiled and cached that module; the runner snapshots only later at `:101-105`. In a fresh scratch archive with both `PYTHONDONTWRITEBYTECODE` and `PYTHONPYCACHEPREFIX` unset, an `importlib` load of the runner changed `before []` to `after_import ['__pycache__/q86-option-b-mutations.cpython-313.pyc']`. `run_manifest("q86-option-b")` returned 185 entries and left that cache file in place.
- **Reasoning:** The five exact commands are clean because callers set the environment variable, but the separately exposed in-process runner does not meet the sidecar’s no-repository-mutation boundary on its documented import path.
- **Correction:** Provide and test a supported pre-import loader/wrapper that sets bytecode suppression before executing the runner module, or narrow the public contract so callers must establish that precondition before import. The module body alone cannot prevent its own loader’s prior cache write; the regression must snapshot before loading the runner itself.

## Outcome and counts

- **Raw reviewer findings adjudicated:** 12.
- **Deduplicated findings:** 11.
- **Valid:** 11 — 2 critical, 4 high, 4 medium, 1 low.
- **Invalid:** 0. GPT F2’s cross-family terminal-reuse observation is not counted as an additional finding because the current sidecar does not state that separate invariant; its wrong-chosen-action defect is valid.
- **Accepted residual risk:** 0.
- **Outcome:** `new_valid`.

## Backstop

No high- or critical-severity finding was dismissed. No independent dismissal re-check is owed. The valid critical and high findings prevent this risky proof increment from counting as a clean review round.
