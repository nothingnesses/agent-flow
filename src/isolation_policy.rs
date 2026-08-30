//! Legacy isolation-policy prose emitted by plan-based `next` and available to
//! custom packs through `{{isolation_policy}}`. The minimal built-in pack uses one
//! implementation branch and does not render this worktree-oriented fragment.

/// The canonical isolation policy prose: the standing directive that every spawned
/// agent runs isolated (the writers and the read-only reviewers, triager, and
/// explorers alike, referencing the tier order in `AGENTS.md`, not restating it),
/// because even a findings or exploration file is a write, DISTINCT from the
/// orchestrator's own integration-level edits on main (step-status flips, increment
/// declarations, round records, ledger anchors), which author no reviewed product
/// content.
///
/// A `&'static str` because the compatibility policy takes no computed input.
pub(crate) const ISOLATION_POLICY_FRAGMENT: &str = "Who isolates is settled here once and rendered from this single source, so the copies of this rule cannot drift: every spawned agent runs in the strongest isolation the harness supports, per the capability-tiered tier order in the Writer isolation rule, and the orchestrator integrates its output onto main. This holds for the writers (the planner and the implementer) and for the read-only reviewers, triager, and explorers alike, because even a findings or an exploration file is a write: isolating every spawned agent keeps main pristine until the orchestrator integrates, so a killed or misbehaving agent never touches main. The only edits made directly on main are the orchestrator's own integration-level ones, which author no reviewed product content and so stay the orchestrator's direct job rather than a spawned agent's: flipping a step's status, declaring an increment, recording a round record, and moving the ledger's resume anchor.";

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn the_fragment_states_the_uniform_isolation_rule() {
		// The fragment must carry the uniform-isolation rule: every spawned agent
		// runs isolated (the read-only reviewers, triager, and explorers included,
		// because even a findings or exploration file is a write), DISTINCT from the
		// orchestrator's own integration-level edits on main. A reword of the policy
		// fails here directly, so the fragment's content is pinned independent of the
		// scaffold output.
		assert!(
			ISOLATION_POLICY_FRAGMENT
				.contains("every spawned agent runs in the strongest isolation"),
			"the isolation policy must state that every spawned agent runs isolated"
		);
		assert!(
			ISOLATION_POLICY_FRAGMENT.contains("even a findings or an exploration file is a write"),
			"the isolation policy must justify isolating the read-only reviewers, triager, and explorers"
		);
		assert!(
			ISOLATION_POLICY_FRAGMENT.contains("the orchestrator's own integration-level ones"),
			"the isolation policy must distinguish spawned-agent work from the orchestrator's integration edits"
		);
	}
}
