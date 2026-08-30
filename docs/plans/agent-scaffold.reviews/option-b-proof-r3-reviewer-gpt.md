# Option B proof work review round 3 — GPT

## Scope and result

I independently reviewed `main...fba79947` against `AGENTS.md`, `.agents/prompts/reviewer.md`, `bounded-convergence-option-b-proof`, all proof files and fixtures, and the round-1 and round-2 triages. I treated the proof as risky and attacked the oracles rather than relying on their summaries.

I found **seven findings: one critical, three high, two medium, and one low**. In the round-2 verification matrix, ten fixes are complete and two are incomplete (T5 and T12). The exact receipt-order/state fix in T1 is effective, but a different fresh-evidence state omission still lets receipt replay certify illegal reopen authority (F4).

## Exact commands, repeatability, and public-tree boundary

I ran all five exact sidecar commands twice from the repository root. Each of the ten invocations used a distinct external temporary directory for `HOME`, `TMPDIR`, `TEMP`, `TMP`, `PYTHONPYCACHEPREFIX`, and XDG cache/state/config/data/runtime variables. Every command's stdout, stderr, and exit status was byte-identical across passes. All ten exited 0 and reported:

- high all-suite: all nine failure counters zero;
- critical all-suite: all nine failure counters zero;
- algebra: all five contracted formulas and all failure counters zero;
- traceability: `valid_findings=51 executable_rows=30 resolved_rows=30 exercised_rows=30 killed_rows=30 unresolved=0`;
- mutation manifest: `discovered_tags=185 mutations=185 unexercised=0 survived=0`.

`git status --porcelain=v1 --untracked-files=all` and a complete non-Git path/type/content manifest, including ignored paths, were byte-identical before the first and after the tenth invocation. `git diff --check main..fba79947` passes. The diff remains planning-only: the 13 authorised files under `docs/plans/workflow-calibration.proofs/` and no production, pack, ledger, metrics, README, changelog, or generated product file.

Every destructive demonstration below ran in a fresh `git archive fba79947` extract outside the repository and was removed afterwards.

## Findings

### F1 — Conflicting duplicate authority projections collapse to the first report and can construct `Complete`

- **Severity:** critical.
- **Evidence:** `HistoryQuotient.extend` checks root, parent, severity, discovery phase, canonical owner, and obligation at `q86-option-b-proof.py:403-429`, but omits scope, triage, route, and disposition. A duplicate therefore always keeps the first record and merely joins reviewer/evidence values. That contradicts the quotient contract that authority-bearing scope and dismissal axes are preserved and that a duplicate can add only attribution/evidence under an exact identity check (`q86-option-b-spec.md:65-69`).
- **Reproduction:**

  ```sh
  root=$(mktemp -d /tmp/q86-r3-conflicting-duplicate.XXXXXX)
  git archive fba79947 | tar -x -C "$root"
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 - "$root/docs/plans/workflow-calibration.proofs/q86-option-b-proof.py" <<'PY'
  import importlib.util, sys
  from dataclasses import replace
  from pathlib import Path
  p=Path(sys.argv[1]); s=importlib.util.spec_from_file_location('q86_dup',p)
  m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m)
  family=m.make_family((1,),('build',),risk='low',family_id='duplicate-conflict')
  dismissed=m.FindingInput('D','D',None,m.Severity.HIGH,m.ScopeRelation.IN_SCOPE,m.TriageDisposition.DISMISSED,'E-dismissed','r1','build','build','O-0-0')
  valid=replace(dismissed,triage=m.TriageDisposition.VALID,evidence_id='E-valid',reviewer='r2')
  campaign=family.campaign('build').initial_batch(m.ReviewBatch('O-0-0',(dismissed,valid)))
  record=campaign.history.as_map()['D']
  print(record.triage_disposition.value, record.reviewers, record.evidence_ids)
  campaign=campaign.dismissal_recheck('D',False).blind_closure(m.ReviewBatch(None,()))
  complete=family.complete((campaign,))
  print(type(complete).__name__,complete.history.as_map()['D'].triage_disposition.value)
  PY
  rm -rf "$root"
  ```

  Output:

  ```text
  AwaitingDismissalRecheck ('r1', 'r2') ('E-dismissed', 'E-valid')
  Complete dismissal-upheld
  ```

