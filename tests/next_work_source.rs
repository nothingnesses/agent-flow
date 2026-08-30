use std::{
	fs,
	path::{
		Path,
		PathBuf,
	},
	process::Command,
};

fn scratch(name: &str) -> PathBuf {
	let dir = std::env::temp_dir().join(format!(
		"agent-flow-next-work-{name}-{}-{}",
		std::process::id(),
		std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos()
	));
	let _ = fs::remove_dir_all(&dir);
	fs::create_dir_all(&dir).unwrap();
	dir
}

fn write(
	path: &Path,
	contents: &str,
) {
	fs::create_dir_all(path.parent().unwrap()).unwrap();
	fs::write(path, contents).unwrap();
}

fn work_source(change: &str) -> String {
	format!(
		"version = 1\nselected_action = \"second\"\n\n\
		 [[step]]\n\
		 id = \"first\"\n\
		 status = \"active\"\n\
		 blocked_by = []\n\
		 user_problem = \"First problem\"\n\
		 change = \"First change\"\n\
		 acceptance = [\"First acceptance\"]\n\
		 why_next = \"First why\"\n\n\
		 [[step]]\n\
		 id = \"second\"\n\
		 status = \"active\"\n\
		 blocked_by = []\n\
		 user_problem = \"Selected problem\"\n\
		 change = {change:?}\n\
		 acceptance = [\"Acceptance one\", \"Acceptance two\"]\n\
		 why_next = \"Selected why\"\n\n\
		 [[step]]\n\
		 id = \"third\"\n\
		 status = \"active\"\n\
		 blocked_by = []\n\
		 user_problem = \"Third problem\"\n\
		 change = \"Third change\"\n\
		 acceptance = [\"Third acceptance\"]\n\
		 why_next = \"Third why\"\n\n\
		 [[step]]\n\
		 id = \"pending\"\n\
		 status = \"pending\"\n\
		 blocked_by = [\"second\"]\n\
		 user_problem = \"PENDING PROSE MUST STAY HIDDEN\"\n\
		 change = \"Pending change\"\n\
		 acceptance = [\"Pending acceptance\"]\n\
		 why_next = \"Pending why\"\n"
	)
}

fn run(
	dir: &Path,
	args: &[&str],
) -> std::process::Output {
	Command::new(env!("CARGO_BIN_EXE_agent-flow"))
		.args(args)
		.current_dir(dir)
		.output()
		.expect("run agent-flow")
}

fn assert_work_error(
	name: &str,
	source: &str,
	diagnostic: &str,
) {
	let root = scratch(name);
	write(&root.join(".agents/work.toml"), source);

	let output = run(&root, &["next"]);
	let stderr = String::from_utf8(output.stderr).unwrap();
	assert_eq!(output.status.code(), Some(1), "{stderr}");
	assert!(output.stdout.is_empty(), "invalid work must not write stdout");
	let prefixed = format!(".agents/work.toml: {diagnostic}");
	assert!(stderr.contains(&prefixed), "expected `{prefixed}` in `{stderr}`");

	let _ = fs::remove_dir_all(root);
}

