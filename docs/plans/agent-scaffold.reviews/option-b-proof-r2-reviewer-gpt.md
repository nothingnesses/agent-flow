# Option B proof work review round 2 — GPT

## Scope and result

I independently reviewed `main...a167d71a` against `AGENTS.md`, `.agents/prompts/reviewer.md`, `bounded-convergence-option-b-proof`, the proof specification, all 13 proof artefacts and eight fixtures, the round-1 triage, and all five retained Q-86 source triages. I treated the artifact as risky and did not rely on its green summaries.

I found **five findings: one critical, one high, two medium, and one low**. There are no other findings.

## Exact commands, repeatability, and boundary

I ran all five exact sidecar commands twice from the repository root. Every invocation used a distinct external temporary directory for `HOME`, `TMPDIR`, `TEMP`, `TMP`, `PYTHONPYCACHEPREFIX`, and the XDG cache/state/config/data/runtime variables. Both passes had identical stdout, stderr, and exit status for each command. All ten exited 0 and reported:

- high all-suite: every failure count zero;
- critical all-suite: every failure count zero;
- algebra: the five contracted formulas and every failure count zero;
- traceability: `valid_findings=51 executable_rows=30 resolved_rows=30 exercised_rows=30 killed_rows=30 unresolved=0`;
- manifest: `discovered_tags=151 mutations=151 unexercised=0 survived=0`.

`git status --porcelain=v1 --untracked-files=all` and a complete non-Git path/type/content manifest, including ignored paths, were byte-identical before and after the ten invocations. `git diff --check main...HEAD` passes. The diff is exactly the 13 authorised files under `docs/plans/workflow-calibration.proofs/`; the Python imports are standard-library-only, and no production, pack, ledger, metrics, README, changelog, or generated product file changed.

Every destructive demonstration below ran in a fresh `git archive HEAD` extraction under `/tmp` and was removed afterwards.

## Findings

### F1 — The delivery constructor accepts impossible transition receipts and attempt states

- **Severity:** critical.
- **New evidence beyond round-1 T2:** The repair replaced forgeable `completed` booleans with transition summaries, but `FrozenFamily._campaign_is_legal` only counts one `blind-closure`, collects `initial-review` owner labels, checks that current states are members of `CLOSED_ATTEMPTS`, and applies numeric caps (`q86-option-b-proof.py:1047-1084`). It never replays transition order or derives attempt states from the receipts. This contradicts the specification that transition receipts derive every legal state (`q86-option-b-spec.md:116-118`) and the explicit promise that delivery constructors reject raw illegal products (`q86-option-b-spec.md:227`).
- **Reproduction:**

  ```sh
  root=$(mktemp -d /tmp/q86-forged-complete.XXXXXX)
  git archive HEAD | tar -x -C "$root"
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 - "$root/docs/plans/workflow-calibration.proofs/q86-option-b-proof.py" <<'PY'
  import importlib.util, sys
  from dataclasses import replace
  from pathlib import Path
  p = Path(sys.argv[1])
  s = importlib.util.spec_from_file_location("q86_forged", p)
  m = importlib.util.module_from_spec(s); sys.modules[s.name] = m; s.loader.exec_module(m)
  family = m.SealedPlanReview(m.converged_plan("low")).to_freeze_pending().freeze(m.load_fixture("freeze.json"), "forged-family")
  campaigns = []
  prior = family.history
  for phase in family.freeze.phases:
      base = family.campaign(phase, prior)
      states = tuple((owner, m.ObligationAttempt.CLOSED_REOPEN) for owner in base.expected_owner_keys)
      transitions = (m.CampaignTransition("blind-closure"),) + tuple(
          m.CampaignTransition("initial-review", owner, (), (owner,)) for owner in base.expected_owner_keys
      )
      forged = replace(base, obligation_states=states, transitions=transitions)
      campaigns.append(forged)
      prior = forged.history
  result = family.complete(tuple(campaigns))
  print(type(result).__name__, len(family.freeze.obligations))
  print([tuple(t.kind for t in c.transitions) for c in campaigns])
  print([tuple(s.value for _, s in c.obligation_states) for c in campaigns])
  PY
  rm -rf "$root"
  ```

  Output:

  ```text
  Complete 3
  [('blind-closure', 'initial-review'), ('blind-closure', 'initial-review'), ('blind-closure', 'initial-review')]
  [('ClosedReopen',), ('ClosedReopen',), ('ClosedReopen',)]
  ```

  Every closure occurs before its alleged initial review, and every obligation is in `ClosedReopen` despite having no reopen or verification receipt. The public delivery gate still constructs `Complete`.
