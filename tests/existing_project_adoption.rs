use std::{
	collections::BTreeMap,
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

const GUIDE: &str = include_str!("../docs/adoption.md");
const PROMPT: &str = include_str!("../pack/user-prompts/adopt.md");

fn block(language: &str) -> &str {
	GUIDE.split_once(&format!("```{language}\n")).unwrap().1.split_once("```").unwrap().0
}

fn guide_commands() -> Vec<Vec<&'static str>> {
	GUIDE
		.lines()
		.filter_map(|line| line.strip_prefix("agent-flow "))
		.map(|line| line.split_whitespace().collect())
		.collect()
}

fn success(output: Output) -> String {
	assert!(
		output.status.success(),
		"stdout: {}\nstderr: {}",
		String::from_utf8_lossy(&output.stdout),
		String::from_utf8_lossy(&output.stderr)
	);
	String::from_utf8(output.stdout).unwrap()
}

fn git(
	root: &Path,
	args: &[&str],
) -> String {
	success(
		Command::new("git")
			.current_dir(root)
			.env("GIT_OPTIONAL_LOCKS", "0")
			.args(args)
			.output()
			.unwrap(),
	)
}

fn cli(
	root: &Path,
	args: &[&str],
	directory_pack: bool,
) -> String {
	let mut command = Command::new(env!("CARGO_BIN_EXE_agent-flow"));
	command.current_dir(root).args(args);
	if directory_pack && args[0] == "scaffold" {
		command.arg("--template").arg(Path::new(env!("CARGO_MANIFEST_DIR")).join("pack"));
	}
	success(command.output().unwrap())
}

fn put(
	root: &Path,
	path: &str,
	contents: &str,
) {
	let path = root.join(path);
	fs::create_dir_all(path.parent().unwrap()).unwrap();
	fs::write(path, contents).unwrap();
}

fn snapshot(root: &Path) -> BTreeMap<PathBuf, Vec<u8>> {
	fn collect(
		root: &Path,
		dir: &Path,
		files: &mut BTreeMap<PathBuf, Vec<u8>>,
	) {
		for entry in fs::read_dir(dir).unwrap() {
			let path = entry.unwrap().path();
			if path.is_dir() {
				collect(root, &path, files);
			} else {
				files.insert(path.strip_prefix(root).unwrap().to_owned(), fs::read(path).unwrap());
			}
		}
	}
	let mut files = BTreeMap::new();
	collect(root, root, &mut files);
	files
}

fn fixture(
	name: &str,
	existing_work: bool,
) -> PathBuf {
	let root =
		std::env::temp_dir().join(format!("agent-flow-adoption-{}-{name}", std::process::id()));
	if root.exists() {
		fs::remove_dir_all(&root).unwrap();
	}
	fs::create_dir_all(&root).unwrap();
	git(&root, &["init", "-q"]);
	for (path, text) in [
		("AGENTS.md", "# Project instructions\n\nPreserve the public API.\n"),
		(
			"docs/plans/product.md",
			"# Product plan\n\n- [x] Historical launch.\n- [ ] Broader redesign, not approved.\n",
		),
		("docs/specification.md", "# Specification\n\nThe public API remains stable.\n"),
		(".agents/checks.toml", "# Project checks, do not execute during adoption.\n"),
		(".agents/checks/local.sh", "#!/bin/sh\nexit 97\n"),
		(".agents/hooks/pre-commit", "#!/bin/sh\nexit 98\n"),
		("src/product.txt", "original\n"),
	] {
		put(&root, path, text);
	}
	if existing_work {
		put(&root, ".agents/work.toml", &block("toml").replace("clarify-help", "existing-action"));
	}
	git(&root, &["add", "."]);
	git(
		&root,
		&[
			"-c",
			"user.name=Fixture",
			"-c",
			"user.email=fixture@example.invalid",
			"-c",
			"core.hooksPath=/dev/null",
			"-c",
			"commit.gpgsign=false",
			"commit",
			"-qm",
			"Initial fixture",
		],
	);
	put(&root, ".git/hooks/pre-commit", "#!/bin/sh\nexit 99\n");
	put(&root, "src/product.txt", "staged unrelated change\n");
	git(&root, &["add", "src/product.txt"]);
	put(&root, "src/product.txt", "unstaged unrelated change\n");
	put(&root, "notes.txt", "Untracked project notes.\n");
	put(&root, ".agents/AGENTS.reference.md", "Old tool reference, approved for replacement.\n");
	root
}

