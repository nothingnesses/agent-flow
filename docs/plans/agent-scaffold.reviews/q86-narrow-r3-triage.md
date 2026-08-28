# Narrowed Q-86 round 3 triage

## Scope and reproduction

I independently triaged the risky narrowed Q-86 decision artefact at `8fb6454a...152e316e`. `git diff --name-only 152e316e..HEAD` contains only the two round-3 reviewer reports, so the reviewed product at the tip is unchanged. I read `AGENTS.md`, the triager prompt, Q-86/Q-88 records and sidecars, the narrowed synthesis and retained proposals, the prior narrowed reviews and triages, and both round-3 reviews. I did not edit the reviewed product, plan, metrics, or earlier records.

`nix develop -c cargo run --quiet -- render --check --strict docs/plans/agent-scaffold.plan.toml` passed. `nix develop -c cargo run --quiet -- validate --source docs/plans/agent-scaffold.plan.toml --workflow` passed with 487 valid metrics records, 114 valid steps, 88 valid questions, and workflow invariants holding.

I reproduced the table claims with `nix run nixpkgs#cmark-gfm -- --extension table`. The synthesis table's header and ordinary rows have five pipes, while its whole-family row has seven. GFM consequently renders its B cell as `` `r_plan + `` and its C cell as `O`, dropping the remainder and the Option C cell. The same reproduction for the safety-process Principle table renders its M2 cell as `` `4 `` and its M3 cell as `O`, dropping its intended M3 text. A minimal GFM table with an unescaped pipe inside a code span reproduces the same split; an escaped pipe does not.

I also reproduced the B scope, sidecar, and digest evidence from the cited sources. The narrowed synthesis restricts `n_q` to post-freeze phases at `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md:103-105`, but labels two table rows as “plan or work phase” at `:156-157`. The Q-86 sidecar gives Q-78 consequences for A and C at `docs/plans/agent-scaffold.questions/Q-86.md:7,9`, but none for B at `:8`; the existing qualified B consequence is at `docs/plans/agent-scaffold.plan.toml:2566` and `Q-86-synthesis.md:131`. Finally, `sha256sum docs/plans/workflow-calibration.explorations/q86-controller-proof.py` returns `8a349c68dbe18df43d1d60d4110e11b3e216d97cdf4efb9f7e7328693d668175`; `git show ad989b5f:docs/plans/workflow-calibration.explorations/q86-controller-proof.py | sha256sum` returns the published `d0dabe6da04fde2009a2baf22d0a3d9fabdfbd6bc96d2859d26043531aff579a`, and `git show d20a4af9:docs/plans/workflow-calibration.explorations/q86-controller-proof.py | sha256sum` returns the current digest. The difference is the subsequently required in-file prototype caveat.

## Deduplication and no-relitigation

The three Claude findings and one GPT finding are distinct; there are four raw findings and no duplicates. None reopens a settled verdict without new evidence that its verdict was wrong. The B claim is the remaining cost-table surface, not a re-adjudication of synthesis round-3 T3's plan-controller decision; T3's correction explicitly repaired the ask and question sidecar, while this table still mislabels the plan phase. The sidecar claim is not synthesis round-4 T7's rejected claim that B is absent from the decision material: it concerns the locally unbalanced narrowed sidecar, which now presents A and C Q-78 consequences directly. The table-parser and digest claims have not previously been adjudicated.

## Verdicts

### T1 — unescaped table delimiters discard decision content in GFM renderers

- **Source:** `docs/plans/agent-scaffold.reviews/q86-narrow-r3-reviewer-claude.md`, finding 1.
- **Verdict:** valid, **low**.
- **Evidence:** `Q-86-synthesis.md:159` has six cells under a four-column table because its B formula contains unescaped `|O|`; GFM truncates the formula and drops Option C's whole-family minimum. `Q-86-safety-process.md:445` has the same defect in its M2 formula and drops the M3 cell. Both exact renders reproduced as described above.
- **Reasoning:** The narrowed synthesis is the designated decision artefact, and its cost comparison is meant to show all three family minima together. The raw source and nearby prose retain the formulas, so this is a recoverable presentation defect rather than a changed bound or implementation authority.
- **Correction:** Escape the cardinality delimiters in both table cells (for example, `` `r_plan + \|O\| + m + 1` `` and `` `4\|O\| + m + 8` ``), or restate them without pipes. Re-render each table through a GFM parser and keep every body row at the header width.

### T2 — B's cost table applies a post-freeze symbol to plan review