- **Consequence:** One reviewer supplied a valid high finding, but the earlier dismissed duplicate controls the authority projection; upholding only that projection permits delivery. This falsifies the arbitrary finite-map induction and the central family-delivery claim. No manifest mutation covers a same-id scope/triage disagreement.

### F2 — Decision receipts do not bind the human's chosen action, and terminal receipts can be replayed across families

- **Severity:** high.
- **Evidence:** Successor binding requires only `receipt.chosen in receipt.options` at `q86-option-b-proof.py:1536-1545`; it never requires the human to have chosen `replan`. Terminal binding likewise checks `receipt.choice == kind` and membership only at `:1690-1704`, while `TerminalReceipt` has no family identity at `:1463-1467`. This is weaker than the exact chosen-successor contract in `bounded-convergence-option-b-proof.md:136`.
- **Reproduction:**

  ```sh
  root=$(mktemp -d /tmp/q86-r3-receipt-choice.XXXXXX)
  git archive fba79947 | tar -x -C "$root"
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 - "$root/docs/plans/workflow-calibration.proofs/q86-option-b-proof.py" <<'PY'
  import importlib.util,sys
  from pathlib import Path
  p=Path(sys.argv[1]); s=importlib.util.spec_from_file_location('q86_receipt',p)
  m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m)
  fx=m.load_fixture('successors.json'); reg=m.GlobalRegistry()
  for row in fx['families']:
      records=tuple(m.finding_from_input(m.fixture_finding(x),str(x['discovery']),tuple(fx['phases'])) for x in row['findings'])
      reg.add_existing(m.FamilyRecord(row['id'],row['parent'],row['digest'],row['terminal'],row['spend'],m.HistoryQuotient(records)))
  d=fx['receipt']
  receipt=m.SuccessorReceipt(d['predecessor'],d['successor'],d['predecessor_digest'],d['successor_digest'],tuple(d['carried_findings']),d['predecessor_spend'],tuple(d['options']),'revert')
  print('successor_from_revert',reg.authorise_successor(d['predecessor'],d['successor'],d['successor_digest'],receipt).family_id)
  terminal=m.TerminalReceipt(m.TerminalKind.ABANDON,('abandon','replan'),'replan')
  print(m.terminal_choice('family-a',m.Floor.HIGH,m.TerminalKind.ABANDON,(),terminal))
  print(m.terminal_choice('family-b',m.Floor.HIGH,m.TerminalKind.ABANDON,(),terminal))
  PY
  rm -rf "$root"
  ```

  Output includes `successor_from_revert family-3` and two accepted `TerminalChoice(... kind=ABANDON ... chosen='replan')` values for different families.
- **Consequence:** The model can replan when the human chose revert, or abandon arbitrary families using one receipt for a different action. The mutation named `successor-exact-receipt-binding` weakens the existing predicate but does not establish the missing chosen-action relation.

### F3 — Reconstructing an append-only family history without receipt history permits a second successor

- **Severity:** high.
- **Evidence:** `GlobalRegistry.add_existing` stores a `FamilyRecord` without validating its parent relation or requiring the corresponding receipt (`q86-option-b-proof.py:1512-1515`). `authorise_successor` detects a prior choice only through `predecessor_id not in self.receipts` at `:1531`; it does not derive the already-existing child relation from `families`. The shipped successor fixture itself reconstructs `family-2` as a child of `family-1` without the `family-1` receipt, but the oracle never asks for another fresh child of `family-1`.
- **Reproduction:**

  ```sh
  root=$(mktemp -d /tmp/q86-r3-second-successor.XXXXXX)
  git archive fba79947 | tar -x -C "$root"
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 - "$root/docs/plans/workflow-calibration.proofs/q86-option-b-proof.py" <<'PY'
  import importlib.util,sys
  from pathlib import Path
  p=Path(sys.argv[1]); s=importlib.util.spec_from_file_location('q86_successor',p)
  m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m)
  registry=m.GlobalRegistry()
  registry.add_existing(m.FamilyRecord('P',None,'pd',True,3,m.HistoryQuotient()))
  registry.add_existing(m.FamilyRecord('C','P','cd',True,4,m.HistoryQuotient()))
  receipt=m.SuccessorReceipt('P','S','pd','sd',(),3,('replan','abandon'),'replan')
  print(registry.authorise_successor('P','S','sd',receipt))
  print(sorted((row.family_id,row.parent_id) for row in registry.families.values()))
  PY
  rm -rf "$root"
  ```

  The command accepts `S`; the final registry contains both `('C','P')` and `('S','P')`.
