//! Typed state for the bounded `.agents/work.toml` workflow.

use {
	serde::{
		Deserialize,
		Serialize,
	},
	std::collections::BTreeMap,
};

const WORK_FILE_VERSION: u64 = 1;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Deserialize, Serialize)]
#[serde(rename_all = "kebab-case")]
pub(crate) enum WorkStatus {
	Active,
	Pending,
	Complete,
}

impl WorkStatus {
	pub(crate) fn label(self) -> &'static str {
		match self {
			Self::Active => "active",
			Self::Pending => "pending",
			Self::Complete => "complete",
		}
	}
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub(crate) struct WorkFile {
	pub(crate) version: u64,
	pub(crate) selected_action: String,
	#[serde(rename = "step")]
	pub(crate) steps: Vec<WorkStep>,
}

#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub(crate) struct WorkStep {
	pub(crate) id: String,
	pub(crate) status: WorkStatus,
	pub(crate) blocked_by: Vec<String>,
	pub(crate) user_problem: String,
	pub(crate) change: String,
	pub(crate) acceptance: Vec<String>,
	pub(crate) why_next: String,
}

impl WorkFile {
	pub(crate) fn selected_step(&self) -> &WorkStep {
		self.steps
			.iter()
			.find(|step| step.id == self.selected_action)
			.expect("validated work file has a selected step")
	}
}

#[derive(Debug)]
pub(crate) enum ParseError {
	Toml(toml::de::Error),
	UnsupportedVersion(u64),
	DuplicateStepId { id: String, first: usize, duplicate: usize },
	UnsafeText { step: Option<usize>, field: &'static str, item: Option<usize>, character: char },
	SelectedActionNotFound(String),
	SelectedActionNotActive { id: String, status: WorkStatus },
}

impl std::fmt::Display for ParseError {
	fn fmt(
		&self,
		f: &mut std::fmt::Formatter<'_>,
	) -> std::fmt::Result {
		match self {
			Self::Toml(error) => write!(f, "malformed work file: {error}"),
			Self::UnsupportedVersion(version) =>
				write!(f, "unsupported work file version {version}; expected {WORK_FILE_VERSION}"),
			Self::DuplicateStepId {
				id,
				first,
				duplicate,
			} => write!(f, "duplicate step id `{id}` at steps {first} and {duplicate}"),
			Self::UnsafeText {
				step,
				field,
				item,
				character,
			} => {
				let location = match (step, item) {
					(Some(step), Some(item)) => format!("step {step} field `{field}` item {item}"),
					(Some(step), None) => format!("step {step} field `{field}`"),
					(None, Some(item)) => format!("work file field `{field}` item {item}"),
					(None, None) => format!("work file field `{field}`"),
				};
				write!(f, "{location} contains control character U+{:04X}", u32::from(*character))
			}
			Self::SelectedActionNotFound(id) => {
				write!(f, "selected_action `{id}` does not match any step id")
			}
			Self::SelectedActionNotActive {
				id,
				status,
			} => write!(
				f,
				"selected_action `{id}` has status `{}`; expected `active`",
				status.label()
			),
		}
	}
}

impl std::error::Error for ParseError {
	fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
		match self {
			Self::Toml(error) => Some(error),
			_ => None,
		}
	}
}

fn reject_control_characters(
	value: &str,
	step: Option<usize>,
	field: &'static str,
	item: Option<usize>,
) -> Result<(), ParseError> {
	if let Some(character) = value.chars().find(|character| character.is_control()) {
		return Err(ParseError::UnsafeText {
			step,
			field,
			item,
			character,
		});
	}
	Ok(())
}

pub(crate) fn parse(source: &str) -> Result<WorkFile, ParseError> {
	let work: WorkFile = toml::from_str(source).map_err(ParseError::Toml)?;
	if work.version != WORK_FILE_VERSION {
		return Err(ParseError::UnsupportedVersion(work.version));
	}

	reject_control_characters(&work.selected_action, None, "selected_action", None)?;

	let mut positions = BTreeMap::new();
	for (index, step) in work.steps.iter().enumerate() {
		let position = index + 1;
		reject_control_characters(&step.id, Some(position), "id", None)?;
		for (item, blocker) in step.blocked_by.iter().enumerate() {
			reject_control_characters(blocker, Some(position), "blocked_by", Some(item + 1))?;
		}
		reject_control_characters(&step.user_problem, Some(position), "user_problem", None)?;
		reject_control_characters(&step.change, Some(position), "change", None)?;
		for (item, criterion) in step.acceptance.iter().enumerate() {
			reject_control_characters(criterion, Some(position), "acceptance", Some(item + 1))?;
		}
		reject_control_characters(&step.why_next, Some(position), "why_next", None)?;

		if let Some(first) = positions.insert(step.id.as_str(), position) {
			return Err(ParseError::DuplicateStepId {
				id: step.id.clone(),
				first,
				duplicate: position,
			});
		}
	}

	let selected = work
		.steps
		.iter()
		.find(|step| step.id == work.selected_action)
		.ok_or_else(|| ParseError::SelectedActionNotFound(work.selected_action.clone()))?;
	if selected.status != WorkStatus::Active {
		return Err(ParseError::SelectedActionNotActive {
			id: selected.id.clone(),
			status: selected.status,
		});
	}
	Ok(work)
}

