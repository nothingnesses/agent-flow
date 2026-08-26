# Convergence investigation fold brief

Act only as planner in the isolated plan worktree. Read AGENTS.md, `workflow-calibration`, the current convergence and acceptance rules, the metrics log, the Q-78 acceptance records, and these sources:

- `https://kevinmahoney.co.uk/articles/ai-review-loops/`.
- `https://gist.github.com/KMahoney/3098f0f12638d0a83a5ef3b91bef601d`.
- `https://lobste.rs/s/52povq/ai_review_loops_don_t_always_stabilise`.

Record Q-85 as decided and folded into `workflow-calibration`, with this exact decision receipt.

Options:

- `Add a design pass to workflow-calibration`.
- `Create a standalone convergence redesign step`.
- `Implement a hard task-level cap now`.

Recommendation and chosen: `Add a design pass to workflow-calibration`.

Register Q-86 as `exploring`, the open mechanism question. Point it at a tracked convergence-mechanism design brief under `docs/plans/workflow-calibration.explorations/`. The later explorers will author separate proposals there. Do not decide the mechanism in this fold.

Update `workflow-calibration` so the design pass examines at least:

- The current five-round per-artifact cap and its reset-after-human-resume branch.
- The uncapped sequence of later acceptance passes.
- A non-resettable task-level review budget and phase-specific sub-budgets.
- Novelty, severity and finding-lineage rules: pre-existing, fix-induced, scope-expanded and relitigated.
- A fixed acceptance rubric and scope firewall that routes optional new obligations to backlog.
- Terminal human choices at budget exhaustion: accept residual risk, narrow scope, revert, replan or abandon.
- A rule that no budget can conceal an unresolved critical finding.
- Blind versus informed reviewer allocation and the article's anchoring result.
- The existing sequential/survival and severity-trajectory ideas already in `workflow-calibration`.

Ground the investigation in reproducible local evidence. The six recorded Q-78 acceptance passes produced 7, 10, 5, 6, 5 and 5 valid shortfalls. Cite the metrics selector rather than treating that list as permanent. Ground the external input accurately: the article's experiment reported 10, 12 and 17 defects, fix-induced defects, growing review scope, oscillating trade-offs, and a machine-checkable core that converged while contract/prose obligations did not.

Require the design pass to return viable mechanisms, trade-offs against the eight Project Principles, a recommendation, a migration and enforcement plan, falsifiable stopping properties, and a YAGNI boundary. Require a later human decision before implementation. Do not change the current cap, acceptance rule, reset behaviour or code now.

Correct the `workflow-calibration` sidecar's stale status wording against the TOML while preserving completed historical records. Add the minimum Success Criterion needed to verify that Q-85/Q-86 and the tracked brief are scheduled. Do not change any Roadmap status, edit pack/code, close Q-58/Q-78/Q-86, or alter existing review identities.

Render and run both validations, strict render, tests, Clippy, checks, diff and ASCII checks. Commit with a docs subject. Do not push.