#[test]
fn default_and_explicit_work_sources_are_small_deterministic_and_truthful() {
	let root = scratch("projection");
	write(&root.join(".agents/work.toml"), &work_source("Selected change"));
	write(&root.join("old.ledger.md"), "## RESUME STATE\nVERBATIM LEDGER SENTINEL\n");
	write(&root.join("old.jsonl"), "not valid metrics\n");

	let human_args = ["next", "--ledger-fragment", "old.ledger.md", "--metrics", "old.jsonl"];
	let human_one = run(&root, &human_args);
	let human_two = run(&root, &human_args);
	assert!(human_one.status.success(), "{}", String::from_utf8_lossy(&human_one.stderr));
	assert!(human_one.stderr.is_empty());
	assert!(human_two.stderr.is_empty());
	assert_eq!(human_one.stdout, human_two.stdout);
	assert!(human_one.stdout.len() <= 8_192);
	let human = String::from_utf8(human_one.stdout).unwrap();
	assert_eq!(human.matches("SELECTED ACTION").count(), 1);
	for id in ["first", "second", "third"] {
		assert_eq!(
			human.lines().filter(|line| line.starts_with(&format!("- {id} ["))).count(),
			1,
			"{human}"
		);
	}
	assert!(!human.contains("PENDING PROSE MUST STAY HIDDEN"));
	assert!(!human.contains("VERBATIM LEDGER SENTINEL"));
	assert!(human.contains("user problem: Selected problem"));
	assert!(human.contains("change: Selected change"));
	assert!(human.contains("why next: Selected why"));
	assert!(!human.contains("\nRESULT\n"), "nonterminal human output changed: {human}");

	let json_one = run(&root, &["next", "--json"]);
	let json_two = run(&root, &["next", "--json"]);
	assert!(json_one.status.success(), "{}", String::from_utf8_lossy(&json_one.stderr));
	assert!(json_one.stderr.is_empty());
	assert!(json_two.stderr.is_empty());
	assert_eq!(json_one.stdout, json_two.stdout);
	assert!(json_one.stdout.len() <= 8_192);
	let value: serde_json::Value = serde_json::from_slice(&json_one.stdout).unwrap();
	let active = value["active_units"].as_array().unwrap();
	assert_eq!(active.len(), 3);
	assert_eq!(
		active.iter().map(|unit| unit["id"].as_str().unwrap()).collect::<Vec<_>>(),
		["first", "second", "third"]
	);
	assert_eq!(value["selected_action"]["id"], "second");
	assert_eq!(
		value.as_object().unwrap().keys().filter(|key| *key == "selected_action").count(),
		1
	);
	assert!(value.get("result").is_none(), "nonterminal JSON output gained a result field");
	let json = String::from_utf8(json_one.stdout).unwrap();
	assert!(!json.contains("PENDING PROSE MUST STAY HIDDEN"));
	assert!(!json.contains("VERBATIM LEDGER SENTINEL"));

	let explicit = run(&root, &["next", "--source", ".agents/work.toml", "--json"]);
	assert!(explicit.status.success(), "{}", String::from_utf8_lossy(&explicit.stderr));
	assert!(explicit.stderr.is_empty());
	assert_eq!(explicit.stdout, json.into_bytes());

	let _ = fs::remove_dir_all(root);
}

#[test]
fn invalid_work_sources_fail_without_stdout_and_name_the_source() {
	let duplicate = work_source("Selected change").replace("id = \"third\"", "id = \"first\"");
	assert_work_error("duplicate-id", &duplicate, "duplicate step id `first` at steps 1 and 3");

	let selected_non_active = work_source("Selected change")
		.replace("selected_action = \"second\"", "selected_action = \"pending\"");
	assert_work_error(
		"selected-non-active",
		&selected_non_active,
		"selected_action `pending` has status `pending`; expected `active`",
	);

	assert_work_error(
		"multiline-field",
		&work_source("line one\nline two"),
		"step 2 field `change` contains control character U+000A",
	);
}

#[test]
fn oversized_work_source_fails_before_next_projects_it() {
	let root = scratch("oversized");
	write(&root.join(".agents/work.toml"), &work_source(&"x".repeat(8_192)));

	for args in [&["next"][..], &["next", "--json"][..]] {
		let output = run(&root, args);
		assert_eq!(output.status.code(), Some(1));
		assert!(output.stdout.is_empty(), "oversized input must not write partial output");
		assert!(
			String::from_utf8_lossy(&output.stderr).contains("the limit is 4096 bytes"),
			"{}",
			String::from_utf8_lossy(&output.stderr)
		);
	}

	let _ = fs::remove_dir_all(root);
}