- **Source:** `docs/plans/agent-scaffold.reviews/q86-narrow-r3-reviewer-claude.md`, finding 2.
- **Verdict:** valid, **low**.
- **Evidence:** B “reuses A's sealed controller for plan review” at `Q-86-synthesis.md:103`, and defines `n_q = |O_q|` only “for post-freeze phase `q`” at `:105`. Its correct whole-family minimum uses a separate `r_plan` term at `:112-119`. The “Low-risk plan or work phase” and “Risky plan or work phase” table rows at `:156-157` nevertheless price B as `n_q + 1`, where `n_q` is undefined for plan review. The Q-86 sidecar and structured ask correctly qualify the same per-phase formula as post-freeze at `docs/plans/agent-scaffold.questions/Q-86.md:8` and `docs/plans/agent-scaffold.plan.toml:2566`.
- **Reasoning:** The source and whole-family algebra correctly distinguish inherited A plan review from post-freeze B campaigns, but the comparison table does not. A reader cannot price B's low- or risky-plan review from that table, and its apparent per-phase result conflicts with the stated whole-family model. This documents a proposed cost allocation and leaves the selected-option proof gate intact, so it is low.
- **Correction:** Split plan review from post-freeze work rows, or qualify the B cells: use A's one-batch/two-call low-risk plan minimum and two-batch/four-call risky-plan minimum, while retaining `n_q + 1` and `2(n_q + 1)` only for post-freeze work phases. Do not change the published family bounds.

### T3 — the Q-86 sidecar omits B's qualified Q-78 consequence

- **Source:** `docs/plans/agent-scaffold.reviews/q86-narrow-r3-reviewer-claude.md`, finding 3.
- **Verdict:** valid, **low**.
- **Evidence:** The sidecar states A's pass-seven/three-low tail at `Q-86.md:7` and C's pass-three/23-shortfall tail at `:9`, but B's bullet at `:8` has no Q-78 consequence. The existing B statement is already qualified as counterfactual in the structured ask at `agent-scaffold.plan.toml:2566` and synthesis at `Q-86-synthesis.md:131`: if each of four observed folds changes the structured digest, B requires four terminal replans and four additional plan-review and freeze campaigns.
- **Reasoning:** Narrowed round-2 T1 correctly required the sidecar to give A's replay result alongside C's. With A and C now directly carrying Q-78 effects, the recommended B alone has none in the same three-option reader path. This is not a claim that decision material lacks B's comparison; it is a local balance defect in the sidecar. The result remains available three lines above in the structured queue and in the synthesis, and must retain its counterfactual qualification, so impact is low.
- **Correction:** Add B's existing qualified statement to `Q-86.md:8`: under the explicit counterfactual assumption that four observed Q-78 folds each change its structured digest, it requires four terminal replans and four additional plan-review and freeze campaigns. Re-render the generated projection.

### T4 — published controller digest does not identify the retained file

- **Source:** `docs/plans/agent-scaffold.reviews/q86-narrow-r3-reviewer-gpt.md`, finding 1.
- **Verdict:** valid, **low**.
- **Evidence:** The current retained controller hashes to `8a349c68dbe18df43d1d60d4110e11b3e216d97cdf4efb9f7e7328693d668175`, but `Q-86-safety-process.md:403` presents `d0dabe6da04fde2009a2baf22d0a3d9fabdfbd6bc96d2859d26043531aff579a` as its SHA-256. The exact reproduction instructions include `sha256sum "$CHECKER"` at `:552` and then call the output current at `:555`, while retaining the old digest. The old digest reproduces only for `ad989b5f`; the current caveated file at `d20a4af9` and tip has the new digest. `Q-86-state-machine.md:467` repeats the unbound old digest for a historical run.
- **Reasoning:** The documents correctly quarantine the script as an incomplete adversarial prototype, so the mismatch grants no safety or implementation authority. It nevertheless makes the published reproduction instructions fail to identify the file they name and leaves “historical” insufficiently bound to a revision.
- **Correction:** Publish `8a349c68dbe18df43d1d60d4110e11b3e216d97cdf4efb9f7e7328693d668175` as the current retained-file digest. If retaining `d0dabe...`, label it explicitly as the historical executable-body digest at commit `ad989b5f`, including in the state-machine reproduction text. Do not expand the prototype's deferred proof scope.

## Outcome and counts

**Outcome: `new_valid`.** Four raw findings deduplicate to **four valid low findings**. Counts: critical 0, high 0, medium 0, low 4, invalid 0. No residual risk was accepted.

## Backstop

No high- or critical-severity finding was dismissed. **No independent dismissal backstop re-check is owed.**
