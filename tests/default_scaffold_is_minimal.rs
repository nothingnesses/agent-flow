//! End-to-end contract for the built-in minimal scaffold.

use std::{
	collections::{
		BTreeMap,
		BTreeSet,
	},
	fs,
	path::{
		Path,
		PathBuf,
	},
	process::{
		Command,
		Output,
	},
};

const MAX_GUIDANCE_BYTES: usize = 65_536;
const MAX_PROMPT_BYTES: usize = 4_096;
const MAX_WORK_BYTES: usize = 4_096;

/// The standalone review prompt is pasted by hand into whatever harness the human uses,
/// so it competes for the same context window as the code under review. The accepted
/// limit is strictly below 2,000 bytes, far under the general prompt ceiling: the surface
/// was chosen over a command because it is compact, and a prompt that grows into a
/// document stops being that. This constant is the only place that limit is enforced.
const MAX_REVIEW_PROMPT_BYTES: usize = 2_000;

/// The four severity values the reviewer role prompt already uses. The standalone prompt
/// keeps the same scale so a finding reads the same whichever surface produced it.
const SEVERITIES: [&str; 4] = ["`low`", "`medium`", "`high`", "`critical`"];

/// Every persisted review-state family the reset deleted. Shipping a review surface is
/// exactly the change that could bring one back, so the prompt must name each as
/// forbidden: a reader told only "read-only" can still believe that writing up findings
/// into a file is part of reviewing rather than a violation of it.
const FORBIDDEN_REVIEW_STATE: [&str; 7] = [
	"findings file",
	"report",
	"ledger",
	"round log",
	"review directory",
	"plan tree",
	"task state",
];

fn scratch(name: &str) -> PathBuf {
	let dir = std::env::temp_dir()
		.join(format!("agent-flow-minimal-scaffold-{}-{name}", std::process::id()));
	let _ = fs::remove_dir_all(&dir);
	fs::create_dir_all(&dir).unwrap();
	let output = Command::new("git").arg("init").arg("-q").arg(&dir).output().unwrap();
	assert!(
		output.status.success(),
		"git init failed: {}",
		String::from_utf8_lossy(&output.stderr)
	);
	dir
}

fn scaffold(root: &Path) -> Output {
	Command::new(env!("CARGO_BIN_EXE_agent-flow"))
		.args(["scaffold", "--output-dir"])
		.arg(root)
		.args(["--write", "--principles", "default"])
		.output()
		.unwrap()
}

fn collect_files(
	root: &Path,
	dir: &Path,
	files: &mut BTreeMap<String, Vec<u8>>,
) {
	let mut entries = fs::read_dir(dir).unwrap().map(|entry| entry.unwrap()).collect::<Vec<_>>();
	entries.sort_by_key(|entry| entry.file_name());
	for entry in entries {
		let path = entry.path();
		let relative = path.strip_prefix(root).unwrap();
		if relative.components().next().is_some_and(|component| component.as_os_str() == ".git") {
			continue;
		}
		if path.is_dir() {
			collect_files(root, &path, files);
		} else {
			files.insert(relative.to_string_lossy().replace('\\', "/"), fs::read(path).unwrap());
		}
	}
}

fn snapshot(root: &Path) -> BTreeMap<String, Vec<u8>> {
	let mut files = BTreeMap::new();
	collect_files(root, root, &mut files);
	files
}

fn collect_dirs(
	root: &Path,
	dir: &Path,
	dirs: &mut BTreeSet<String>,
) {
	for entry in fs::read_dir(dir).unwrap().map(|entry| entry.unwrap()) {
		let path = entry.path();
		if !path.is_dir() {
			continue;
		}
		let relative = path.strip_prefix(root).unwrap();
		if relative.components().next().is_some_and(|component| component.as_os_str() == ".git") {
			continue;
		}
		dirs.insert(relative.to_string_lossy().replace('\\', "/"));
		collect_dirs(root, &path, dirs);
	}
}

