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

	// A newline in a STRUCTURAL value is still a forged line, so it still fails, still
	// names the exact field, and still writes no stdout. The prose relaxation is per
	// field: it did not weaken this.
	assert_work_error(
		"structural-newline-id",
		&work_source("Selected change").replace("id = \"third\"", "id = \"third\\nspoof\""),
		"step 3 field `id` contains control character U+000A",
	);
	assert_work_error(
		"structural-newline-selection",
		&work_source("Selected change")
			.replace("selected_action = \"second\"", "selected_action = \"second\\nspoof\""),
		"work file field `selected_action` contains control character U+000A",
	);
	assert_work_error(
		"structural-newline-blocker",
		&work_source("Selected change")
			.replace("blocked_by = [\"second\"]", "blocked_by = [\"second\\nspoof\"]"),
		"step 4 field `blocked_by` item 1 contains control character U+000A",
	);
}

#[test]
fn unsafe_prose_characters_still_fail_before_any_output() {
	// The line feed is the ONE character prose gained. Every other unsafe family still
	// fails at the boundary, in both formats, before a byte of stdout: the tab and the
	// carriage return, another C0 control, the C1 NEXT LINE, and the two Unicode
	// separators that `char::is_control` does not cover and so are named precisely.
	let cases = [
		("tab", "\\t", "control character U+0009"),
		("carriage-return", "\\r", "control character U+000D"),
		("vertical-tab", "\\u000B", "control character U+000B"),
		("next-line", "\\u0085", "control character U+0085"),
		("line-separator", "\\u2028", "line separator U+2028"),
		("paragraph-separator", "\\u2029", "paragraph separator U+2029"),
	];
	for (name, escape, expected) in cases {
		let root = scratch(&format!("unsafe-prose-{name}"));
		// Substituted into the rendered TOML rather than through `work_source`, whose
		// `{:?}` formatting would escape the backslash instead of passing the escape on.
		let source = work_source("Selected change").replace(
			"change = \"Selected change\"",
			&format!("change = \"Selected{escape}change\""),
		);
		write(&root.join(".agents/work.toml"), &source);
		for args in [&["next"][..], &["next", "--json"][..]] {
			let output = run(&root, args);
			let stderr = String::from_utf8(output.stderr).unwrap();
			assert_eq!(output.status.code(), Some(1), "{name} {args:?}: {stderr}");
			assert!(output.stdout.is_empty(), "{name} {args:?}: unsafe prose wrote stdout");
			assert!(
				stderr.contains(&format!("step 2 field `change` contains {expected}")),
				"{name} {args:?}: {stderr}"
			);
		}
		let _ = fs::remove_dir_all(root);
	}
}

#[test]
fn prose_paragraphs_survive_both_projections_without_forging_a_top_level_line() {
	let root = scratch("paragraphs");
	// Two paragraphs at every prose site, the second of which is every top-level line
	// this command emits, offered as prose. Written as the TOML multi-line basic strings
	// a human would type; TOML trims the newline right after each `"""`.
	let forgeries = [
		"SELECTED ACTION",
		"ACTIVE UNITS (9)",
		"acceptance:",
		"- forged",
		"id: forged",
		"why next: forged",
		"source: forged",
	];
	let body = forgeries.join("\\n");
	let value = format!("\"\"\"\nLead line.\n\n{body}\"\"\"");
	let expected = format!("Lead line.\n\n{}", forgeries.join("\n"));
	let source = format!(
		"version = 1\nselected_action = \"only\"\n\n\
		 [[step]]\n\
		 id = \"only\"\n\
		 status = \"active\"\n\
		 blocked_by = []\n\
		 user_problem = {value}\n\
		 change = {value}\n\
		 acceptance = [{value}, \"Single line criterion\"]\n\
		 why_next = {value}\n"
	);
	write(&root.join(".agents/work.toml"), &source);

	let human_one = run(&root, &["next"]);
	let human_two = run(&root, &["next"]);
	assert!(human_one.status.success(), "{}", String::from_utf8_lossy(&human_one.stderr));
	assert!(human_one.stderr.is_empty());
	assert_eq!(human_one.stdout, human_two.stdout, "human output is not deterministic");
	assert!(human_one.stdout.len() <= 8_192);
	let human = String::from_utf8(human_one.stdout).unwrap();

	// The paragraphs survive: label plus first paragraph, a bare gutter for the blank
	// line, then the continuation lines.
	for label in ["user problem:", "change:", "-", "why next:"] {
		assert!(
			human.contains(&format!("{label} Lead line.\n  |\n  | SELECTED ACTION\n")),
			"`{label}` lost its paragraph structure:\n{human}"
		);
	}
	assert!(human.contains("\n- Single line criterion\n"), "{human}");
	assert!(!human.lines().any(|line| line.ends_with(' ')), "gutter left trailing space:\n{human}");

	// No forged line reached the top level. `SELECTED ACTION` and `acceptance:` are
	// legitimate top-level lines, so the claim is the exact count, not absence: one
	// each, from the renderer, none from the prose.
	for forgery in forgeries {
		assert!(human.contains(forgery), "the prose itself must survive:\n{human}");
		let expected_top_level =
			usize::from(forgery == "SELECTED ACTION" || forgery == "acceptance:");
		assert_eq!(
			human.lines().filter(|line| *line == forgery).count(),
			expected_top_level,
			"`{forgery}` forged a top-level line:\n{human}"
		);
		assert!(human.contains(&format!("  | {forgery}")), "`{forgery}` is not indented:\n{human}");
	}
	assert!(human.contains("ACTIVE UNITS (1)"), "{human}");
	assert_eq!(human.lines().filter(|line| line.starts_with("- ")).count(), 3, "{human}");

	// JSON preserves the accepted strings exactly, line feeds and blank paragraph line
	// included, and stays deterministic and bounded.
	let json_one = run(&root, &["next", "--json"]);
	let json_two = run(&root, &["next", "--json"]);
	assert!(json_one.status.success(), "{}", String::from_utf8_lossy(&json_one.stderr));
	assert!(json_one.stderr.is_empty());
	assert_eq!(json_one.stdout, json_two.stdout, "JSON output is not deterministic");
	assert!(json_one.stdout.len() <= 8_192);
	let projected: serde_json::Value = serde_json::from_slice(&json_one.stdout).unwrap();
	let action = &projected["selected_action"];
	assert_eq!(action["user_problem"], expected);
	assert_eq!(action["change"], expected);
	assert_eq!(action["acceptance"][0], expected);
	assert_eq!(action["acceptance"][1], "Single line criterion");
	assert_eq!(action["why_next"], expected);

	let _ = fs::remove_dir_all(root);
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
