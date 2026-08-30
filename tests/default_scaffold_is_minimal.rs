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
		".agents/user-prompts/kickoff.md",
		".agents/work.toml",
		"AGENTS.md",
	];
	assert_eq!(
		first_files.keys().map(String::as_str).collect::<Vec<_>>(),
		expected,
		"the module-free scaffold should create only the minimal core assets"
	);
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
