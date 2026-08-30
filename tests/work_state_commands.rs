//! End-to-end contracts for bounded-work `validate` and `status` mode.

use std::{
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

const MAX_STATUS_BYTES: usize = 16_384;
const MAX_NEXT_BYTES: usize = 8_192;

fn scratch(name: &str) -> PathBuf {
	let dir = std::env::temp_dir().join(format!(
		"agent-flow-work-state-{name}-{}-{}",
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

fn run(
	dir: &Path,
	args: &[&str],
) -> Output {
	Command::new(env!("CARGO_BIN_EXE_agent-flow"))
		.current_dir(dir)
		.args(args)
		.output()
		.expect("run agent-flow")
}

fn step(
	id: &str,
	status: &str,
	blocked_by: &[&str],
) -> String {
	let blockers =
		blocked_by.iter().map(|blocker| format!("{blocker:?}")).collect::<Vec<_>>().join(", ");
	format!(
		"[[step]]\nid = {id:?}\nstatus = {status:?}\nblocked_by = [{blockers}]\n\
		 user_problem = \"Problem for {id}\"\nchange = \"Change for {id}\"\n\
		 acceptance = [\"Acceptance for {id}\"]\nwhy_next = \"Why {id}\"\n\n"
	)
}

fn clean_work() -> String {
	format!(
		"version = 1\nselected_action = \"selected\"\n\n{}{}{}{}",
		step("complete-base", "complete", &[]),
		step("selected", "active", &["complete-base"]),
		step("parallel", "active", &["complete-base"]),
		step("later", "pending", &["selected", "parallel"]),
	)
}

fn completed_work() -> String {
	format!(
		"version = 1\n\n{}{}{}",
		step("first", "complete", &[]),
		step("second", "complete", &["first"]),
		step("third", "complete", &["first", "second"]),
	)
}

fn write_work(
	root: &Path,
	contents: &str,
) {
	write(&root.join(".agents/work.toml"), contents);
}

fn assert_work_rejected(
	name: &str,
	source: &str,
	diagnostic: &str,
) {
	let root = scratch(name);
	write_work(&root, source);
	let output = run(&root, &["validate"]);
	let stderr = String::from_utf8(output.stderr).unwrap();
	assert_eq!(output.status.code(), Some(1), "{stderr}");
	assert!(output.stdout.is_empty(), "invalid state wrote stdout");
	assert!(stderr.contains(".agents/work.toml:"), "source prefix missing from:\n{stderr}");
	assert!(stderr.contains(diagnostic), "expected source-prefixed `{diagnostic}` in:\n{stderr}");
	fs::remove_dir_all(root).unwrap();
}

#[test]
fn a_fresh_minimal_scaffold_validates_without_legacy_state() {
	let root = scratch("fresh-scaffold");
	let scaffold = run(
		&root,
		&["scaffold", "--output-dir", ".", "--write", "--principles", "default", "--vcs", "none"],
	);
	assert!(scaffold.status.success(), "{}", String::from_utf8_lossy(&scaffold.stderr));
	assert!(!root.join("docs/plans").exists());
	assert!(!root.join("docs/metrics").exists());

	let validate = run(&root, &["validate"]);
	assert!(validate.status.success(), "{}", String::from_utf8_lossy(&validate.stderr));
	assert!(validate.stderr.is_empty());
	assert!(String::from_utf8_lossy(&validate.stdout).contains("1 steps, selected action"));

	for args in [&["status"][..], &["status", "--json"][..]] {
		let status = run(&root, args);
		assert!(status.status.success(), "{}", String::from_utf8_lossy(&status.stderr));
		assert!(status.stderr.is_empty());
		assert!(status.stdout.len() <= MAX_STATUS_BYTES);
	}
	fs::remove_dir_all(root).unwrap();
}

#[test]
fn all_complete_work_without_a_selection_is_projected_by_every_real_command() {
	let root = scratch("all-complete");
	write_work(&root, &completed_work());

	let validate = run(&root, &["validate"]);
	assert!(validate.status.success(), "{}", String::from_utf8_lossy(&validate.stderr));
	assert!(validate.stderr.is_empty());
	assert_eq!(validate.stdout, b".agents/work.toml: 3 steps, all complete, valid\n");

	for args in [&["status"][..], &["status", "--json"][..], &["next"][..], &["next", "--json"][..]]
	{
		let one = run(&root, args);
		let two = run(&root, args);
		assert!(one.status.success(), "{args:?}: {}", String::from_utf8_lossy(&one.stderr));
		assert!(one.stderr.is_empty(), "{args:?}");
		assert_eq!(one.stdout, two.stdout, "{args:?}");
		let limit = if args[0] == "next" { MAX_NEXT_BYTES } else { MAX_STATUS_BYTES };
		assert!(one.stdout.len() <= limit, "{args:?}: {} bytes", one.stdout.len());
	}

	let status_human = String::from_utf8(run(&root, &["status"]).stdout).unwrap();
	assert!(status_human.contains("selected action: none"), "{status_human}");
	for (position, id) in [(1, "first"), (2, "second"), (3, "third")] {
		assert!(status_human.contains(&format!("{position}. {id} [complete]")), "{status_human}");
	}
	let status_json: serde_json::Value =
		serde_json::from_slice(&run(&root, &["status", "--json"]).stdout).unwrap();
	assert!(status_json["selected_action"].is_null());
	assert!(status_json["steps"]
		.as_array()
		.unwrap()
		.iter()
		.all(|step| step["status"] == "complete"));

	let next_human = String::from_utf8(run(&root, &["next"]).stdout).unwrap();
	assert!(next_human.contains("ACTIVE UNITS (0)"), "{next_human}");
	assert!(next_human.contains("SELECTED ACTION\nnone"), "{next_human}");
	assert!(next_human.contains("RESULT\ncompleted"), "{next_human}");
	let next_json: serde_json::Value =
		serde_json::from_slice(&run(&root, &["next", "--json"]).stdout).unwrap();
	assert_eq!(next_json["active_units"], serde_json::json!([]));
	assert!(next_json["selected_action"].is_null());
	assert_eq!(next_json["result"], "completed");

	fs::remove_dir_all(root).unwrap();
}

#[test]
fn every_real_work_command_rejects_an_absent_selection_while_work_remains() {
	let root = scratch("unfinished-without-selection");
	let unfinished = clean_work().replace("selected_action = \"selected\"\n", "");
	write_work(&root, &unfinished);

	for args in [
		&["validate"][..],
		&["status"][..],
		&["status", "--json"][..],
		&["next"][..],
		&["next", "--json"][..],
	] {
		let output = run(&root, args);
		let stderr = String::from_utf8(output.stderr).unwrap();
		assert_eq!(output.status.code(), Some(1), "{args:?}: {stderr}");
		assert!(output.stdout.is_empty(), "{args:?}: invalid state wrote stdout");
		assert!(
			stderr.contains(
				".agents/work.toml: selected_action is required while work remains; found 2 active and 1 pending steps"
			),
			"{args:?}: {stderr}"
		);
	}

	fs::remove_dir_all(root).unwrap();
}

#[test]
fn validate_rejects_every_bounded_work_invariant() {
	let mut sixth = clean_work();
	sixth.push_str(&step("fifth", "pending", &[]));
	sixth.push_str(&step("sixth", "pending", &[]));
	assert_work_rejected("sixth-step", &sixth, "work source has 6 steps; the limit is 5 steps");

	let duplicate_selection = clean_work().replacen(
		"selected_action = \"selected\"",
		"selected_action = \"selected\"\nselected_action = \"parallel\"",
		1,
	);
	assert_work_rejected(
		"duplicate-selection",
		&duplicate_selection,
		"duplicate key `selected_action`",
	);

	let duplicate_id = clean_work().replace("id = \"parallel\"", "id = \"selected\"");
	assert_work_rejected(
		"duplicate-id",
		&duplicate_id,
		"duplicate step id `selected` at steps 2 and 3",
	);

	let invalid_selection =
		clean_work().replace("selected_action = \"selected\"", "selected_action = \"later\"");
	assert_work_rejected(
		"invalid-selection",
		&invalid_selection,
		"selected_action `later` has status `pending`; expected `active`",
	);

	let unknown_status = clean_work().replacen("status = \"pending\"", "status = \"paused\"", 1);
	assert_work_rejected("unknown-status", &unknown_status, "unknown variant `paused`");

	let unknown_blocker = clean_work()
		.replace("blocked_by = [\"selected\", \"parallel\"]", "blocked_by = [\"missing\"]");
	assert_work_rejected(
		"unknown-blocker",
		&unknown_blocker,
		"step 4 `later` declares unknown blocker `missing`",
	);

	let unresolved = clean_work().replacen("status = \"complete\"", "status = \"pending\"", 1);
	assert_work_rejected(
		"unresolved-active-blocker",
		&unresolved,
		"active step `selected` depends on `complete-base` with status `pending`; active-step blockers must be complete",
	);

	assert_work_rejected(
		"oversized-source",
		&"x".repeat(4_097),
		"work source is 4097 bytes; the limit is 4096 bytes",
	);
}

#[test]
fn validate_rejects_pending_blockers_that_are_not_earlier_unfinished_steps() {
	let itself = clean_work()
		.replace("blocked_by = [\"selected\", \"parallel\"]", "blocked_by = [\"later\"]");
	assert_work_rejected(
		"pending-self-blocker",
		&itself,
		"pending step 4 `later` declares itself as a blocker",
	);

	let mut later = clean_work();
	later.push_str(&step("fifth", "pending", &[]));
	let later =
		later.replace("blocked_by = [\"selected\", \"parallel\"]", "blocked_by = [\"fifth\"]");
	assert_work_rejected(
		"pending-later-blocker",
		&later,
		"pending step 4 `later` declares blocker `fifth` at step 5; pending-step blockers must be earlier steps",
	);

	let complete = clean_work()
		.replace("blocked_by = [\"selected\", \"parallel\"]", "blocked_by = [\"complete-base\"]");
	assert_work_rejected(
		"pending-complete-blocker",
		&complete,
		"pending step 4 `later` depends on `complete-base` with status `complete`; pending-step blockers must be active or pending",
	);

	// A pending step may wait on an earlier ACTIVE or an earlier PENDING predecessor. The
	// clean fixture already carries the active case; chain a second pending step onto it for
	// the pending case, and require the real CLI to accept both.
	let root = scratch("pending-earlier-predecessors");
	let mut chained = clean_work();
	chained.push_str(&step("last", "pending", &["later"]));
	write_work(&root, &chained);
	let validate = run(&root, &["validate"]);
	assert!(validate.status.success(), "{}", String::from_utf8_lossy(&validate.stderr));
	assert!(validate.stderr.is_empty());
	assert!(String::from_utf8_lossy(&validate.stdout).contains("5 steps"));
	let human = String::from_utf8(run(&root, &["status"]).stdout).unwrap();
	assert!(
		human.contains("4. later [pending]; dependencies: selected [active], parallel [active]")
	);
	assert!(human.contains("5. last [pending]; dependencies: later [pending]"));
	fs::remove_dir_all(root).unwrap();
}

#[test]
fn a_source_path_that_could_forge_a_line_is_refused_before_any_output() {
	let root = scratch("forged-source-path");
	let spoof = root.join("spoof\nsource: forged/.agents/work.toml");
	write(&spoof, &clean_work());
	let path = spoof.to_str().unwrap();

	// Both human paths, the ones that print the source label as bare text, plus `--json` for
	// which the same path is refused before anything is rendered at all.
	for args in [
		&["validate", "--source", path][..],
		&["status", "--source", path][..],
		&["status", "--source", path, "--json"][..],
	] {
		let output = run(&root, args);
		let stderr = String::from_utf8(output.stderr).unwrap();
		assert_eq!(output.status.code(), Some(1), "{args:?}: {stderr}");
		assert!(output.stdout.is_empty(), "{args:?}: unsafe source path wrote stdout");
		assert!(
			stderr.contains(
				"work source path contains control character U+000A; refusing to read it or echo it back"
			),
			"{args:?}: {stderr}"
		);
		assert!(!stderr.contains("forged"), "{args:?}: refusal echoed the forged line: {stderr}");
		assert!(!stderr.contains("spoof"), "{args:?}: refusal echoed the raw path: {stderr}");
	}

	// The same state under a safe label still validates, so the refusal is about the PATH.
	write_work(&root, &clean_work());
	let safe = run(&root, &["validate"]);
	assert!(safe.status.success(), "{}", String::from_utf8_lossy(&safe.stderr));
	fs::remove_dir_all(root).unwrap();
}

#[test]
fn a_claimed_review_record_cannot_green_invalid_work_state() {
	let root = scratch("claimed-review");
	let invalid = clean_work()
		.replace("blocked_by = [\"selected\", \"parallel\"]", "blocked_by = [\"claimed-review\"]");
	write_work(&root, &invalid);
	let claim = "{\"type\":\"round\",\"task\":\"later\",\"step\":\"later\",\
		\"increment\":\"later\",\"artifact\":\"self-authored-review\",\
		\"phase\":\"work_review\",\"changed_since_prev\":true,\"outcome\":\"clean\",\
		\"valid_findings\":0,\"severities\":[],\"consecutive_clean\":1,\
		\"risk_class\":\"low_risk\"}\n";
	write(&root.join("docs/metrics/workflow.jsonl"), claim);
	write(&root.join("docs/metrics/nested/claimed-review.jsonl"), claim);

	for args in [&["validate"][..], &["status"][..], &["status", "--json"][..]] {
		let output = run(&root, args);
		let stderr = String::from_utf8(output.stderr).unwrap();
		assert_eq!(output.status.code(), Some(1), "{args:?}: {stderr}");
		assert!(output.stdout.is_empty(), "{args:?}: invalid work wrote stdout");
		assert!(stderr.contains("declares unknown blocker `claimed-review`"), "{stderr}");
		assert!(!stderr.contains("records, valid"), "work mode read a claimed record: {stderr}");
	}
	fs::remove_dir_all(root).unwrap();
}

#[test]
fn work_status_is_deterministic_bounded_and_truthful_in_both_formats() {
	let root = scratch("status");
	write_work(&root, &clean_work());
	write(&root.join("docs/plans/stale.plan.toml"), "not a plan");
	write(&root.join("docs/plans/stale.ledger.md"), "FAKE LEDGER");
	write(&root.join("docs/plans/stale.reviews/claim.md"), "FAKE REVIEW");
	write(&root.join("docs/metrics/workflow.jsonl"), "not jsonl");
	write(&root.join(".agents/workflow.toml"), "not a workflow spec");

	let validate = run(&root, &["validate"]);
	let explicit_validate = run(&root, &["validate", "--source", ".agents/work.toml"]);
	assert!(validate.status.success() && explicit_validate.status.success());
	assert!(validate.stderr.is_empty() && explicit_validate.stderr.is_empty());
	assert_eq!(validate.stdout, explicit_validate.stdout);
	assert_eq!(
		validate.stdout, b".agents/work.toml: 4 steps, selected action `selected`, valid\n",
		"the current nonterminal validate projection must stay compatible"
	);

	for args in [
		&["status"][..],
		&["status", "--json"][..],
		&["status", "--source", ".agents/work.toml"][..],
		&["status", "--source", ".agents/work.toml", "--json"][..],
	] {
		let one = run(&root, args);
		let two = run(&root, args);
		assert!(one.status.success(), "{args:?}: {}", String::from_utf8_lossy(&one.stderr));
		assert!(one.stderr.is_empty(), "{args:?}");
		assert_eq!(one.stdout, two.stdout, "{args:?}");
		assert!(one.stdout.len() <= MAX_STATUS_BYTES, "{args:?}: {} bytes", one.stdout.len());
		let text = String::from_utf8_lossy(&one.stdout);
		assert!(!text.contains("FAKE LEDGER") && !text.contains("not jsonl"));
	}

	let human = String::from_utf8(run(&root, &["status"]).stdout).unwrap();
	assert!(human.contains("selected action: selected"));
	assert!(human.contains("1. complete-base [complete]; dependencies: none"));
	assert!(human.contains("2. selected [active]; dependencies: complete-base [complete]"));
	assert!(
		human.contains("4. later [pending]; dependencies: selected [active], parallel [active]")
	);
	assert!(!human.contains("blocked by"));

	let json = run(&root, &["status", "--json"]);
	let value: serde_json::Value = serde_json::from_slice(&json.stdout).unwrap();
	assert_eq!(value["selected_action"], "selected");
	let steps = value["steps"].as_array().unwrap();
	assert_eq!(
		steps.iter().map(|step| step["id"].as_str().unwrap()).collect::<Vec<_>>(),
		["complete-base", "selected", "parallel", "later"]
	);
	assert_eq!(value["steps"][1]["dependencies"][0]["id"], "complete-base");
	assert_eq!(value["steps"][1]["dependencies"][0]["status"], "complete");
	fs::remove_dir_all(root).unwrap();
}

#[test]
fn oversized_status_output_fails_without_writing_a_prefix() {
	let root = scratch("oversized-status");
	let blockers = std::iter::repeat_n("\"\"", 1_280).collect::<Vec<_>>().join(",");
	let source = format!(
		"version=1\nselected_action=\"a\"\n\n\
		 [[step]]\nid=\"\"\nstatus=\"complete\"\nblocked_by=[]\nuser_problem=\"\"\n\
		 change=\"\"\nacceptance=[]\nwhy_next=\"\"\n\n\
		 [[step]]\nid=\"a\"\nstatus=\"active\"\nblocked_by=[{blockers}]\nuser_problem=\"\"\n\
		 change=\"\"\nacceptance=[]\nwhy_next=\"\"\n"
	);
	assert!(source.len() <= 4_096, "fixture is {} bytes", source.len());
	write_work(&root, &source);

	for args in [&["status"][..], &["status", "--json"][..]] {
		let output = run(&root, args);
		assert_eq!(output.status.code(), Some(1), "{args:?}");
		assert!(output.stdout.is_empty(), "{args:?}: output was partially written");
		assert!(
			String::from_utf8_lossy(&output.stderr).contains("the limit is 16384 bytes"),
			"{args:?}: {}",
			String::from_utf8_lossy(&output.stderr)
		);
	}
	fs::remove_dir_all(root).unwrap();
}

#[test]
fn explicit_legacy_inputs_and_projects_without_work_keep_compatibility() {
	for with_invalid_work in [false, true] {
		let root = scratch(if with_invalid_work { "legacy-with-work" } else { "legacy-no-work" });
		if with_invalid_work {
			write_work(&root, "this is deliberately not work TOML");
		}
		write(&root.join("legacy.jsonl"), "");
		write(&root.join("docs/metrics/workflow.jsonl"), "");

		let validate = run(&root, &["validate", "--metrics", "legacy.jsonl"]);
		assert!(validate.status.success(), "{}", String::from_utf8_lossy(&validate.stderr));
		assert_eq!(validate.stdout, b"legacy.jsonl: 0 records, valid\n");

		let status = run(&root, &["status", "--metrics", "legacy.jsonl", "--json"]);
		assert!(status.status.success(), "{}", String::from_utf8_lossy(&status.stderr));
		let value: serde_json::Value = serde_json::from_slice(&status.stdout).unwrap();
		assert!(value["plan"].is_null());
		assert_eq!(value["metrics"]["records"], 0);

		if !with_invalid_work {
			let bare_validate = run(&root, &["validate"]);
			assert!(bare_validate.status.success());
			assert_eq!(bare_validate.stdout, b"docs/metrics/workflow.jsonl: 0 records, valid\n");
			let bare_status = run(&root, &["status", "--json"]);
			assert!(bare_status.status.success());
			let value: serde_json::Value = serde_json::from_slice(&bare_status.stdout).unwrap();
			assert_eq!(value["metrics"]["records"], 0);
		}
		fs::remove_dir_all(root).unwrap();
	}
}
