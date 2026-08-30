# Minimal project reset charter

## Diagnosis and non-goals

The Rust product is salvageable, but its local workflow is not serving delivery. Since 13 August, 92.2% of commits have been documentation-only. The current `next` command emits 765,503 bytes on this repository, mostly a verbatim and stale ledger, while the active planning state is about 2.9 MB. The Roadmap has 115 steps and 93 questions, four steps carry `in-progress` status, and only one implementation worktree was real when the proof loop paused. The process therefore hides work, reports a stale single loop as authoritative, and produces more state than the product can use. This reset does not rewrite the product from zero. It preserves the Rust source, pack, tests, released versions, tags, changelog, and Git history. It also preserves the two 13 August audit records as live evidence. It does not merge or continue the bounded-convergence proof, redesign the whole command set, erase history, push a branch, publish a crate, or make a release.

## Exact file disposition

After approval, `RESET.md` is the replacement charter. The old plan is evidence, not a template.

| Path or path family | Disposition | Result |
| --- | --- | --- |
| `RESET.md` | Retain as the approved reset charter | This is the only planning prose for the reset and remains at the repository root. |
| `.agents/work.toml` | Create as replacement active state | It contains no more than five ordered delivery steps, their status, blockers, and enough typed phase data for `next`. It is not a ledger or event log. |
| `docs/plans/agent-scaffold.plan.toml`, `docs/plans/agent-scaffold.md`, `docs/plans/agent-scaffold.ledger.md`, `docs/plans/agent-scaffold.*.md`, `docs/plans/agent-scaffold.steps/`, `docs/plans/agent-scaffold.questions/`, `docs/plans/agent-scaffold.explorations/`, and `docs/plans/agent-scaffold.reviews/` | Delete from the working tree after the audit copy is committed | Preserve only in Git history. No mega-plan, ledger, question corpus, step sidecars, exploration corpus, or transient review directory remains active. |
| `docs/plans/*.explorations/`, `docs/plans/*.build-plan.md`, and `docs/plans/*.design.md` | Delete from the working tree after the two exceptions below are copied | Preserve only in Git history. This removes the surrounding design and proof-planning corpus rather than carrying it into the reset. |
| `docs/plans/workflow-calibration.explorations/2026-08-13-audit-when-the-loop-turned.md` | Move byte-for-byte to `docs/audits/2026-08-13-audit-when-the-loop-turned.md` | Retain as audit evidence and link it from this charter. |
| `docs/plans/workflow-calibration.explorations/2026-08-13-audit-measurement-methods.md` | Move byte-for-byte to `docs/audits/2026-08-13-audit-measurement-methods.md` | Retain as audit evidence and link it from this charter. |
| `docs/metrics/workflow.jsonl` and the empty `docs/metrics/` directory | Delete from the working tree | Preserve only in Git history. No JSONL round log remains active or serves as proof. |
| `docs/plans/TEMPLATE*` | Replace through the simplified pack in delivery step 2 | Retain only as compact generated product output. It must not recreate the deleted plan, ledger, metrics, or review machinery. |
| `AGENTS.md`, `.agents/AGENTS.reference.md`, `.agents/prompts/`, `.agents/user-prompts/`, `.agents/principles.toml`, and `.agents/workflow.toml` | Replace through the simplified pack in delivery step 2 | Keep compact generated product guidance that implements the operating rules below. |
| `.agents/LEDGER.template.md` | Delete when delivery step 2 removes it from the pack manifest | Preserve only in Git history. The reset has no ledger template. |
| `.agents/checks.toml` and any `.agents/checks/` or `.agents/hooks/` product-development assets | Retain as product development configuration | They are checks or hooks, not task state. |
| `src/**`, `tests/**`, `pack/**`, `Cargo.toml`, `Cargo.lock`, `build.rs`, `flake.nix`, `flake.lock`, `justfile`, and `rustfmt.toml` | Retain as product | Change them only through the delivery steps. The pack is simplified in place, not discarded. |
| `README.md`, `CHANGELOG.md`, `LICENSE`, `.gitignore`, `.prettierrc.json`, `.envrc`, and `.vscode/**` | Retain as product, release, licence, or development material | Update user-facing product documentation only when a delivery step makes it stale. |
| Git commits, tags `v0.0.1` through `v0.0.4`, and release history | Retain unchanged | Cleanup is a new reversible commit sequence, never a history rewrite. |
| Branch `impl/bounded-convergence-option-b-proof` at `d02fa3c8741418d813d6eb442861242b7dba58c0` | Preserve unmerged and paused | Do not rebase, merge, delete, or treat it as active reset work. Its proof artefacts remain recoverable on that branch and in Git history. |

