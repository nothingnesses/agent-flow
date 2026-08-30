//! Legacy human-input-contract prose available to custom packs through
//! `{{recommendation_rule}}`. The minimal built-in pack states its compact
//! ask-and-recommend rule directly and does not render this plan-oriented fragment.

/// The canonical recommendation-rule prose: the standing directive that the
/// human-input contract presents every decision the orchestrator puts to the
/// human the same way (the viable options or approaches, the trade-offs of each,
/// a recommendation, and the reasoning, with the reasoning judged against the
/// plan's Project Principles BY NAME), settled once and rendered from this
/// single source so its copies cannot drift.
///
/// A `&'static str` because the compatibility rule takes no computed input.
pub(crate) const RECOMMENDATION_RULE_FRAGMENT: &str = "The human-input contract's presentation format is settled once and rendered from this single source, so its copies cannot drift: wherever the orchestrator puts a decision to the human, it presents that decision the same way, as the viable options or approaches, the trade-offs of each, a recommendation, and the reasoning, with the reasoning judged against the plan's Project Principles by name.";

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn the_fragment_states_the_recommendation_rule() {
		// The fragment must carry the recommendation-in-options rule: it is the single
		// source of the human-input contract's presentation format, it presents the
		// options with their trade-offs, a recommendation, and the reasoning, and it
		// judges that reasoning against the plan's Project Principles BY NAME. A reword
		// of the rule fails here directly, so the fragment's content is pinned
		// independent of the scaffold output.
		assert!(
			RECOMMENDATION_RULE_FRAGMENT
				.contains("settled once and rendered from this single source"),
			"the recommendation rule must state it is the single canonical source"
		);
		assert!(
			RECOMMENDATION_RULE_FRAGMENT
				.contains("the trade-offs of each, a recommendation, and the reasoning"),
			"the recommendation rule must require the options, their trade-offs, a recommendation, and the reasoning"
		);
		assert!(
			RECOMMENDATION_RULE_FRAGMENT.contains("judged against the plan's Project Principles by name"),
			"the recommendation rule must judge the reasoning against the plan's Project Principles by name"
		);
	}
}
