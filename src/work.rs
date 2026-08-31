//! Typed state for the bounded `.agents/work.toml` workflow.

use {
	serde::{
		Deserialize,
		Serialize,
	},
	std::{
		collections::BTreeMap,
		fs::File,
		io::{
			self,
			Read,
		},
		path::Path,
	},
};

const WORK_FILE_VERSION: u64 = 1;
pub(crate) const MAX_SOURCE_BYTES: usize = 4_096;
pub(crate) const MAX_STEPS: usize = 5;
pub(crate) const MAX_STATUS_OUTPUT_BYTES: usize = 16_384;

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
	pub(crate) selected_action: Option<String>,
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
	pub(crate) fn selected_step(&self) -> Option<&WorkStep> {
		self.selected_action.as_ref().map(|selected_action| {
			self.steps
				.iter()
				.find(|step| step.id == *selected_action)
				.expect("validated nonterminal work file has a selected step")
		})
	}

	/// A step's declared predecessors paired with their statuses, in declaration order.
	/// Single-sourced here so `status` and `next` describe one dependency the same way:
	/// parsing already proved every blocker names a step, so a status is always available
	/// and neither projection has to invent a word for a missing one.
	pub(crate) fn dependencies(
		&self,
		step: &WorkStep,
	) -> Vec<Dependency> {
		step.blocked_by
			.iter()
			.map(|id| Dependency {
				id: id.clone(),
				status: self
					.steps
					.iter()
					.find(|candidate| candidate.id == *id)
					.expect("validated blocker names a step")
					.status,
			})
			.collect()
	}
}

