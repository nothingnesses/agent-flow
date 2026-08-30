//! Legacy findings-path templates used by plan-based `next` and available to
//! custom packs through `{{findings_naming}}`. The minimal built-in pack emits no
//! findings directory or naming guidance.

/// The findings-files directory, a named-token template. `<task>` is filled by the
/// driver builders; the convention sentence names the directory in the hand-authored
/// prose that precedes the `{{findings_naming}}` slot, so it is not rendered here.
const DIR_TEMPLATE: &str = "docs/plans/<task>.reviews";

/// A reviewer's findings-file basename, a named-token template. `<role>` resolves to
/// the literal `reviewer` for a reviewer's file; `<step>` is filled by the driver;
/// `<disambiguator>` is left as a literal token for the orchestrator to assign, so no
/// two parallel reviewers collide.
const REVIEWER_BASENAME: &str = "<step>-<role>-<disambiguator>.md";

/// The triager's findings-file basename, a named-token template.
const TRIAGE_BASENAME: &str = "<step>-triage.md";

/// The backstop re-check triager's findings-file basename, a named-token template.
/// The driver has no re-check state and never produces this path; the convention
/// names it for the human, so it appears only in `convention_fragment()`.
const TRIAGE_RECHECK_BASENAME: &str = "<step>-triage-recheck.md";

/// Fill `<task>` in the directory template and join the given basename onto it,
/// producing a findings-file path from the single-source templates. Named-token
/// substitution (not `format!`) because `format!` cannot leave a named argument
/// unfilled, and the builders must leave `<disambiguator>` (and, for the convention,
/// every token) in place.
fn join_dir(
	task: &str,
	basename: &str,
) -> String {
	let dir = DIR_TEMPLATE.replace("<task>", task);
	format!("{dir}/{basename}")
}

/// The reviewer findings-file path the `next` driver emits: `<task>` and `<step>`
/// filled, `<role>` set to the literal `reviewer`, `<disambiguator>` left as its
/// template token for the orchestrator to assign. Reproduces exactly the string the
/// driver formatted by hand before this module existed.
pub(crate) fn review_findings_path(
	task: &str,
	step: &str,
) -> String {
	let basename = REVIEWER_BASENAME.replace("<step>", step).replace("<role>", "reviewer");
	join_dir(task, &basename)
}

/// The triager findings-file path the `next` driver emits: `<task>` and `<step>`
/// filled. Reproduces exactly the string the driver formatted by hand before this
/// module existed.
pub(crate) fn triage_findings_path(
	task: &str,
	step: &str,
) -> String {
	let basename = TRIAGE_BASENAME.replace("<step>", step);
	join_dir(task, &basename)
}

/// Render the legacy convention from the same templates the plan-based driver
/// fills. Custom packs may consume it; the minimal built-in pack does not.
pub(crate) fn convention_fragment() -> String {
	format!(
		"The filenames follow one convention so parallel writers never collide: a reviewer's file is `{REVIEWER_BASENAME}`, where the orchestrator assigns each spawned reviewer a distinct disambiguator (its model, or an index); the triager's is `{TRIAGE_BASENAME}`; and the backstop re-check triager's is `{TRIAGE_RECHECK_BASENAME}`."
	)
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn the_fragment_states_the_naming_convention() {
		// The fragment must carry the naming convention: the collision-avoidance
		// rationale, the reviewer/triage/recheck filename shapes with their tokens
		// unfilled, and the disambiguator-assignment prose. A reword fails here
		// directly, so the fragment's content is pinned independent of the scaffold
		// output.
		let fragment = convention_fragment();
		assert!(
			fragment.contains("parallel writers never collide"),
			"the convention must state the filenames avoid parallel-writer collisions"
		);
		assert!(
			fragment.contains("`<step>-<role>-<disambiguator>.md`"),
			"the convention must name the reviewer filename shape with tokens unfilled"
		);
		assert!(
			fragment.contains(
				"the orchestrator assigns each spawned reviewer a distinct disambiguator (its model, or an index)"
			),
			"the convention must explain how the disambiguator is assigned"
		);
		assert!(
			fragment.contains("`<step>-triage.md`"),
			"the convention must name the triager filename shape"
		);
		assert!(
			fragment.contains("`<step>-triage-recheck.md`"),
			"the convention must name the backstop re-check filename shape"
		);
	}

	#[test]
	fn the_builders_fill_tokens_as_the_driver_expects() {
		// The driver builders must reproduce the exact strings the `next` driver
		// formatted by hand: `<task>`/`<step>` filled, `<role>` set to `reviewer`,
		// `<disambiguator>` left as its literal token. This pins the byte-for-byte
		// equivalence the driver's golden fixtures also assert.
		assert_eq!(
			review_findings_path("demo", "core-assets"),
			"docs/plans/demo.reviews/core-assets-reviewer-<disambiguator>.md"
		);
		assert_eq!(
			triage_findings_path("demo", "core-assets"),
			"docs/plans/demo.reviews/core-assets-triage.md"
		);
	}
}
