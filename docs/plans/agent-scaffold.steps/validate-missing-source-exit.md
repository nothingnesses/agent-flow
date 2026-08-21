### `validate-missing-source-exit`: make `validate` fail on an explicitly named input path that does not exist, instead of reporting success

THE PROBLEM. `validate --source <path>` prints a note and EXITS 0 when the path does not exist, so every criterion in this plan whose pass condition is "validate exits 0" also passes on a tree where the plan file is absent.

THE APPROACH. Treat an explicitly named path that does not exist as a violation rather than as nothing to do, and leave a DEFAULTED path that does not exist as the note-and-skip it is today.

HOW IT WAS FOUND. A specification writer measured it while running the rebuilt `Q-78` acceptance criteria against deliberately wrong implementations. It is a product defect and not a criterion defect, so it takes its own step rather than a note in either `Q-78` step.

THE MEASUREMENT, REPRODUCED IN THIS PASS. In an empty directory outside the repository:

```
agent-flow validate --source docs/plans/TEMPLATE.plan.toml
```

prints `no metrics log at docs/metrics/workflow.jsonl; nothing to validate` and `no source plan at docs/plans/TEMPLATE.plan.toml; nothing to validate` on stderr, prints NOTHING on stdout, and exits 0. `validate --plan docs/plans/nope.md` behaves the same way. The site is `src/main.rs:954` and the two sibling arms above and below it.

THE TOOL ALREADY HOLDS THE RULE THIS BREAKS, WHICH IS WHAT DECIDES THE STEP. The `--workflow` help text states it outright: "the check cannot run, and a check that did not run must not report success". `--workflow` honours it, and MEASURED, `validate --source <absent> --workflow` exits 1. The three input-path arms do not honour it. So this step is a consistency repair against a rule the product already publishes, rather than a new stance that needs a human ruling (Principle 1, Prefer the cleaner long-term architecture over the smallest diff).

WHAT COUNTS AS EXPLICIT, AND WHY THE SPLIT IS THERE. `--source` and `--plan` carry no default, so any value is one the user typed. `--metrics` carries a default derived from the source, so an absent DEFAULT metrics path is the ordinary state of a project that runs no instrumentation, and it must stay a note-and-skip under Principle 3, Safe on existing projects. An absent `--metrics` value the user typed is the same user error as the other two. The rule is therefore one rule with one condition, not three special cases: an explicitly supplied path that does not exist is a violation.

THE NARROWER ALTERNATIVE IS REJECTED, and it is recorded so a review round does not re-raise it. Fixing `--source` alone leaves `--plan` carrying the identical defect for every Markdown-primary project, and a rule that fires on one flag and not its sibling needs a ground that does not exist. Principle 5, Make illegal states unrepresentable, decides it: "the user named a file that is not there and the tool reported success" is the state being removed, and the flag it arrived through is not part of that state.

WHAT THIS COSTS AN EXISTING PROJECT, STATED RATHER THAN DISCOVERED. A scaffolded project whose `.agents/checks.toml` passes a path that has since moved flips from green to red on upgrade. That is the intended effect and not a regression: the green was false. The error names the path, so the fix is to correct the path or drop the flag. This is the one place the step knowingly trades against Principle 3, and it trades against it because the alternative is a check that reports success without running.

THIS STEP BLOCKS NOTHING IN THE `Q-78` PASS, AND THE ENUMERATION BEHIND THAT CLAIM COVERS ALL FIVE OF THE PASS'S STEPS. Three of the five pin the `<N> steps, <M> questions, valid` line on stdout as well as the exit code, precisely because of this defect: `plan-order-array-position`, `step-intent-encoding` and `ledger-order-citation-currency`. The fourth is this step. THE FIFTH IS `sidecar-status-opening-drift`, AND ITS CRITERION 8 READS A BARE EXIT 0 ON ONE COMMAND, which is the exact pattern this step exists to remove, inside the pass this step sits in. AN EARLIER FORM OF THIS PARAGRAPH NAMED THREE STEPS AND CONCLUDED ABOUT FIVE, which is a claim stated more generally than what was measured, and that is the pass's own named failure mode.

THE FIFTH STEP STILL DOES NOT DEPEND ON THE FIX, AND THE HUMAN ACCEPTED THE MISMATCH AS RESIDUAL RISK ON 2026-08-21, receipt `type:"decision"` `q_id:"Q-78-residuals"` in `docs/metrics/workflow.jsonl`. THE CONSEQUENCE THE HUMAN WEIGHED: that criterion requires a SECOND command, `validate --source <plan> --workflow`, to exit 0 as well. MEASURED in an empty directory outside the repository, that command exits 1 with `--workflow requested but no plan source resolved`. So an absent source fails the criterion on the `--workflow` arm and nothing wrong can ship.