- **Consequence:** Receipt/family reconstruction can lose the one-successor authority already spent by a predecessor, contrary to the append-only, no-omitted-links contract (`q86-option-b-spec.md:128-130`). The current one-successor mutation exercises only two calls in the same live registry.

### F4 — Current-campaign evidence is absent from receipt replay's global evidence registry, so same-evidence reopen reaches `Complete`

- **Severity:** high.
- **Evidence:** `PhaseCampaign.reopen` delegates freshness to the caller-supplied registry at `q86-option-b-proof.py:939-974`, and `EvidenceRegistry.reopen` checks only its own set at `:1588-1622`. Receipt replay seeds its local registry only from `exact_starting_history` at `:1139-1179`; it never registers evidence introduced by an `initial-review` receipt. A caller can therefore pass an empty registry, reuse the finding's original evidence id, and obtain a campaign that the new exact receipt replay also accepts.
- **Reproduction:**

  ```sh
  root=$(mktemp -d /tmp/q86-r3-same-evidence.XXXXXX)
  git archive fba79947 | tar -x -C "$root"
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 - "$root/docs/plans/workflow-calibration.proofs/q86-option-b-proof.py" <<'PY'
  import importlib.util,sys
  from pathlib import Path
  p=Path(sys.argv[1]); s=importlib.util.spec_from_file_location('q86_evidence',p)
  m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m)
  family=m.make_family((1,),('build',),risk='low',family_id='same-evidence')
  item=m.FindingInput('F','F',None,m.Severity.LOW,m.ScopeRelation.IN_SCOPE,m.TriageDisposition.VALID,'E-old','r','build','build','O-0-0')
  campaign=family.campaign('build').initial_batch(m.ReviewBatch('O-0-0',(item,)))
  campaign=campaign.repair(('F',)).verify(('F',))
  campaign=campaign.reopen(('F',),'E-old',m.EvidenceRegistry())
  campaign=campaign.repair(('F',)).verify(('F',)).blind_closure(m.ReviewBatch(None,()))
  complete=family.complete((campaign,))
  print(type(complete).__name__,complete.history.as_map()['F'].evidence_ids)
  print([t.evidence_id for t in campaign.transitions if t.kind=='reopen-review'])
  PY
  rm -rf "$root"
  ```

  Output:

  ```text
  Complete ('E-old',)
  ['E-old']
  ```

- **Consequence:** Same-evidence relitigation mints reopen authority and passes the exact receipt-derived completion gate, contrary to `bounded-convergence-option-b-proof.md:140,224`. The existing freshness mutation works only because its oracle manually preloads `E-old`; the legal campaign/delivery path does not conserve that global state.

### F5 — A shared replay route defect survives every exact command and all 185 mutations

- **Severity:** medium.
- **New evidence beyond round-2 T2:** The new independent event accountant closes shared spend/remaining-authority defects, but no independent oracle anchors the event stream's owner-route results. `ReplayState.apply` writes the shared reducer's route at `q86-option-b-proof.py:1781-1803`; `check_replay` at `:3090-3113` compares five snapshots to another use of that reducer and asserts only family id and authority coordinates. All per-view route mutations still happen after reconstruction.
- **Reproduction:**

  ```sh
  root=$(mktemp -d /tmp/q86-r3-replay-route.XXXXXX)
  git archive fba79947 | tar -x -C "$root"
  proof="$root/docs/plans/workflow-calibration.proofs/q86-option-b-proof.py"
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 - "$proof" <<'PY'
  from pathlib import Path
  import sys
  p=Path(sys.argv[1]); text=p.read_text()
  old='            self.routes[finding] = route.value\n'
  assert text.count(old)==1
  p.write_text(text.replace(old,'            self.routes[finding] = OwnerRoute.CURRENT.value\n'))
  PY
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 "$proof" --suite all --floor high
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 "$root/docs/plans/workflow-calibration.proofs/q86-option-b-mutations.py" --all
  rm -rf "$root"
  ```

  Both commands exit 0 with all suite counters zero and `discovered_tags=185 mutations=185 unexercised=0 survived=0`, even though the fixture's `F-scope-high` event is canonically owned by acceptance and is reconstructed as `CurrentOwner` in every view.