The audit and methods records remain easy to find because they have stable `docs/audits/` paths and this root charter names both paths. No surrounding planning directory is needed to interpret either record.

## Ordered delivery

### 1. Make `next` small and truthful

- **User problem:** `next` emits about 764 KB, copies the ledger verbatim, hides concurrent active work, and selects a stale lowest-order loop.
- **Change:** Add the bounded `.agents/work.toml` source and replace singular loop selection with an ordered `active_units` projection plus exactly one derived `selected_action`. Remove every ledger echo and free-form resume-state field from human and JSON output.
- **Acceptance test:** On this repository, both human and JSON invocations are at most 8,192 bytes, contain no verbatim ledger text, list every active unit exactly once, return exactly one correct selected action, and do not expose a stale singular-loop choice. Fixtures cover several simultaneous phases and a reordered first actionable unit. Two identical runs for each format are byte-identical.
- **Why it is next:** It removes the largest immediate user cost and gives later reset work a trustworthy, bounded control surface.

### 2. Make the default scaffold use the minimal workflow

- **User problem:** A newly scaffolded project inherits the ceremony that produced the deleted planning tree.
- **Change:** Simplify the pack and regenerate its committed copies so the default workflow uses this charter's operating rules, one small work file, one implementation branch, and no ledger, round log, plan-review loop, or review directory.
- **Acceptance test:** Scaffolding into an empty temporary repository creates no ledger template, JSONL log, `docs/plans/` process tree, or review directory. Its active workflow guidance stays within the limits below, a second scaffold run is byte-idempotent, and the existing product tests pass.
- **Why it is next:** Fixing only this repository would leave the product teaching every adopter the failed process.

### 3. Make validation check real state rather than review claims

- **User problem:** The current validator can certify self-authored round records without proving that an independent review occurred.
- **Change:** Make status and validation parse the bounded work file, enforce its closed statuses and limits, and treat review as an external human or platform event rather than a self-certified JSON proof record. Remove default dependencies on the deleted plan, ledger, and metrics log.
- **Acceptance test:** Validation succeeds in a clean scaffold with only the compact work state, rejects a sixth active step, duplicate selection, an unknown status, an unresolved blocker, and an oversized state file, and cannot be made green by appending a claimed review record. Human and JSON status output are deterministic and bounded.
- **Why it is next:** The simplified pack needs a mechanical boundary that checks useful invariants without recreating the old evidence theatre.

### 4. Establish a releasable product baseline

- **User problem:** Process changes have obscured whether the retained product can still install, scaffold, validate, and guide a user end to end.
- **Change:** Align README and changelog wording with the shipped minimal behaviour, remove only product code proven unreachable after steps 1 to 3, and prepare a local release candidate without publishing it.
- **Acceptance test:** The locked Nix toolchain runs formatting checks, Clippy with warnings denied, the full test suite, a local install, an empty-directory scaffold twice, validation, human `next`, and JSON `next`. The tree stays clean and no command requires the deleted process files.
- **Why it is next:** It turns the reset into a tested product baseline while leaving release and push authority with the human.

## Minimal operating rules

1. Keep at most five active delivery steps in `.agents/work.toml`. Use one active implementation branch, `impl/minimal-reset`, and no parallel implementation worktrees. The preserved proof branch is paused evidence, not active work.
2. For each product step, run one implementer pass and one independent product review of the code, tests, pack, and shipped user documentation. Planning prose receives one human approval and no agent review loop.
3. Run a separate triage only when the product review reports findings. Permit one scoped fix pass and at most one focused verification. If that verification fails, stop and return the unresolved result to the human rather than opening another loop.
4. Review findings may require a fix only within the step's existing acceptance test. They cannot add a step, broaden Success Criteria, or create process-generated scope. A new request waits for a later human decision.
5. A review record authored by the implementer, orchestrator, validator, or project itself is not proof of independent review. Use the independent reviewer's actual output or the hosting platform's review event. Never manufacture a file or JSON line to certify review.

## Hard size and cost limits