This step is ordered ahead of them because every OTHER step in the plan still reads a bare exit 0 as proof, and each day the defect stands is another criterion written against a defective oracle (Principle 6, Ground decisions in evidence).

### Increment 1, `validate-missing-source-exit-inc1`: the exit-code repair

RISK CLASS `risky` (two consecutive clean review rounds). THE GROUND: the increment changes the exit code of a shipped subcommand that every scaffolded project's checks and CI read, so a project that names a stale path flips from passing to failing on upgrade. That is the "widely depended on" clause of the `AGENTS.md` test, and the flip reaches every downstream project at once rather than this repository alone. The diff is small and one revert undoes it here, which argues the other way, and the downstream reach decides it. It is the opposite of the plan's worked `low_risk` example at `test-tmpdir-repo-assumption.md`, which is confined to `#[cfg(test)]` code and ships nothing.

WHAT IT DOES. At `src/main.rs:954` and its two sibling arms, an explicitly supplied path that does not exist pushes a problem into the existing `problems` vector instead of printing a note, so it flows through the exit path the command already owns. A `--metrics` path that came from the default keeps the note and the skip. The `--help` text of all three flags states the new behaviour, because the current `--metrics` help documents the defaulting rule and now has to document the split.

THE MESSAGES. Each keeps its current wording and takes an error prefix, so an existing reader recognises the line:

```
error: no source plan at <path>
error: no plan at <path>
error: no metrics log at <path>
```

`validate` exits 1 on any of the three, through the same path as every other violation.

ACCEPTANCE, EACH EXECUTABLE.

1. RED CONTROL, RECORDED BEFORE THE CHANGE. In an empty directory outside the repository, `agent-flow validate --source docs/plans/TEMPLATE.plan.toml` exits 0 and prints nothing on stdout. The outcome quotes that exit code and the two stderr lines, because a criterion that only shows the fixed state does not show that the fix was needed. MEASURED at authoring time, the exit code is 0.

2. AN ABSENT EXPLICIT `--source` FAILS. In an empty directory outside the repository:

```
./target/debug/agent-flow validate --source docs/plans/TEMPLATE.plan.toml
```

Pass: stderr carries a line ending `no source plan at docs/plans/TEMPLATE.plan.toml`, stdout is empty, and the exit status is 1.

3. AN ABSENT EXPLICIT `--plan` FAILS, AND IT IS RUN SEPARATELY. In the same directory:

```
./target/debug/agent-flow validate --plan docs/plans/nope.md
```

Pass: stderr carries a line ending `no plan at docs/plans/nope.md`, stdout is empty, and the exit status is 1. This command is given on its own rather than as a substitution into criterion 2, because a reader who substitutes once proves one flag and the two arms are two pieces of code.

4. AN ABSENT EXPLICIT `--metrics` FAILS, AND IT IS RUN SEPARATELY.

```
./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/nope.jsonl
```

Pass: stderr carries a line ending `no metrics log at docs/metrics/nope.jsonl` and the exit status is 1, run from the repository root where the `--source` path DOES exist, so the failure is attributable to the metrics path alone.

THEN THE USER TYPES THE DEFAULT PATH, AND THAT COMMAND IS GIVEN SEPARATELY BECAUSE IT IS WHAT TYPES `--metrics` AS EXPLICIT. Scaffold into an empty directory outside the repository, create no metrics log, and run:

```
./target/debug/agent-flow validate --source docs/plans/TEMPLATE.plan.toml --metrics docs/metrics/workflow.jsonl
```

Pass: stderr carries a line ending `no metrics log at docs/metrics/workflow.jsonl` and the exit status is 1. The path typed here is byte-identical to the DERIVED default, which criterion 5 runs in the same directory and requires to exit 0, so the two commands differ in one thing only: whether the user supplied the flag.