- **Consequence:** The central complete-only safety gate does not prove that frozen obligations traversed the legal protocol. The 151-mutation manifest has no transition-order/state-derivation mutation, so its survivor count does not expose this unsafe constructor.
- **Correction:** Make campaign receipts sufficient to replay the state machine from the exact initial state, and have `complete` compare the replay-derived owner states, history, spend, closure position, and final product to the supplied campaign. Reject out-of-order, missing, duplicate, and state-inconsistent receipts. Add independent mutations for closure-before-attempt, `ClosedReopen` without reopen/verification, and history evolution unsupported by a receipt.

### F2 — Initial-review scope and dismissal referrals can only be re-checked after stale blind closure, then cannot take the overturned repair route

- **Severity:** high.
- **New evidence beyond round-1 T9:** The new campaign continuation methods repair closure-discovered re-checks, but both methods reject every call before `blind_closure_spent` (`q86-option-b-proof.py:943-952`). Conversely, blind-closure readiness only checks `repairable` records and ignores pending scope/dismissal axes (`q86-option-b-proof.py:955-963`). An initial serious dismissal therefore closes its obligation, permits blind closure while the re-check is pending, and, when overturned, has no open attempt authority for repair (`q86-option-b-proof.py:822`). This violates the rule that blind closure starts only after earlier current-owner components settle (`bounded-convergence-option-b-proof.md:84`) and that pending re-checks are never closure evidence (`bounded-convergence-option-b-proof.md:112`).
- **Reproduction:**

  ```sh
  root=$(mktemp -d /tmp/q86-preclosure-recheck.XXXXXX)
  git archive HEAD | tar -x -C "$root"
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 - "$root/docs/plans/workflow-calibration.proofs/q86-option-b-proof.py" <<'PY'
  import importlib.util, sys
  from pathlib import Path
  p = Path(sys.argv[1])
  s = importlib.util.spec_from_file_location("q86_recheck", p)
  m = importlib.util.module_from_spec(s); sys.modules[s.name] = m; s.loader.exec_module(m)
  family = m.make_family((1,), ("build",), risk="low", family_id="recheck-family")
  item = m.FindingInput("dismissed", "dismissed", None, m.Severity.HIGH, m.ScopeRelation.IN_SCOPE, m.TriageDisposition.DISMISSED, "E-dismissed", "reviewer", "build", "build", "O-0-0")
  c = family.campaign("build").initial_batch(m.ReviewBatch("O-0-0", (item,)))
  print(c.state_map()["O-0-0"].value, c.history.as_map()["dismissed"].triage_disposition.value)
  for label, action in (("pre", lambda: c.dismissal_recheck("dismissed", True)),):
      try: action()
      except Exception as e: print(label, type(e).__name__, str(e))
  c = c.blind_closure(m.ReviewBatch(None, ())).dismissal_recheck("dismissed", True)
  print("after", c.completed, c.state_map()["O-0-0"].value)
  try: c.repair(("dismissed",))
  except Exception as e: print("repair", type(e).__name__, str(e))
  try: family.complete((c,))
  except Exception as e: print("complete", type(e).__name__, str(e))
  PY
  rm -rf "$root"
  ```

  Output:

  ```text
  ClosedInitial AwaitingDismissalRecheck
  pre ValueError closure dismissal re-check requires closure evidence
  after True ClosedInitial
  repair ValueError repair has no unspent attempt authority
  complete ValueError family cannot construct Complete
  ```

  The same dead end applies to an initial high scope referral overturned into `InScope`.
- **Consequence:** A required legal current-owner continuation is absent and the model takes blind closure against a state that its own ordering excludes. The path cannot deliver unsafely, but only because it becomes permanently blocked and terminalises work that Option B says can be repaired and verified before closure.
- **Correction:** Distinguish pre-closure findings from closure-discovered findings. Permit per-id scope and dismissal re-checks before closure for earlier batches; on overturn, open the matching initial/deferred authority and require repair plus verification. Make blind closure reject every unresolved earlier scope or dismissal axis. Preserve the existing post-closure continuation only for `closure_discovery=True` records, where current/prior/unowned routes remain non-delivering.

### F3 — The mutation census misses the CLI floor boundary, so a label-only critical command still gets 151/151 kills