#[derive(Debug)]
pub(crate) enum ParseError {
	SourceTooLarge(usize),
	Toml(toml::de::Error),
	UnsupportedVersion(u64),
	TooManySteps(usize),
	DuplicateStepId { id: String, first: usize, duplicate: usize },
	UnsafeText { step: Option<usize>, field: &'static str, item: Option<usize>, character: char },
	UnknownBlocker { step: usize, id: String, blocker: String },
	ActiveBlockerNotComplete { id: String, blocker: String, status: WorkStatus },
	PendingBlockerIsSelf { step: usize, id: String },
	PendingBlockerNotEarlier { step: usize, id: String, blocker: String, blocker_step: usize },
	PendingBlockerComplete { step: usize, id: String, blocker: String },
	SelectedActionNotFound(String),
	SelectedActionNotActive { id: String, status: WorkStatus },
	SelectedActionMissingWithUnfinishedWork { active: usize, pending: usize },
}

impl std::fmt::Display for ParseError {
	fn fmt(
		&self,
		f: &mut std::fmt::Formatter<'_>,
	) -> std::fmt::Result {
		match self {
			Self::SourceTooLarge(bytes) => write!(
				f,
				"work source is {bytes} bytes; the limit is {MAX_SOURCE_BYTES} bytes"
			),
			Self::Toml(error) => write!(f, "malformed work file: {error}"),
			Self::UnsupportedVersion(version) =>
				write!(f, "unsupported work file version {version}; expected {WORK_FILE_VERSION}"),
			Self::TooManySteps(steps) => {
				write!(f, "work source has {steps} steps; the limit is {MAX_STEPS} steps")
			}
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
				write!(
					f,
					"{location} contains {} U+{:04X}",
					unsafe_character_kind(*character),
					u32::from(*character)
				)
			}
			Self::UnknownBlocker {
				step,
				id,
				blocker,
			} => write!(f, "step {step} `{id}` declares unknown blocker `{blocker}`"),
			Self::ActiveBlockerNotComplete {
				id,
				blocker,
				status,
			} => write!(
				f,
				"active step `{id}` depends on `{blocker}` with status `{}`; active-step blockers must be complete",
				status.label()
			),
			Self::PendingBlockerIsSelf {
				step,
				id,
			} => write!(f, "pending step {step} `{id}` declares itself as a blocker"),
			Self::PendingBlockerNotEarlier {
				step,
				id,
				blocker,
				blocker_step,
			} => write!(
				f,
				"pending step {step} `{id}` declares blocker `{blocker}` at step {blocker_step}; pending-step blockers must be earlier steps"
			),
			Self::PendingBlockerComplete {
				step,
				id,
				blocker,
			} => write!(
				f,
				"pending step {step} `{id}` depends on `{blocker}` with status `complete`; pending-step blockers must be active or pending"
			),
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
			Self::SelectedActionMissingWithUnfinishedWork {
				active,
				pending,
			} => write!(
				f,
				"selected_action is required while work remains; found {active} active and {pending} pending steps"
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

/// Whether a character is unsafe in ANY work-file value. Two families: the control
/// characters (which include the C1 block, so U+0085 NEXT LINE is here rather than
/// spelled out), and the two Unicode separators a consumer may render as a line break.
/// U+2028 and U+2029 are not control characters, so `char::is_control` alone would let
/// them through into text that is about to be printed as lines.
///
/// This is the whole unsafe set. The two callers below differ in ONE character: prose
/// exempts the line feed, and nothing else.
fn is_unsafe_character(character: char) -> bool {
	character.is_control() || matches!(character, '\u{2028}' | '\u{2029}')
}

/// What to call an unsafe character in a diagnostic. The separators get their own words
/// because calling U+2028 a control character would send a reader looking for something
/// that is not there.
fn unsafe_character_kind(character: char) -> &'static str {
	match character {
		'\u{2028}' => "line separator",
		'\u{2029}' => "paragraph separator",
		_ => "control character",
	}
}

/// A STRUCTURAL value: `selected_action`, a step `id`, a blocker id. These name things
/// and are printed inline inside composed lines (`- {id} [{status}; ...]`), so a line
/// break anywhere in one forges output. Every unsafe character is rejected, the line
/// feed included.
fn reject_structural_text(
	value: &str,
	step: Option<usize>,
	field: &'static str,
	item: Option<usize>,
) -> Result<(), ParseError> {
	reject_unsafe_text(value, step, field, item, is_unsafe_character)
}

/// A PROSE value: `user_problem`, `change`, an `acceptance` item, `why_next`. A step
/// cannot state its problem honestly on one line, so these carry paragraphs: the line
/// feed is accepted, and the renderer indents every continuation line behind a gutter
/// (`next::PROSE_CONTINUATION`) so a paragraph break cannot become a top-level output
/// line. Every OTHER unsafe character stays rejected, including the tab and the carriage
/// return, which a terminal can move the cursor with, and the two Unicode separators,
/// which some consumers break lines on.
fn reject_prose_text(
	value: &str,
	step: Option<usize>,
	field: &'static str,
	item: Option<usize>,
) -> Result<(), ParseError> {
	reject_unsafe_text(value, step, field, item, |character| {
		character != '\n' && is_unsafe_character(character)
	})
}

fn reject_unsafe_text(
	value: &str,
	step: Option<usize>,
	field: &'static str,
	item: Option<usize>,
	is_unsafe: impl Fn(char) -> bool,
) -> Result<(), ParseError> {
	if let Some(character) = value.chars().find(|character| is_unsafe(*character)) {
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
	if source.len() > MAX_SOURCE_BYTES {
		return Err(ParseError::SourceTooLarge(source.len()));
	}
	let work: WorkFile = toml::from_str(source).map_err(ParseError::Toml)?;
	if work.version != WORK_FILE_VERSION {
		return Err(ParseError::UnsupportedVersion(work.version));
	}
	if work.steps.len() > MAX_STEPS {
		return Err(ParseError::TooManySteps(work.steps.len()));
	}

	if let Some(selected_action) = &work.selected_action {
		reject_structural_text(selected_action, None, "selected_action", None)?;
	}

	let mut positions = BTreeMap::new();
	for (index, step) in work.steps.iter().enumerate() {
		let position = index + 1;
		// Structural first, then prose: the split is per FIELD, not per file, so one
		// weakened predicate can never let a line break into an id.
		reject_structural_text(&step.id, Some(position), "id", None)?;
		for (item, blocker) in step.blocked_by.iter().enumerate() {
			reject_structural_text(blocker, Some(position), "blocked_by", Some(item + 1))?;
		}
		reject_prose_text(&step.user_problem, Some(position), "user_problem", None)?;
		reject_prose_text(&step.change, Some(position), "change", None)?;
		for (item, criterion) in step.acceptance.iter().enumerate() {
			reject_prose_text(criterion, Some(position), "acceptance", Some(item + 1))?;
		}
		reject_prose_text(&step.why_next, Some(position), "why_next", None)?;

		if let Some(first) = positions.insert(step.id.as_str(), position) {
			return Err(ParseError::DuplicateStepId {
				id: step.id.clone(),
				first,
				duplicate: position,
			});
		}
	}

	// The dependency rules, read against the SAME declaration order the file lists and the
	// projections print. An active step is already unblocked, so its predecessors must all
	// be complete. A pending step is waiting on work that is still owed, so each of its
	// predecessors must be an EARLIER step that is still active or pending: a self, later,
	// or already-complete predecessor describes no wait at all. Complete steps carry no
	// ordering rule (their history is settled), and neither active nor complete steps gain
	// one here.
	for (index, step) in work.steps.iter().enumerate() {
		let position = index + 1;
		for blocker in &step.blocked_by {
			let blocker_position =
				*positions.get(blocker.as_str()).ok_or_else(|| ParseError::UnknownBlocker {
					step: position,
					id: step.id.clone(),
					blocker: blocker.clone(),
				})?;
			let blocker_status = work.steps[blocker_position - 1].status;
			match step.status {
				WorkStatus::Active if blocker_status != WorkStatus::Complete => {
					return Err(ParseError::ActiveBlockerNotComplete {
						id: step.id.clone(),
						blocker: blocker.clone(),
						status: blocker_status,
					});
				}
				WorkStatus::Pending => {
					if blocker_position == position {
						return Err(ParseError::PendingBlockerIsSelf {
							step: position,
							id: step.id.clone(),
						});
					}
					if blocker_position > position {
						return Err(ParseError::PendingBlockerNotEarlier {
							step: position,
							id: step.id.clone(),
							blocker: blocker.clone(),
							blocker_step: blocker_position,
						});
					}
					if blocker_status == WorkStatus::Complete {
						return Err(ParseError::PendingBlockerComplete {
							step: position,
							id: step.id.clone(),
							blocker: blocker.clone(),
						});
					}
				}
				WorkStatus::Active | WorkStatus::Complete => {}
			}
		}
	}

	if let Some(selected_action) = &work.selected_action {
		let selected = work
			.steps
			.iter()
			.find(|step| step.id == *selected_action)
			.ok_or_else(|| ParseError::SelectedActionNotFound(selected_action.clone()))?;
		if selected.status != WorkStatus::Active {
			return Err(ParseError::SelectedActionNotActive {
				id: selected.id.clone(),
				status: selected.status,
			});
		}
	} else {
		let active = work.steps.iter().filter(|step| step.status == WorkStatus::Active).count();
		let pending = work.steps.iter().filter(|step| step.status == WorkStatus::Pending).count();
		if active != 0 || pending != 0 {
			return Err(ParseError::SelectedActionMissingWithUnfinishedWork {
				active,
				pending,
			});
		}
	}
	Ok(work)
}

#[derive(Debug)]
pub(crate) enum LoadError {
	Read(io::Error),
	NotUtf8(std::str::Utf8Error),
	Invalid(ParseError),
}

impl std::fmt::Display for LoadError {
	fn fmt(
		&self,
		f: &mut std::fmt::Formatter<'_>,
	) -> std::fmt::Result {
		match self {
			Self::Read(error) => write!(f, "could not read work source: {error}"),
			Self::NotUtf8(error) => write!(f, "work source is not UTF-8: {error}"),
			Self::Invalid(error) => error.fmt(f),
		}
	}
}

impl std::error::Error for LoadError {
	fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
		match self {
			Self::Read(error) => Some(error),
			Self::NotUtf8(error) => Some(error),
			Self::Invalid(error) => Some(error),
		}
	}
}

/// A source path whose printable label carries a control character. It holds only the
/// offending character: the whole point is that the path itself is never echoed back.
#[derive(Debug, PartialEq, Eq)]
pub(crate) struct UnsafeSourceLabel {
	pub(crate) character: char,
}

impl std::fmt::Display for UnsafeSourceLabel {
	fn fmt(
		&self,
		f: &mut std::fmt::Formatter<'_>,
	) -> std::fmt::Result {
		write!(
			f,
			"work source path contains control character U+{:04X}; refusing to read it or echo it back",
			u32::from(self.character)
		)
	}
}

impl std::error::Error for UnsafeSourceLabel {}

/// The label `validate` and `status` print beside the state they loaded, or a refusal.
/// Both commands echo the path they read, so a path carrying a newline could forge a line
/// of otherwise trustworthy output; the same reason the parser refuses control characters
/// in the file's own text. Checked BEFORE the read, and the refusal names the character
/// rather than the path, so neither the raw path nor the forged line reaches a stream.
pub(crate) fn source_label(path: &Path) -> Result<String, UnsafeSourceLabel> {
	let label = path.display().to_string();
	match label.chars().find(|character| character.is_control()) {
		Some(character) => Err(UnsafeSourceLabel {
			character,
		}),
		None => Ok(label),
	}
}

/// Read and parse the bounded source through one shared typed boundary.
pub(crate) fn load(path: &Path) -> Result<WorkFile, LoadError> {
	let file = File::open(path).map_err(LoadError::Read)?;
	let file_bytes = file.metadata().map_err(LoadError::Read)?.len();
	if file_bytes > MAX_SOURCE_BYTES as u64 {
		let file_bytes = usize::try_from(file_bytes).unwrap_or(usize::MAX);
		return Err(LoadError::Invalid(ParseError::SourceTooLarge(file_bytes)));
	}

	// Limit the read too: metadata gives an exact early rejection for a regular file,
	// while `take` still bounds allocation if the file grows between metadata and read.
	let mut bytes = Vec::with_capacity(file_bytes as usize);
	file.take((MAX_SOURCE_BYTES + 1) as u64).read_to_end(&mut bytes).map_err(LoadError::Read)?;
	if bytes.len() > MAX_SOURCE_BYTES {
		return Err(LoadError::Invalid(ParseError::SourceTooLarge(bytes.len())));
	}
	let source = std::str::from_utf8(&bytes).map_err(LoadError::NotUtf8)?;
	parse(source).map_err(LoadError::Invalid)
}

#[derive(Debug, Serialize)]
pub(crate) struct StatusProjection {
	pub(crate) source: String,
	pub(crate) selected_action: Option<String>,
	pub(crate) steps: Vec<StatusStep>,
}

#[derive(Debug, Serialize)]
pub(crate) struct StatusStep {
	pub(crate) id: String,
	pub(crate) status: WorkStatus,
	pub(crate) dependencies: Vec<Dependency>,
}

#[derive(Debug, Serialize)]
pub(crate) struct Dependency {
	pub(crate) id: String,
	pub(crate) status: WorkStatus,
}

pub(crate) fn project_status(
	source: String,
	work: &WorkFile,
) -> StatusProjection {
	StatusProjection {
		source,
		selected_action: work.selected_action.clone(),
		steps: work
			.steps
			.iter()
			.map(|step| StatusStep {
				id: step.id.clone(),
				status: step.status,
				dependencies: work.dependencies(step),
			})
			.collect(),
	}
}

pub(crate) fn render_status_human(projection: &StatusProjection) -> String {
	let selected_action = projection.selected_action.as_deref().unwrap_or("none");
	let mut output = format!(
		"source: {}\nselected action: {selected_action}\nsteps ({})\n",
		projection.source,
		projection.steps.len()
	);
	for (index, step) in projection.steps.iter().enumerate() {
		let dependencies = if step.dependencies.is_empty() {
			"none".to_string()
		} else {
			step.dependencies
				.iter()
				.map(|dependency| format!("{} [{}]", dependency.id, dependency.status.label()))
				.collect::<Vec<_>>()
				.join(", ")
		};
		output.push_str(&format!(
			"{}. {} [{}]; dependencies: {dependencies}\n",
			index + 1,
			step.id,
			step.status.label()
		));
	}
	output.pop();
	output
}

pub(crate) fn render_status_json(
	projection: &StatusProjection
) -> Result<String, serde_json::Error> {
	serde_json::to_string_pretty(projection)
}

#[derive(Debug, PartialEq, Eq)]
pub(crate) struct StatusOutputTooLarge {
	pub(crate) bytes: usize,
}

impl std::fmt::Display for StatusOutputTooLarge {
	fn fmt(
		&self,
		f: &mut std::fmt::Formatter<'_>,
	) -> std::fmt::Result {
		write!(
			f,
			"status output is {} bytes; the limit is {MAX_STATUS_OUTPUT_BYTES} bytes",
			self.bytes
		)
	}
}

impl std::error::Error for StatusOutputTooLarge {}

pub(crate) fn enforce_status_output_size(output: &str) -> Result<(), StatusOutputTooLarge> {
	let bytes = output.len().saturating_add(1);
	if bytes > MAX_STATUS_OUTPUT_BYTES {
		Err(StatusOutputTooLarge {
			bytes,
		})
	} else {
		Ok(())
	}
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

	/// One step's TOML, for the dependency-rule cases that need a specific step ORDER
	/// rather than the two-step `source` fixture's fixed shape.
	fn step(
		id: &str,
		status: &str,
		blocked_by: &[&str],
	) -> String {
		let blockers =
			blocked_by.iter().map(|blocker| format!("{blocker:?}")).collect::<Vec<_>>().join(", ");
		format!(
			"\n[[step]]\nid = {id:?}\nstatus = {status:?}\nblocked_by = [{blockers}]\n\
			 user_problem = \"{id} problem\"\nchange = \"{id} change\"\n\
			 acceptance = [\"{id} acceptance\"]\nwhy_next = \"{id} why\"\n"
		)
	}

	fn work_of(
		selected_action: &str,
		steps: &[String],
	) -> String {
		format!("version = 1\nselected_action = {selected_action:?}\n{}", steps.concat())
	}

	#[test]
	fn parser_preserves_step_order_and_action_fields() {
		let work = parse(&source(Some("alpha"))).unwrap();
		assert_eq!(work.version, 1);
		assert_eq!(work.selected_action.as_deref(), Some("alpha"));
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
				"user_problem = \"Alpha\\rspoof\"",
				"step 1 field `user_problem` contains control character U+000D",
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
				"why_next = \"Beta\\tspoof\"",
				"step 2 field `why_next` contains control character U+0009",
			),
		];

		for (name, before, after, expected) in cases {
			let input = source(Some("alpha")).replace(before, after);
			let error = parse(&input).unwrap_err().to_string();
			assert_eq!(error, expected, "{name}");
		}
	}