WHY THIS COMMAND EXISTS, AND IT IS THE PREMISE HALF OF THIS STEP'S OWN GROUND. THE PREMISE: explicitness is whether the user SUPPLIED the flag, which the code reads as `args.metrics.is_some()` (`metrics: Option<PathBuf>`, `src/main.rs`). THE CONSEQUENCE: an absent explicit `--metrics` fails and an absent defaulted `--metrics` skips. An implementation that decides explicitness by COMPARING the resolved path against the derived default falsifies the premise while the consequence still holds for every path the other criteria supply. Criterion 4's first command names `docs/metrics/nope.jsonl`, which differs from the default, so it fails there. Criterion 5 supplies no flag at all, so it skips there. That implementation passes criteria 2, 3, 4 and 5 as they stood before this command, and it reports success on the command above, which is the state Principle 5 removes. MEASURED before the change, the command above and criterion 5's command both print `docs/plans/TEMPLATE.plan.toml: 1 steps, 0 questions, valid` and exit 0, so the pair detects the condition rather than merely staying silent.

5. AN ABSENT DEFAULTED `--metrics` STILL SKIPS, WHICH IS THE HALF THAT KEEPS THE CHANGE SAFE. Scaffold into an empty directory outside the repository, do not create a metrics log, then:

```
./target/debug/agent-flow scaffold --output-dir . --write --vcs none
./target/debug/agent-flow validate --source docs/plans/TEMPLATE.plan.toml
```

Pass: stdout carries exactly `docs/plans/TEMPLATE.plan.toml: 1 steps, 0 questions, valid` and the exit status is 0, with the metrics note still on stderr. THIS IS THE CRITERION THAT CATCHES THE OVER-WIDE FIX. An implementation that treats the defaulted metrics path as explicit breaks every project that runs no instrumentation, and it passes criteria 2, 3 and 4 while doing so.

6. THE LIVE PLAN IS UNAFFECTED. From the repository root, `./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --metrics docs/metrics/workflow.jsonl` prints its `<N> steps, <M> questions, valid` line on stdout and exits 0, and `./target/debug/agent-flow validate --source docs/plans/agent-scaffold.plan.toml --workflow` prints `workflow invariants hold` and exits 0.

7. `--workflow` KEEPS ITS OWN BEHAVIOUR. `validate --source <absent> --workflow` still exits 1, and its stderr still carries `--workflow requested but no plan source resolved`. The new error joins that message rather than replacing it, so the diagnostic that already worked is not lost.

8. EACH BRANCH IS PINNED IN THE SUITE. The integration tests gain one test per branch: an absent explicit `--source`, an absent explicit `--plan`, an absent explicit `--metrics` naming a path that is NOT the default, an absent explicit `--metrics` naming a path that IS byte-identical to the default, and an absent DEFAULTED `--metrics` that still exits 0. FIVE TESTS, because five branches. The fourth and the fifth are a pair over the same path string, and only the flag differs, so together they pin explicitness to `is_some()` rather than to a path comparison. The fifth is also the one that fails if the fix is written too wide. Verify with `grep -c 'fn .*missing_.*_path' tests/`, whose count the outcome records. A criterion that only runs by hand does not survive the increment, which is why the pair lives in the suite as well as in criteria 4 and 5.

9. THE HELP TEXT STATES THE RULE. `./target/debug/agent-flow validate --help` describes, for each of the three flags, that a path the user supplies must exist. `grep -c -F -- 'must exist' <(./target/debug/agent-flow validate --help)` prints at least `3`.

10. THE CHANGED PATH SET. `git diff --name-only` lists `src/main.rs` and the integration test file criterion 8 adds to, and nothing else. No file under `docs/plans/` appears, and `pack/` does not appear, because the pack ships no `validate` invocation that names a path this rule newly rejects. If that turns out to be false, the pack file joins the set and the outcome says which and why.

11. THE SUITE, THE VALIDATORS AND ASCII. `cargo test` passes. `cargo clippy --all-targets -- -D warnings` exits 0. `cargo run -- render --check --strict docs/plans/agent-scaffold.plan.toml` prints `up to date` and exits 0. `LC_ALL=C grep -cP '[^\t\x20-\x7e]' <file>` prints `0` for every changed file.

### NOT IN SCOPE, NAMED SO IT IS NOT DRAWN IN

- EVERY OTHER SUBCOMMAND THAT SKIPS A MISSING PATH. `status` documents a best-effort stance in its own help text and `next` follows it. Whether that stance is right is a separate question, and this step neither answers it nor changes either command.
- THE `--workflow` REFUSAL RULES. They already implement the rule this step restores elsewhere, and they are left exactly as they are.
- RE-AUDITING THE PLAN'S OTHER "VALIDATE EXITS 0" CRITERIA. The `Q-78` steps already pin their stdout lines. The rest of the plan's criteria are not re-read here, and that sweep, if it is wanted, is its own step.