/// Every directory under `root`, `.git` aside, relative and forward-slashed.
///
/// Collected separately from the file snapshot because an EMPTY directory holds no
/// file whose path could carry its name, so a criterion phrased over file paths
/// alone cannot fail for one. The no-review-directory criterion is about the
/// directory itself, so it is checked against this.
fn directories(root: &Path) -> BTreeSet<String> {
	let mut dirs = BTreeSet::new();
	collect_dirs(root, root, &mut dirs);
	dirs
}

#[test]
fn default_scaffold_is_bounded_parseable_and_byte_idempotent() {
	let root = scratch("default");
	let first = scaffold(&root);
	assert!(
		first.status.success(),
		"first scaffold failed:\nstdout:\n{}\nstderr:\n{}",
		String::from_utf8_lossy(&first.stdout),
		String::from_utf8_lossy(&first.stderr)
	);

	let first_files = snapshot(&root);
	let expected = [
		".agents/AGENTS.reference.md",
		".agents/principles.toml",
		".agents/prompts/fixer.md",
		".agents/prompts/implementer.md",
		".agents/prompts/reviewer.md",
		".agents/prompts/triager.md",
		".agents/prompts/verifier.md",
		".agents/user-prompts/adopt.md",
		".agents/user-prompts/kickoff.md",
		".agents/user-prompts/review.md",
		".agents/work.toml",
		"AGENTS.md",
	];
	assert_eq!(
		first_files.keys().map(String::as_str).collect::<Vec<_>>(),
		expected,
		"the module-free scaffold should create only the minimal core assets"
	);
	assert!(!root.join(".git/hooks/pre-commit").exists());
	assert!(!root.join(".agents/LEDGER.template.md").exists());
	assert!(!root.join(".agents/workflow.toml").exists());
	assert!(!root.join("docs/plans").exists());
	assert!(!root.join("docs/metrics/workflow.jsonl").exists());
	// The criterion is "no review DIRECTORY", so it is checked against the directory
	// walk: an empty one fails it too, not only one that happens to hold a file. The
	// file check stays as the second half of the same claim.
	let first_dirs = directories(&root);
	assert!(
		first_dirs.iter().all(|path| !path.contains("reviews")),
		"the scaffold must create no review directory, empty or not: {first_dirs:?}"
	);
	assert!(
		first_files.keys().all(|path| !path.contains("reviews")),
		"the scaffold must create no file under a review directory"
	);

	let work = first_files.get(".agents/work.toml").unwrap();
	assert!(work.len() <= MAX_WORK_BYTES, "work.toml is {} bytes", work.len());
	let parsed: toml::Value = toml::from_str(std::str::from_utf8(work).unwrap()).unwrap();
	let steps = parsed.get("step").and_then(toml::Value::as_array).unwrap();
	assert!(!steps.is_empty() && steps.len() <= 5);
	let selected = parsed.get("selected_action").and_then(toml::Value::as_str).unwrap();
	let active = steps
		.iter()
		.filter(|step| step.get("status").and_then(toml::Value::as_str) == Some("active"))
		.collect::<Vec<_>>();
	assert_eq!(active.len(), 1, "the starter has exactly one active step");
	let starter = active[0];
	assert_eq!(starter.get("id").and_then(toml::Value::as_str), Some(selected));
	for field in ["user_problem", "change", "why_next"] {
		assert!(
			starter.get(field).and_then(toml::Value::as_str).is_some_and(|text| !text.is_empty()),
			"starter field `{field}` has useful text"
		);
	}
	let acceptance = starter.get("acceptance").and_then(toml::Value::as_array).unwrap();
	assert!(
		acceptance.len() >= 2
			&& acceptance.iter().all(|item| item.as_str().is_some_and(|text| !text.is_empty())),
		"starter acceptance has useful criteria"
	);
	for step in steps {
		assert!(
			matches!(
				step.get("status").and_then(toml::Value::as_str),
				Some("active" | "pending" | "complete")
			),
			"starter statuses use the closed work parser vocabulary"
		);
	}

	// A successful `next` invocation proves the scaffolded bytes pass the step-1
	// work parser, not merely TOML's generic parser.
	let next = Command::new(env!("CARGO_BIN_EXE_agent-flow"))
		.current_dir(&root)
		.args(["next", "--source", ".agents/work.toml", "--json"])
		.output()
		.unwrap();
	assert!(
		next.status.success(),
		"next rejected starter work.toml: {}",
		String::from_utf8_lossy(&next.stderr)
	);
	let projection: serde_json::Value = serde_json::from_slice(&next.stdout).unwrap();
	assert_eq!(projection["active_units"].as_array().unwrap().len(), 1);
	assert_eq!(projection["selected_action"]["id"], selected);

	let guidance_bytes: usize = first_files
		.iter()
		.filter(|(path, _)| path.as_str() != ".agents/work.toml")
		.map(|(_, contents)| contents.len())
		.sum();
	assert!(guidance_bytes <= MAX_GUIDANCE_BYTES, "default guidance is {guidance_bytes} bytes");
	for (path, contents) in &first_files {
		if path.starts_with(".agents/prompts/") || path.starts_with(".agents/user-prompts/") {
			assert!(contents.len() <= MAX_PROMPT_BYTES, "{path} is {} bytes", contents.len());
		}
	}

	let second = scaffold(&root);
	assert!(
		second.status.success(),
		"second scaffold failed:\nstdout:\n{}\nstderr:\n{}",
		String::from_utf8_lossy(&second.stdout),
		String::from_utf8_lossy(&second.stderr)
	);
	assert_eq!(snapshot(&root), first_files, "a second scaffold must be byte-identical");

	fs::remove_dir_all(root).unwrap();
}