#[cfg(test)]
mod tests {
	use super::*;

	fn source(selected_action: Option<&str>) -> String {
		let selected =
			selected_action.map(|id| format!("selected_action = \"{id}\"\n")).unwrap_or_default();
		format!(
			"version = 1\n{selected}\n\
			 [[step]]\n\
			 id = \"alpha\"\n\
			 status = \"active\"\n\
			 blocked_by = []\n\
			 user_problem = \"Alpha problem\"\n\
			 change = \"Alpha change\"\n\
			 acceptance = [\"Alpha acceptance\"]\n\
			 why_next = \"Alpha why\"\n\n\
			 [[step]]\n\
			 id = \"beta\"\n\
			 status = \"pending\"\n\
			 blocked_by = [\"alpha\"]\n\
			 user_problem = \"Beta problem\"\n\
			 change = \"Beta change\"\n\
			 acceptance = [\"Beta acceptance one\", \"Beta acceptance two\"]\n\
			 why_next = \"Beta why\"\n"
		)
	}

	#[test]
	fn parser_preserves_step_order_and_action_fields() {
		let work = parse(&source(Some("alpha"))).unwrap();
		assert_eq!(work.version, 1);
		assert_eq!(work.selected_action, "alpha");
		assert_eq!(
			work.steps.iter().map(|step| step.id.as_str()).collect::<Vec<_>>(),
			["alpha", "beta"]
		);
		assert_eq!(work.steps[1].status, WorkStatus::Pending);
		assert_eq!(work.steps[1].blocked_by, ["alpha"]);
		assert_eq!(work.steps[1].user_problem, "Beta problem");
		assert_eq!(work.steps[1].change, "Beta change");
		assert_eq!(work.steps[1].acceptance, ["Beta acceptance one", "Beta acceptance two"]);
		assert_eq!(work.steps[1].why_next, "Beta why");
	}

	#[test]
	fn projection_text_rejects_control_characters_with_field_locations() {
		let cases = [
			(
				"selected action",
				"selected_action = \"alpha\"",
				"selected_action = \"alpha\\nspoof\"",
				"work file field `selected_action` contains control character U+000A",
			),
			(
				"step id",
				"id = \"alpha\"",
				"id = \"alpha\\rspoof\"",
				"step 1 field `id` contains control character U+000D",
			),
			(
				"blocker id",
				"blocked_by = [\"alpha\"]",
				"blocked_by = [\"alpha\\tspoof\"]",
				"step 2 field `blocked_by` item 1 contains control character U+0009",
			),
			(
				"user problem",
				"user_problem = \"Alpha problem\"",
				"user_problem = \"Alpha\\nspoof\"",
				"step 1 field `user_problem` contains control character U+000A",
			),
			(
				"change",
				"change = \"Alpha change\"",
				"change = \"Alpha\\rspoof\"",
				"step 1 field `change` contains control character U+000D",
			),
			(
				"acceptance item",
				"acceptance = [\"Beta acceptance one\", \"Beta acceptance two\"]",
				"acceptance = [\"Beta acceptance one\", \"Beta\\tacceptance\"]",
				"step 2 field `acceptance` item 2 contains control character U+0009",
			),
			(
				"why next",
				"why_next = \"Beta why\"",
				"why_next = \"Beta\\nspoof\"",
				"step 2 field `why_next` contains control character U+000A",
			),
		];

		for (name, before, after, expected) in cases {
			let input = source(Some("alpha")).replace(before, after);
			let error = parse(&input).unwrap_err().to_string();
			assert_eq!(error, expected, "{name}");
		}
	}

	#[test]
	fn printable_ascii_and_unicode_projection_text_is_preserved() {
		let input = source(Some("alpha")).replace(
			"user_problem = \"Alpha problem\"",
			"user_problem = \"ASCII !~; crème brûlée; 東京; 🚀\"",
		);
		let work = parse(&input).unwrap();
		assert_eq!(work.steps[0].user_problem, "ASCII !~; crème brûlée; 東京; 🚀");
	}

	#[test]
	fn duplicate_ids_are_rejected() {
		let input = source(Some("alpha")).replace("id = \"beta\"", "id = \"alpha\"");
		let error = parse(&input).unwrap_err().to_string();
		assert_eq!(error, "duplicate step id `alpha` at steps 1 and 2");
	}

	#[test]
	fn an_absent_selected_action_is_rejected() {
		let error = parse(&source(None)).unwrap_err().to_string();
		assert!(error.contains("missing field `selected_action`"), "{error}");
	}

	#[test]
	fn a_selected_non_active_step_is_rejected() {
		let error = parse(&source(Some("beta"))).unwrap_err().to_string();
		assert_eq!(error, "selected_action `beta` has status `pending`; expected `active`");
	}

	#[test]
	fn an_unknown_selected_action_is_rejected() {
		let error = parse(&source(Some("missing"))).unwrap_err().to_string();
		assert_eq!(error, "selected_action `missing` does not match any step id");
	}
}