- **Severity:** medium.
- **Evidence:** The functional fix now passes `Floor(args.floor)` into `run_suite` at `q86-option-b-proof.py:3151`, but the only `floor-threaded-construction` mutation is inside `FreezePending.freeze`. It does not mutate or observe the CLI-to-suite call. In a scratch archive, replace exactly:

  ```text
  failures = run_suite(args.suite, Floor(args.floor))
  ```

  with:

  ```text
  failures = run_suite(args.suite, Floor.HIGH)
  ```

  Then run:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 docs/plans/workflow-calibration.proofs/q86-option-b-proof.py --suite all --floor critical
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 docs/plans/workflow-calibration.proofs/q86-option-b-mutations.py --all
  ```

  The mutant still reports:

  ```text
  architecture=FrozenObligationsWithSealedPhaseCampaigns comparison_floor=critical suite=all
  safety_failures=0 transition_failures=0 authority_failures=0 delivery_failures=0 legacy_failures=0 identity_failures=0 evidence_failures=0 product_failures=0 bound_failures=0
  manifest=q86-option-b discovered_tags=151 mutations=151 unexercised=0 survived=0
  ```

- **Consequence:** The exact critical command can regress to the round-1 label-only behavior while every declared mutation still dies, contrary to the requirement that the critical command exercise the comparison model (`q86-option-b-spec.md:9`) and that every load-bearing boundary have a killing mutation (`bounded-convergence-option-b-proof.md:192-196`).
- **Correction:** Put a mutation point on the parsed-floor handoff or invoke `main(["--suite", "all", "--floor", "critical"])` from an oracle that observes a floor-sensitive family produced only through that invocation. The mutant that substitutes `Floor.HIGH` must survive no command or manifest run.

### F4 — Removing every dynamic algebra fixture case leaves the algebra proof and full mutation manifest green

- **Severity:** medium.
- **Evidence:** `check_algebra` iterates whatever is present in `fixture["finite_cases"]` without asserting a required case family (`q86-option-b-proof.py:2609`). In a scratch archive, set `fixtures/algebra.json`'s `finite_cases` to `[]`, then run the exact algebra and mutation commands. Both still exit 0 with all five formulas, zero bound failures, and `discovered_tags=151 mutations=151 unexercised=0 survived=0`.
- **Reproduction:**

  ```sh
  root=$(mktemp -d /tmp/q86-empty-algebra-fixture.XXXXXX)
  git archive HEAD | tar -x -C "$root"
  nix shell --inputs-from . nixpkgs#python3 -c python3 - "$root/docs/plans/workflow-calibration.proofs/fixtures/algebra.json" <<'PY'
  import json, sys
  from pathlib import Path
  p = Path(sys.argv[1]); data = json.loads(p.read_text()); data["finite_cases"] = []; p.write_text(json.dumps(data))
  PY
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 "$root/docs/plans/workflow-calibration.proofs/q86-option-b-proof.py" --suite algebra --floor high
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 "$root/docs/plans/workflow-calibration.proofs/q86-option-b-mutations.py" --all
  rm -rf "$root"
  ```

- **Consequence:** The green algebra contract no longer establishes the claimed zero-, one-, and several arbitrary named phase registries (`q86-option-b-spec.md:196,207`). The current fixture contains those rows, but neither the oracle nor the manifest makes their continued presence and execution load-bearing, so the named fixture repair is not fail-closed.
- **Correction:** Require a semantic case partition rather than names alone: zero obligations/no work loops, one work loop, several dynamic phase names, empty and non-empty owners, and nonuniform owner distributions. Record which required coordinates executed and fail if any is absent. Add a mutation that removes each required coordinate family and is killed by the algebra oracle.

### F5 — The public mutation runner cleans up by deleting a pre-existing repository bytecode artifact

- **Severity:** low.
- **New evidence beyond round-1 T10:** `remove_runner_bytecode` unlinks the runner's cached file before taking its cleanliness baseline (`q86-option-b-mutations.py:23-31,94-97`). This removes a pre-existing ignored/untracked artifact, while the public contract is supposed not to create, remove, or change repository state. The regression only compares bytecode after that deletion.
- **Reproduction:**

  ```sh
  root=$(mktemp -d /tmp/q86-preexisting-bytecode.XXXXXX)
  git archive HEAD | tar -x -C "$root"
  cat >"$root/probe.py" <<'PY'
  import importlib.util, sys
  from pathlib import Path
  p = Path(sys.argv[1]); action = sys.argv[2]
  s = importlib.util.spec_from_file_location("q86_public_runner", p)
  m = importlib.util.module_from_spec(s); sys.modules[s.name] = m; s.loader.exec_module(m)
  cached = Path(m.__cached__)
  print("before_call", cached.exists(), cached)
  if action == "call":
      result = m.run_manifest("q86-option-b")
      print("after_call", cached.exists(), "entries", len(result.entries))
  PY
  runner="$root/docs/plans/workflow-calibration.proofs/q86-option-b-mutations.py"
  env -u PYTHONDONTWRITEBYTECODE nix shell --inputs-from . nixpkgs#python3 -c python3 "$root/probe.py" "$runner" import-only
  env -u PYTHONDONTWRITEBYTECODE nix shell --inputs-from . nixpkgs#python3 -c python3 "$root/probe.py" "$runner" call
  rm -rf "$root"
  ```

  Output:

  ```text
  before_call True .../__pycache__/q86-option-b-mutations.cpython-313.pyc
  before_call True .../__pycache__/q86-option-b-mutations.cpython-313.pyc
  after_call False entries 151
  ```

- **Consequence:** The exact five commands remain clean because they set `PYTHONDONTWRITEBYTECODE=1`, but the explicitly exposed in-process contract mutates a caller's pre-existing planning-tree state. This is the remaining edge of the round-1 public-cleanliness defect.
- **Correction:** Do not delete caller-owned cache state. Load the runner and all sibling modules with bytecode suppression established by an external wrapper before import, or direct every loader cache to external temporary state. Snapshot before any cleanup and require exact before/after equality, including a pre-existing runner cache regression.

## Round-1 fix verification matrix

| Round-1 item | Round-2 result |
| --- | --- |
| T1 traceability pointer | Fixed: the stable sidecar pointer resolves and the exact in-process traceability command passes twice. |
| T2 family completion | **Incomplete: F1** supplies new evidence that impossible receipt/state products still construct `Complete`. |
| T3 real transition algebra | The shipped clean/maximum witnesses now use `PhaseCampaign` and `Complete`; no-op/repeated work is rejected and the real cross-credit path is killed. F1 and F4 remain independent delivery/coverage defects. |
| T4 reconstruction independence | Fixed for the reviewed paths: baseline, serialized resume, rename envelope, JSON rebuild, and unchanged-replan registry path are distinct; empty/start-only/noncanonical streams fail. |
| T5 fixture semantics | Product, campaign, successor, replay, and terminal bodies are now consumed. **F4** shows the required algebra case family is still optional to the oracle. |
| T6 floor threading | Functionally fixed at the reviewed tip, but **F3** shows the mandatory mutation does not protect the CLI boundary. |
| T7 deferred/second reopen | Fixed: deferred state is consumed by an executable transition, initial priority is checked, and a second reopen is rejected with distinct killed mutations. |
| T8 dynamic phase routing | Fixed in the transition model: the frozen registry is threaded, duplicate identities fail, and arbitrary names execute. **F4** concerns the separate dynamic algebra fixture gate. |
| T9 blind-closure re-checks | Closure-discovered re-check continuation and all four critical owner coordinates now execute. **F2** supplies new evidence that earlier-batch referrals are forced through stale closure and cannot continue after overturn. |
| T10 public cleanliness | Fresh direct calls no longer leave new bytecode, but **F5** shows cleanup removes pre-existing state. |
| T11 mandatory checker | Fixed: a missing checker fails before discovery, and all 18 checker controls participate in the 151-entry manifest. |

## Other adversarial checks that came back clean

- The retained-triage parser independently derives the same 51 valid round-qualified identities: R1 13, R2 12, R3 9, R4 8, and R5 9. The 51 matrix rows partition into 30 executable, 12 durable-text, and 9 Option-B-inapplicable rows. The corrected R1-T12 durable pointer resolves.
- Unknown, surviving, and unexercised mutation entries, wrong manifests, fabricated runner results, dropped joins, count suppression, duplicate/malformed triages, and matrix set changes fail the checker self-tests and live join.
- The real two-owner cross-credit mutant reaches the ordinary complete domain in two phase batches and is killed against the unmutated three-batch minimum. Maximum witnesses reject no-op, absent, repeated, and inexact repair/verification selections.
- Dynamic phase names and duplicate-phase rejection, deferred reopen ordering, second-reopen rejection, global family freshness, one successor per predecessor, exact receipt/ancestry/carry/spend, fresh evidence, legacy gating, terminal choices, critical non-delivery, future-owner activation, and the shipped closure owner/scope/triage products passed their exercised cases.
- Documentation currency and planning-only scope are otherwise clean. The false proof claims corresponding to F1-F4 are confined to the proof specification/sidecar under review; no shipped product documentation was made stale.

## Counts

- **Raw findings:** 5.
- **Deduplicated findings:** 5.
- **Critical:** 1.
- **High:** 1.
- **Medium:** 2.
- **Low:** 1.
- **Outcome:** `new_valid`.