#[test]
fn displayed_adoption_commands_preserve_existing_projects() {
	let commands = guide_commands();
	assert_eq!(commands.len(), 7);
	assert_eq!(
		commands[0],
		["scaffold", "--output-dir", ".", "--vcs", "none", "--principles", "default", "--dry-run"]
	);
	assert_eq!(
		commands[1],
		["scaffold", "--output-dir", ".", "--vcs", "none", "--principles", "default", "--write"]
	);
	for directory_pack in [false, true] {
		for existing_work in [false, true] {
			let root = fixture(&format!("{directory_pack}-{existing_work}"), existing_work);
			let before = snapshot(&root);
			let preview = cli(&root, &commands[0], directory_pack);
			assert!(preview.contains(".agents/user-prompts/adopt.md"));
			assert!(preview.contains("skip (exists)  AGENTS.md"));
			assert!(preview.contains("refresh  .agents/AGENTS.reference.md"));
			assert_eq!(snapshot(&root), before, "dry-run changed the project");

			cli(&root, &commands[1], directory_pack);
			let installed = snapshot(&root);
			for (path, contents) in &before {
				if path != Path::new(".agents/AGENTS.reference.md") {
					assert_eq!(installed.get(path), Some(contents), "changed {}", path.display());
				}
			}
			assert_ne!(
				installed[Path::new(".agents/AGENTS.reference.md")],
				before[Path::new(".agents/AGENTS.reference.md")]
			);
			assert_eq!(installed[Path::new(".agents/user-prompts/adopt.md")], PROMPT.as_bytes());
			if !existing_work {
				assert_eq!(
					installed[Path::new(".agents/work.toml")],
					include_bytes!("../pack/work.toml").as_slice()
				);
				put(&root, ".agents/work.toml", block("toml"));
			}
			let instructions = fs::read_to_string(root.join("AGENTS.md")).unwrap();
			put(&root, "AGENTS.md", &format!("{instructions}\nRead `.agents/AGENTS.reference.md` for the approved delivery workflow.\n"));
			let adopted = snapshot(&root);
			let expected_action = if existing_work { "existing-action" } else { "clarify-help" };
			for args in &commands[2 ..] {
				let output = cli(&root, args, directory_pack);
				if args.contains(&"--json") {
					let value: serde_json::Value = serde_json::from_str(&output).unwrap();
					if args[0] == "next" {
						assert_eq!(value["selected_action"]["id"], expected_action);
					} else {
						assert_eq!(value["selected_action"], expected_action);
					}
				} else if args[0] != "validate" {
					assert!(output.contains(expected_action));
				}
				assert_eq!(snapshot(&root), adopted, "read-only command changed the project");
			}

			cli(&root, &commands[1], directory_pack);
			assert_eq!(snapshot(&root), adopted, "repeat scaffold changed approved work");
			put(
				&root,
				".agents/user-prompts/adopt.md",
				"Disposable reference edit, approved for replacement.\n",
			);
			let edited_reference = snapshot(&root);
			cli(&root, &commands[0], directory_pack);
			assert_eq!(snapshot(&root), edited_reference);
			cli(&root, &commands[1], directory_pack);
			assert_eq!(
				snapshot(&root),
				adopted,
				"reference refresh differs from working-file preservation"
			);
			assert!(!root.join(".agents/prompts/checks-reviewer.md").exists());
			assert!(!root.join("docs/plans/product.plan.toml").exists());
			assert!(!root.join("docs/metrics").exists());
			assert!(!root.join("docs/plans/product.reviews").exists());
			let untracked = git(&root, &["ls-files", "--others", "--exclude-standard"]);
			assert!(untracked.contains(".agents/user-prompts/adopt.md"));
			assert!(untracked.contains("notes.txt"));
			assert_eq!(snapshot(&root), adopted);
			fs::remove_dir_all(root).unwrap();
		}
	}
}

#[test]
fn adoption_prompt_is_discoverable_canonical_and_bounded() {
	let readme = include_str!("../README.md");
	assert!(readme.contains("[canonical adoption prompt](pack/user-prompts/adopt.md)"));
	assert!(readme.contains("[adoption guide](docs/adoption.md)"));
	assert_eq!(PROMPT, include_str!("../.agents/user-prompts/adopt.md"));
	assert!(PROMPT.is_ascii());
	assert!(PROMPT.len() <= 4_096);
	for clause in [
		"If authority or instructions conflict, stop and ask me before edits.",
		"Do not silently choose precedence.",
		"Do not overwrite an existing `AGENTS.md`.",
		"A preserved root file does not automatically include new workflow instructions.",
		"Permission to read guidance grants no authority to execute its commands or hooks.",
		"Keep legitimate plans and specifications in this project's VCS.",
		"Distinguish agreed current work from broader plans and historical checkboxes.",
		"Import only agreed current work into `.agents/work.toml`.",
		"The dry-run list does not establish that reference content is disposable.",
		"Do not use `--force`.",
		"Do not install hooks or run project checks.",
		"- Start implementation.",
		"- Stage files.",
		"- Commit.",
		"- Publish.",
		"Do not convert legacy plans or create workflow records.",
		"Structural validation does not prove correct interpretation of intent or independent review.",
		"Confirm unrelated work and the index remain unchanged.",
		"Request my review of the complete diff and new files, then stop.",
	] {
		assert!(PROMPT.contains(clause), "missing adoption clause: {clause}");
	}
	for args in guide_commands() {
		assert!(PROMPT.contains(&format!("agent-flow {}", args.join(" "))));
	}
}