/// The no-review-directory criterion checked above is only worth its wording if it
/// can fail for a review directory that holds nothing. Plant an empty one and show
/// both halves: the file snapshot the criterion used to rest on cannot see it, and
/// the directory walk the criterion now rests on does.
#[test]
fn the_no_review_directory_criterion_fails_for_an_empty_review_directory() {
	let root = scratch("empty-review-dir");
	let planted = root.join("docs/plans/agent-scaffold.reviews");
	fs::create_dir_all(&planted).unwrap();

	let files = snapshot(&root);
	assert!(
		files.keys().all(|path| !path.contains("reviews")),
		"a file snapshot cannot see an empty review directory, so it cannot carry the criterion"
	);

	let dirs = directories(&root);
	assert!(
		dirs.contains("docs/plans/agent-scaffold.reviews"),
		"the directory walk must see an empty review directory: {dirs:?}"
	);
	assert!(
		!dirs.iter().all(|path| !path.contains("reviews")),
		"the criterion as asserted above must fail for an empty review directory"
	);

	fs::remove_dir_all(root).unwrap();
}

/// The one line of `prompt` that starts with `marker`, panicking if it is missing or
/// repeated. Anchoring each clause to its own line is what makes the assertions below a
/// contract rather than a bag of substrings: a required phrase that drifted into some
/// other sentence no longer satisfies the clause it was meant to pin, and a duplicated
/// clause (two target-mode lines saying different things) fails instead of half-passing.
fn clause<'a>(
	prompt: &'a str,
	marker: &str,
) -> &'a str {
	let mut matched = prompt.lines().filter(|line| line.starts_with(marker));
	let line = matched
		.next()
		.unwrap_or_else(|| panic!("the review prompt has no line starting with {marker:?}"));
	assert!(
		matched.next().is_none(),
		"the review prompt has more than one line starting with {marker:?}, so pinning that clause would check only the first"
	);
	line
}

/// Assert that the `name` clause states every phrase in `required`.
fn assert_states(
	name: &str,
	line: &str,
	required: &[&str],
) {
	for phrase in required {
		assert!(
			line.contains(phrase),
			"the {name} clause of the review prompt must state {phrase:?}, but it reads {line:?}"
		);
	}
}