	/// Two paragraphs with a blank line between them, at every one of the four prose
	/// sites, written as the TOML multi-line basic strings a human would actually type.
	/// The leading newline after each `"""` is TOML's own trim, so every value starts at
	/// its first word.
	fn paragraphs_source() -> String {
		"version = 1\nselected_action = \"alpha\"\n\n\
		 [[step]]\n\
		 id = \"alpha\"\n\
		 status = \"active\"\n\
		 blocked_by = []\n\
		 user_problem = \"\"\"\nProblem one.\n\nProblem two.\"\"\"\n\
		 change = \"\"\"\nChange one.\n\nChange two.\"\"\"\n\
		 acceptance = [\"\"\"\nCriterion one.\n\nCriterion two.\"\"\", \"Single line criterion\"]\n\
		 why_next = \"\"\"\nWhy one.\n\nWhy two.\"\"\"\n"
			.to_string()
	}

	#[test]
	fn every_prose_field_carries_paragraphs_verbatim() {
		let work = parse(&paragraphs_source()).unwrap();
		let step = &work.steps[0];
		assert_eq!(step.user_problem, "Problem one.\n\nProblem two.");
		assert_eq!(step.change, "Change one.\n\nChange two.");
		assert_eq!(step.acceptance, ["Criterion one.\n\nCriterion two.", "Single line criterion"]);
		assert_eq!(step.why_next, "Why one.\n\nWhy two.");
		// The structural half of the same file is untouched by the prose relaxation.
		assert_eq!(step.id, "alpha");
		assert_eq!(work.selected_action.as_deref(), Some("alpha"));
	}