- **Consequence:** The replay oracle can falsely report route-preserving resume/rename/rebuild/replan reconstruction. This leaves the spec's “Every compared field is derived” and every-owner-route claim (`q86-option-b-spec.md:157`) unproved despite fixing the narrower authority arithmetic defect.

### F6 — The real `main` CLI-to-suite handoff remains unprotected

- **Severity:** medium.
- **New evidence beyond round-2 T5:** `model_from_parsed_command` now has a killing floor mutation (`q86-option-b-proof.py:3773-3780`), but the oracle invokes that helper directly. The actual `main` handoff at `:3877-3880` can still substitute `Floor.HIGH`; `run_suite` then consistently receives and constructs high, while output uses the original critical command for its label.
- **Reproduction:**

  ```sh
  root=$(mktemp -d /tmp/q86-r3-cli-floor.XXXXXX)
  git archive fba79947 | tar -x -C "$root"
  proof="$root/docs/plans/workflow-calibration.proofs/q86-option-b-proof.py"
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 - "$proof" <<'PY'
  from pathlib import Path
  import sys
  p=Path(sys.argv[1]); text=p.read_text()
  old='    failures = run_suite(command)\n'
  assert text.count(old)==1
  p.write_text(text.replace(old,'    failures = run_suite(ParsedCommand(command.suite, Floor.HIGH))\n'))
  PY
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 "$proof" --suite all --floor critical
  PYTHONDONTWRITEBYTECODE=1 nix shell --inputs-from . nixpkgs#python3 -c python3 "$root/docs/plans/workflow-calibration.proofs/q86-option-b-mutations.py" --all
  rm -rf "$root"
  ```

  The critical command still prints `comparison_floor=critical` with all counters zero, and the mutation command still reports all 185 killed.
- **Consequence:** The exact public critical invocation can again become label-only without any declared survivor. T5's required CLI-to-suite boundary fix is incomplete.

### F7 — Importing the public runner without the exact command's environment still creates repository bytecode

- **Severity:** low.
- **New evidence beyond round-2 T12:** The runner correctly stopped deleting pre-existing cache, but `sys.dont_write_bytecode = True` at `q86-option-b-mutations.py:8` executes only after Python's loader has already compiled/cached the runner itself. `run_manifest` snapshots only after that import at `:96-104`, and its external-cache regression tests a different module after suppression is active.
- **Reproduction:**

  ```sh
  root=$(mktemp -d /tmp/q86-r3-public-cache.XXXXXX)
  git archive fba79947 | tar -x -C "$root"
  cat >"$root/probe.py" <<'PY'
  import importlib.util,sys
  from pathlib import Path
  p=Path(sys.argv[1]); s=importlib.util.spec_from_file_location('q86_public_runner_probe',p)
  m=importlib.util.module_from_spec(s); sys.modules[s.name]=m
  print('before',list(p.parent.rglob('*.pyc')))
  s.loader.exec_module(m)
  print('after_import',[str(x.relative_to(p.parent)) for x in p.parent.rglob('*.pyc')])
  print('entries',len(m.run_manifest('q86-option-b').entries))
  print('after_call',[str(x.relative_to(p.parent)) for x in p.parent.rglob('*.pyc')])
  PY
  env -u PYTHONDONTWRITEBYTECODE nix shell --inputs-from . nixpkgs#python3 -c python3 "$root/probe.py" "$root/docs/plans/workflow-calibration.proofs/q86-option-b-mutations.py"
  rm -rf "$root"
  ```

  Output begins with `before []`, then reports `after_import ['__pycache__/q86-option-b-mutations.cpython-313.pyc']`; the file remains after the 185-entry public call.