- `RESET.md` stays below 200 natural Markdown lines and at most 2,500 words. `.agents/work.toml` is at most 4 KiB and five active steps.
- Active task state, meaning `RESET.md` plus `.agents/work.toml`, is at most 24 KiB. Final generated workflow guidance, meaning `AGENTS.md` plus `.agents/` prompts, user prompts, principles, and workflow configuration, is at most 64 KiB. No individual prompt exceeds 4 KiB.
- Human `next` and `next --json` output are each at most 8 KiB. Human and JSON status or validation output are each at most 16 KiB. Commands fail non-zero rather than truncate, spill into another file, or print a hidden tail.
- A product step consumes at most five agent passes: implementation, product review, conditional triage, conditional fix, and conditional verification. Planning consumes one human approval and no reviewer or triager pass.
- When any limit would be exceeded, work stops before another file, step, review, or agent pass is created. Reduce the same scope by deletion or ask the human to revise it. Do not waive the limit, split around it, or generate a follow-up task.

## Salvage test

The salvage window starts when the cleanup migration lands and ends at the earlier of seven calendar days or completion of delivery step 4. A product commit must touch `src/`, `pack/`, `tests/`, `Cargo.toml`, `Cargo.lock`, or `build.rs`, pass its step acceptance test, and complete the independent product review above.

The repository passes only if all of these are true at the deadline:

- Three accepted product commits have landed, including the `next` repair, the minimal default scaffold, and real-state validation.
- `next` and all active process files meet their hard limits, all active work is visible, and no deleted ledger, JSONL log, mega-plan, or review directory has returned.
- The locked-toolchain formatting check, Clippy with warnings denied, full tests, local install, two-run scaffold, validation, and both `next` formats pass from a clean tree.
- No product step exceeded one product review, one conditional triage, one fix, or one verification, and no review generated new task scope.
- After the migration commits, no more than one process-only commit has landed and no status claims active work without the single implementation branch that carries it.

If any criterion fails, stop work in this repository. Create a local `archive/salvage-failed-<date>` ref at the failed tip, preserve all existing release tags and the proof branch, and make no further product or process commits here. Any continuation starts in a new repository from tag `v0.0.4` plus individually selected, passing product commits. Remote archival, creation of the new repository, pushes, publication, and releases still require explicit human action.

## Reversible migration

1. Record the approved `main` hash and the proof-branch hash, then create local branch `archive/pre-minimal-reset` at the approved `main` tip. Do not move the proof branch.
2. Move the two audit records to `docs/audits/` and commit the move before deleting their surrounding exploration tree.
3. Add the bounded `.agents/work.toml`, then delete the old active process families exactly as listed in the disposition table. Commit the cleanup separately so `git revert` can restore it without touching product history.
4. Use only `impl/minimal-reset` for delivery. Merge accepted product commits locally. Do not push, publish, release, force-update, or delete any preservation ref.

Every migration operation is represented by an ordinary commit or a new local ref. Reverting the commits and resetting from `archive/pre-minimal-reset` restores the pre-reset working tree.

## Human decision required

Choose exactly one option before any cleanup or product work begins.

| Option | Trade-offs |
| --- | --- |
| **Approve reset** | Preserves product and history, removes the failed active process, and tests salvage quickly. It accepts targeted compatibility changes to the scaffolded workflow and a strict stop if delivery does not recover. |
| **Revise charter** | Corrects a disposition, limit, step, or pass criterion before deletion. It delays the evidence window and risks another prose cycle, so revisions should be specific and approved once. |
| **Choose a new repository now** | Gives the cleanest process boundary and avoids changing this repository in place. It splits continuity, requires deliberate code and release-history transfer, and leaves the current product archived sooner. |
| **Archive now** | Stops further cost and preserves the released project and evidence exactly as they stand. It delivers no `next` repair, no minimal scaffold, and no salvage measurement. |

**Recommendation: Approve reset.** It follows **Prefer the cleaner long-term architecture over the smallest diff** by removing contradictory active state rather than patching the mega-plan. It follows **Minimal by default** through five-step, file-size, output, and review-cost caps. It follows **Safe on existing projects** through audit copies, preservation refs, ordinary commits, and no product rewrite. It follows **Idempotent** through deterministic output and a two-run scaffold test. It follows **Make illegal states unrepresentable** through a closed, bounded work file and one derived selected action. It follows **Ground decisions in evidence** through the 13 August audit and the timed salvage test. It follows **Reproducible** through the locked Nix toolchain and executable acceptance checks. It follows **Structured data first, project for humans** through one small typed work source and bounded human and JSON projections rather than prose ledgers and self-certified event logs.

Approval authorises only the reversible migration and the four delivery steps in this charter. It grants no push, publication, release, remote archive, or new-repository authority.