/// Pin the standalone review prompt's contract as the scaffold ships it.
///
/// This asset is a human-invoked reference prompt: it is copied out of the scaffold and
/// pasted into an arbitrary harness, so no code downstream re-derives or enforces what it
/// means. Its bytes ARE the contract, which is why the meaning is asserted here and not
/// just its presence in the asset list. Each group below pins one clause the decision to
/// ship a prompt rather than a `review` command rests on.
#[test]
fn the_scaffolded_review_prompt_pins_its_standalone_contract() {
	let root = scratch("review-prompt");
	let output = scaffold(&root);
	assert!(
		output.status.success(),
		"scaffold failed:\nstdout:\n{}\nstderr:\n{}",
		String::from_utf8_lossy(&output.stdout),
		String::from_utf8_lossy(&output.stderr)
	);

	let prompt = fs::read_to_string(root.join(".agents/user-prompts/review.md")).unwrap();
	assert!(
		prompt.len() < MAX_REVIEW_PROMPT_BYTES,
		"the review prompt is {} bytes; the compact limit is under {MAX_REVIEW_PROMPT_BYTES}",
		prompt.len()
	);
	assert!(
		prompt.is_ascii(),
		"the review prompt is pasted into unknown harnesses and terminals, so it stays ASCII-only"
	);

	// Both target modes, and the exclusivity between them. The failure this guards is
	// concrete and silent: asking for a whole-tree review as if it were a diff resolves to
	// an empty range, which reviews nothing and reports nothing wrong.
	assert_states(
		"target-mode",
		clause(&prompt, "Give me a standalone"),
		&["read-only", "exactly one target mode"],
	);
	assert_states(
		"CURRENT TREE",
		clause(&prompt, "- CURRENT TREE at"),
		&["complete tree", "no baseline", "never a diff review", "never an empty one"],
	);
	assert_states(
		"DIFF",
		clause(&prompt, "- DIFF from"),
		&[
			"`<base>..<tip>`",
			"only the surrounding code needed to judge them",
			"Do not widen this into a whole-tree review",
		],
	);

	// Criteria and a stated starting point. Refs resolved in full and a clean-or-dirty
	// statement are what make the review reproducible by someone who was not there.
	assert!(
		prompt.lines().any(|line| line.starts_with("Criteria:")),
		"the review prompt must carry a criteria slot for the human to fill"
	);
	assert_states(
		"setup",
		clause(&prompt, "Before reviewing,"),
		&["full commit ID", "clean or dirty", "stop and ask"],
	);

	// Read-only work, a direct response, and no persisted review state of any family.
	// The non-mutation ban is scoped to the reviewed repository and bounded at both ends
	// by a `git status --porcelain` comparison: unscoped, it also forbids the isolated
	// reproduction the evidence clause below requires, and without the closing comparison
	// the permitted scratch has nothing proving it stayed outside the reviewed tree.
	let read_only = clause(&prompt, "Work read-only.");
	assert_states(
		"read-only",
		read_only,
		&[
			"Do not edit",
			"format",
			"stage, commit or delete any file in the reviewed repository",
			"index, refs or configuration",
			"human-authorised scratch directory outside that repository",
			"Record `git status --porcelain` before and after",
			"report any difference",
			"Return the review directly in this response.",
		],
	);
	for family in FORBIDDEN_REVIEW_STATE {
		assert!(
			read_only.contains(family),
			"the read-only clause must forbid writing a {family}, the review-state family the reset removed; it reads {read_only:?}"
		);
	}

	// Severity and reproducible evidence, so a finding can be checked rather than believed.
	// A textual citation carries the revision it was read at, which is what makes it
	// resolve for the reader in either target mode: a bare `file:line` names different
	// content at each end of a diff, and names nothing at all for a deleted line.
	let evidence = clause(&prompt, "Give each finding a severity");
	assert_states(
		"evidence",
		evidence,
		&["exact command", "`<full-commit-id>:<file>:<line>`", "out of scope, not a finding"],
	);
	for severity in SEVERITIES {
		assert!(
			evidence.contains(severity),
			"the evidence clause must offer the {severity} severity; it reads {evidence:?}"
		);
	}

	// A clean review must have a short, unambiguous way to say so. Without it, an agent
	// with nothing to report is pushed toward padding the response with non-findings.
	assert_states(
		"clean-result",
		clause(&prompt, "If nothing violates the criteria,"),
		&["`No findings.`", "the checks you ran"],
	);

	fs::remove_dir_all(root).unwrap();
}