- **Consequence:** The five exact commands are clean because their caller sets `PYTHONDONTWRITEBYTECODE=1`, but the separately exposed in-process contract still creates a caller-visible planning-tree artifact. T12's public-cleanliness correction is incomplete, and `q86-option-b-spec.md:219` overclaims the public runner's boundary.

## Round-2 fix verification matrix

| Round-2 item | Round-3 result |
| --- | --- |
| T1 receipt order/state replay | Fixed for the adjudicated defect: closure-before-initial, forged `ClosedReopen`, missing/duplicate receipts, changed history, and wrong starting history are rejected; `mut-campaign-receipt-replay-required` dies in `complete-stage-gate`. F4 is a distinct missing global-evidence input to replay. |
| T2 independent authority conservation | Fixed for spend and remaining authority: the independent raw-event account checks all snapshots, and both reducer mutations die before snapshot comparison. F5 is a separate unanchored owner-route coordinate. |
| T3 earlier-batch referrals | Fixed: pre-closure scope/dismissal re-checks open matching attempt authority, unresolved earlier referrals block closure, and repair/verification can continue. |
| T4 unchanged-replan load-bearing check | Fixed: registry rejection is in the snapshot and removing the call is killed. F3 concerns incomplete append-only registry reconstruction, not omission of this call. |
| T5 CLI floor boundary | **Incomplete: F6.** The helper boundary is covered, but the actual `main -> run_suite` call can still substitute high while the public critical command and all mutations stay green. |
| T6 arbitrary-history semantics | Fixed for the three required extension coordinates: real campaign transitions route, re-check, repair, verify, close, and deliver after 257 settled identities. F1 is a newly tested conflicting-duplicate reduction case. |
| T7 dynamic algebra fixture partition | Fixed: seven semantic coordinates are required, every retained case drives real families, and coordinate-removal mutations die. |
| T8 independently derived maximum | Fixed: the delivery predicate no longer embeds `4n+1`; transition-token accounting rejects duplicate/out-of-capacity spend and maximum witnesses attain capacity. |
| T9 witness-specific cross-credit kill | Fixed: `run_mutation("mut-algebra-cross-credit")` now returns `AssertionError: L_q=2 < n_q+1=3` before maximum drivers. |
| T10 campaign fixture lifecycle | Fixed: each obligation lifecycle is joined to emitted transition kinds and closure is checked separately; the lifecycle-join mutation dies. |
| T11 dead fields/helpers | Fixed for the adjudicated fields: owner/history digests and phase accounts are asserted and mutated, `maximum_phase_witness` is called, and the unused parsed title was removed. |
| T12 pre-existing public bytecode | **Incomplete: F7.** Pre-existing cache is preserved, but loading the public runner itself without the exact command's environment creates a fresh `.pyc` before its internal suppression and snapshot. |

## Other adversarial checks that came back clean

- The mandatory cross-credit witness dies at the intended `L_q` assertion; transition capacity removal dies at the independent authority account; forged receipt replay dies at the family gate; unchanged-replan call removal dies at replay; history-extension coordinate removals and campaign fixture disconnection die in their named oracles.
- Receipt replay rejects out-of-order, missing, duplicate, unsupported, wrong-digest, wrong-start, changed-history, and attempt-state-inconsistent campaign products when evidence-registry state is otherwise complete.
- Dynamic registries, nonuniform partitions, actual minimum/maximum transition witnesses, earlier dual-axis settlement, future-owner closure activation, critical scope products, serious carry, legacy gates, source-derived traceability joins, and exact-command tree cleanliness passed the exercised cases.
- Documentation staleness is confined to proof/spec claims cited in F1, F3, F5, and F7; no shipped product documentation changed.

## Counts

- **Raw findings:** 7.
- **Deduplicated findings:** 7.
- **Critical:** 1.
- **High:** 3.
- **Medium:** 2.
- **Low:** 1.
- **Outcome:** `new_valid`.