	#[test]
	fn prose_accepts_the_line_feed_and_no_other_unsafe_character() {
		// One case per unsafe family, at a prose site: the tab and the carriage return a
		// terminal moves the cursor with, another C0 control, the C1 NEXT LINE, and the two
		// Unicode separators that are not control characters at all and so needed checking
		// for on top of `char::is_control`.
		let cases = [
			("tab", "\\t", "control character U+0009"),
			("carriage return", "\\r", "control character U+000D"),
			("vertical tab", "\\u000B", "control character U+000B"),
			("next line", "\\u0085", "control character U+0085"),
			("line separator", "\\u2028", "line separator U+2028"),
			("paragraph separator", "\\u2029", "paragraph separator U+2029"),
		];
		for (name, escape, expected) in cases {
			let input = source(Some("alpha")).replace(
				"user_problem = \"Alpha problem\"",
				&format!("user_problem = \"Alpha{escape}spoof\""),
			);
			assert_eq!(
				parse(&input).unwrap_err().to_string(),
				format!("step 1 field `user_problem` contains {expected}"),
				"{name}"
			);
		}
	}

	#[test]
	fn a_structural_field_rejects_the_line_feed_prose_now_accepts() {
		// The same character, the same file, the two verdicts the split exists to give.
		let cases = [
			(
				"selected_action = \"alpha\"",
				"work file field `selected_action` contains control character U+000A",
			),
			("id = \"alpha\"", "step 1 field `id` contains control character U+000A"),
			(
				"blocked_by = [\"alpha\"]",
				"step 2 field `blocked_by` item 1 contains control character U+000A",
			),
		];
		for (field, expected) in cases {
			let spoofed = field.replace("alpha", "alpha\\nspoof");
			let input = source(Some("alpha")).replace(field, &spoofed);
			assert_eq!(parse(&input).unwrap_err().to_string(), expected, "{field}");
		}

		// A structural id also rejects the two separators, which are not control
		// characters, and names each one precisely rather than calling it a control.
		for (escape, expected) in
			[("\\u2028", "line separator U+2028"), ("\\u2029", "paragraph separator U+2029")]
		{
			let input =
				source(Some("alpha")).replace("id = \"beta\"", &format!("id = \"beta{escape}\""));
			assert_eq!(
				parse(&input).unwrap_err().to_string(),
				format!("step 2 field `id` contains {expected}")
			);
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
	fn an_absent_selected_action_is_valid_only_when_every_step_is_complete() {
		let complete = source(None)
			.replacen("status = \"active\"", "status = \"complete\"", 1)
			.replacen("status = \"pending\"", "status = \"complete\"", 1);
		let work = parse(&complete).unwrap();
		assert_eq!(work.selected_action, None);
		assert!(work.steps.iter().all(|step| step.status == WorkStatus::Complete));

		let error = parse(&source(None)).unwrap_err().to_string();
		assert_eq!(
			error,
			"selected_action is required while work remains; found 1 active and 1 pending steps"
		);
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

	#[test]
	fn blockers_are_known_and_active_blockers_are_complete() {
		let unknown =
			source(Some("alpha")).replace("blocked_by = [\"alpha\"]", "blocked_by = [\"missing\"]");
		assert_eq!(
			parse(&unknown).unwrap_err().to_string(),
			"step 2 `beta` declares unknown blocker `missing`"
		);

		let unresolved = source(Some("alpha")).replace(
			"status = \"pending\"\nblocked_by = [\"alpha\"]",
			"status = \"active\"\nblocked_by = [\"alpha\"]",
		);
		assert_eq!(
			parse(&unresolved).unwrap_err().to_string(),
			"active step `beta` depends on `alpha` with status `active`; active-step blockers must be complete"
		);

		let pending = parse(&source(Some("alpha"))).unwrap();
		assert_eq!(pending.steps[1].status, WorkStatus::Pending);
	}

	#[test]
	fn a_pending_step_waits_only_on_earlier_unfinished_steps() {
		// An earlier ACTIVE predecessor is the shape the live repository state carries; an
		// earlier PENDING one is equally valid, because the wait is still owed either way.
		let valid = parse(&work_of(
			"active",
			&[
				step("active", "active", &[]),
				step("pending-one", "pending", &["active"]),
				step("pending-two", "pending", &["pending-one"]),
			],
		))
		.unwrap();
		assert_eq!(valid.steps[1].blocked_by, ["active"]);
		assert_eq!(valid.steps[2].blocked_by, ["pending-one"]);

		let cases = [
			(
				vec![step("active", "active", &[]), step("beta", "pending", &["beta"])],
				"pending step 2 `beta` declares itself as a blocker",
			),
			(
				vec![
					step("active", "active", &[]),
					step("beta", "pending", &["gamma"]),
					step("gamma", "pending", &[]),
				],
				"pending step 2 `beta` declares blocker `gamma` at step 3; pending-step blockers must be earlier steps",
			),
			(
				vec![
					step("done", "complete", &[]),
					step("active", "active", &["done"]),
					step("beta", "pending", &["done"]),
				],
				"pending step 3 `beta` depends on `done` with status `complete`; pending-step blockers must be active or pending",
			),
		];
		for (steps, expected) in cases {
			assert_eq!(parse(&work_of("active", &steps)).unwrap_err().to_string(), expected);
		}
	}

	#[test]
	fn active_and_complete_steps_carry_no_ordering_rule() {
		// A LATER complete predecessor is legal for both: the active rule speaks only to the
		// predecessor's status, and a complete step's own history is settled.
		let work = parse(&work_of(
			"alpha",
			&[
				step("alpha", "active", &["omega"]),
				step("done", "complete", &["omega"]),
				step("omega", "complete", &[]),
			],
		))
		.unwrap();
		assert_eq!(work.steps[0].blocked_by, ["omega"]);
		assert_eq!(work.steps[1].blocked_by, ["omega"]);
	}

	#[test]
	fn a_source_path_label_with_a_control_character_is_refused_without_echoing_it() {
		assert_eq!(source_label(Path::new(".agents/work.toml")).unwrap(), ".agents/work.toml");

		let error = source_label(Path::new("spoof\nsource: forged/.agents/work.toml")).unwrap_err();
		assert_eq!(
			error,
			UnsafeSourceLabel {
				character: '\n',
			}
		);
		let text = error.to_string();
		assert_eq!(
			text,
			"work source path contains control character U+000A; refusing to read it or echo it back"
		);
		assert!(!text.contains("forged"), "{text}");
	}

	#[test]
	fn source_and_step_limits_are_enforced() {
		let oversized = "x".repeat(MAX_SOURCE_BYTES + 1);
		assert_eq!(
			parse(&oversized).unwrap_err().to_string(),
			"work source is 4097 bytes; the limit is 4096 bytes"
		);

		let mut six = source(Some("alpha"));
		for id in ["gamma", "delta", "epsilon", "zeta"] {
			six.push_str(&format!(
				"\n[[step]]\nid = \"{id}\"\nstatus = \"pending\"\nblocked_by = []\n\
				 user_problem = \"p\"\nchange = \"c\"\nacceptance = [\"a\"]\nwhy_next = \"w\"\n"
			));
		}
		assert_eq!(
			parse(&six).unwrap_err().to_string(),
			"work source has 6 steps; the limit is 5 steps"
		);
	}

	#[test]
	fn status_projection_reports_completed_dependencies_truthfully() {
		let input = source(Some("beta"))
			.replacen("status = \"active\"", "status = \"complete\"", 1)
			.replacen("status = \"pending\"", "status = \"active\"", 1);
		let work = parse(&input).unwrap();
		let projection = project_status(".agents/work.toml".to_string(), &work);
		let human = render_status_human(&projection);
		let json = render_status_json(&projection).unwrap();

		assert!(human.contains("1. alpha [complete]; dependencies: none"));
		assert!(human.contains("2. beta [active]; dependencies: alpha [complete]"));
		assert!(!human.contains("blocked"));
		let value: serde_json::Value = serde_json::from_str(&json).unwrap();
		assert_eq!(value["selected_action"], "beta");
		assert_eq!(value["steps"][1]["dependencies"][0]["status"], "complete");
	}

	#[test]
	fn status_output_limit_includes_the_newline_and_never_truncates() {
		enforce_status_output_size(&"x".repeat(MAX_STATUS_OUTPUT_BYTES - 1)).unwrap();
		assert_eq!(
			enforce_status_output_size(&"x".repeat(MAX_STATUS_OUTPUT_BYTES)).unwrap_err(),
			StatusOutputTooLarge {
				bytes: MAX_STATUS_OUTPUT_BYTES + 1,
			}
		);
	}
}
