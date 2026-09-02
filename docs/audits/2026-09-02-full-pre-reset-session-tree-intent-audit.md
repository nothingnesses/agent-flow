# Full pre-reset session-tree intent audit

Final audit of the full pre-reset Pi session tree. This record preserves the conclusions in a self-contained, sanitised form.

## Scope and boundary

This audit covers every session record before the human selected the minimal reset.

The reset boundary is message `095858ed` at JSONL line 62,326 on 2026-08-30T13:34:15.841Z.

The external source was a local Pi session JSONL, 136,637,987 bytes, SHA-256 `99dd7feb80bca0b92c767cf49faac1a989cbc9da9502f6c048d1a3035d11d2a1`.

## Method

The audit classified the full pre-reset user-side corpus, then separated likely human intent from wrappers and control traffic.

It normalised whitespace and case, removed duplicates, removed pre-session branch carry-over, and merged direct user texts with question-tool answers. It then mapped every retained intent id across three independent analyst passes and reconciled the union for completeness.

This report records the final counts, findings, and dispositions. It does not require any ignored working files to interpret or support its conclusions.

## Corpus counts

Before the reset decision, the source contained 62,325 records.

It contained 2,918 `user` records, classified first as:

- 1,921 task notifications
- 156 session-control prompts
- 95 command wrappers
- 90 local-command wrappers
- 17 interruption markers
- 4 editor wrappers
- 590 other user messages
- 45 short responses

Whitespace and case normalisation reduced 635 likely human user messages to 320 unique texts.

Seventy-five unique texts existed only outside the reset-decision ancestry. Seventy-three belonged to copied CV and interview branches. The two project texts were `a97ab504` and `04035a56`.

The audit also corrected the earlier omission of legacy `AskUserQuestion` results. The prior audit ignored 646 such results because it recognised only the later lowercase tool name.

After duplicate and pre-session removal, the combined intent index contained:

- 245 unique direct user texts
- 306 unique question-tool results
- 551 total intent records

Seven question results and two direct texts contained branch-exclusive project intent.

Three independent analysts mapped all 551 ids. The combined map contained 551 unique ids with no missing or extra ids.

Final classification of the 551 intent records:

- 297 project intent
- 244 process control
- 10 other repositories

## Main correction to the earlier audit

The earlier audit found eleven broad candidates, but it omitted most question-tool answers and became stale after two later changes.

Safe multiline work prose shipped in `5218d0b1`.

The standalone review prompt shipped in `60aa294e`.

The earlier audit also under-described the purpose of metrics. The full tree confirms that the data was meant to support evaluation and possible ablation, as the human recalled.

## Metrics intent and use

Several direct messages state the purpose:

- `3b4c53b2` asked why metrics existed and whether the data matched that purpose
- `5d8fa97d` required dogfood use of the metrics
- `14c4c590` asked for broad data with one source of truth
- `acc79493` asked whether statistical methods can make the process rigorous
- `de57f73e` asked how evidence can distinguish a bad cap from genuine defects
- `fa60e524` commissioned an objective workflow and product audit
- `76cf71e9` defined success as correct requirement delivery over time and named gaming, human waits, correctness oracles, and artificial requirements

The historical `pack/instrument.md` stated the narrower mechanical goal. Calibration metrics were meant to tune review-round constants from real use.

The intended feedback path was:

1. Collect evidence about workflow activity and results
2. Test whether code, prompts, and workflow rules help
3. Diagnose weak or costly parts
4. Remove or redesign parts that do not justify their cost

The data was used. The July calibration analysis used round transitions and clean streaks. The 13 August audit used round data, git history, review files, and independent agents. The 14 August causation investigation re-tested dates and candidate causes. Later Q-86 work used the same evidence to compare bounded-convergence designs.

The feedback path therefore closed once at large scale. It did not become a repeatable evaluation system.

## Historical workflow log, measured at the preserved pre-reset tree

At `archive/pre-minimal-reset`, `docs/metrics/workflow.jsonl` contained 509 records:

- 339 review rounds
- 145 human decision receipts
- 20 escalations
- 4 intake records
- 1 dismissal recheck

The 339 rounds contained 200 `new_valid` outcomes and 139 `clean` outcomes, with 1,111 round-level valid findings.

Reviewer arrays existed on 277 rounds. They recorded role, model, harness, raw finding count, and valid finding count.

Timestamps existed on 455 of 509 records. Fifty-four records had no timestamp.

The log recorded phase, risk class, clean streak, finding count, severity, and whether the artefact changed. It captured process events and review yield.

It did not record the outcome and cost measures needed for a broad evaluation system, including duration, human wait, token use, model cost, prompt version, acceptance-test result, coverage, mutation result, field defects, or ablation results.

Decision receipts and waivers later became control evidence. They did not measure development effectiveness.

## Why the metrics system still failed

The intent was sound, but the implementation mixed three duties:

- calibration data
- active workflow state
- evidence for enforcement and completion

That mix created a conflict. The actors under measurement also authored the records that certified their process.

`validate --workflow` checked log arithmetic but could not prove that a review occurred. Two hand-written clean records could satisfy it.

Many fields had no decision rule or consumer. The 13 August audit reported that over half of field values were validated but never read.

The schema also lacked the measures needed for its wider purpose. It could compare reviewer yield, but not development success against token cost.

The reset was correct to remove that mechanism. It did not reject empirical evaluation as a goal.

## Mutation testing and test robustness

`a02a7005` proposed a test-first phase, property tests, end-to-end flows, and mutation testing for generated tests. The human selected a design pass in `158aaa48`.

The human later selected a separate test-author role in `9684c5e5`. Two design documents explored test and mutation modules.

The planned mutation module was optional, depended on the test-driven and checks modules, ran once after green review rather than in every round, used a changed-code diff, carried a time budget and survivor threshold, and named tools such as `cargo-mutants`.

The plan created a `mutation` step, but the step never started. On 30 July, the human selected `Record it, do not schedule it` for the cadence gap. The reset later removed the plan that held the deferred step. That history means deferred, not rejected on merit.

Formal mutation testing did run once as an audit experiment. The 13 August audit ran `cargo-mutants` on `src/workflow.rs` and `src/plan/source.rs`. That experiment killed 144 of 150 viable mutants, or 96 percent. It covered two historical files, not the full current repository.

Current enforcement remained absent at audit time:

- `src/checks.rs` parsed `test` and `mutation` kinds but skipped both
- `budget` and `threshold` were parsed but unused
- `pack/checks.toml` documented only commented reserved examples
- `flake.nix` included neither `cargo-mutants` nor `cargo-machete`
- CI ran no mutation job

Recent reviews used manual fault probes. Those probes exercised selected paths, but they did not form a mutation programme.

Current disposition: mutation testing needs a fresh human decision. The old module design is evidence, not current authority.

## Meaningful test coverage

The quality gate at audit time ran 429 Rust unit tests and all integration binaries, plus Clippy, formatting, repository checks, work validation, actionlint, and attribution checks.

Tests covered many parser, projection, path, and scaffold boundaries. Review prompts required evidence that tests exercised the claimed path.

The repository had no coverage gate, fuzz target, property-test framework, or mutation gate. Test count alone did not measure path significance.

The historical mutation result gave strong evidence for two old modules. It did not give a whole-tree or current changed-code guarantee.

Current disposition: a meaningful-path test strategy remained unresolved.

## Code value and ablation

`8dd819e7` asked for deterministic and statistical evidence that code earns its maintenance cost, including tests, fuzzing, mutation, and periodic review.

The current `agent-flow audit` command was only a foothold. It ran the source-suppression and foreign-function-interface scan.

Its rustc dead-code producer did not run. Its `cargo-machete` producer did not run.

The old plan designed a deletion experiment with `cargo-mutants` body nulls and item removal, followed by build and test. That experiment never became product behaviour. The old plan also forbade automatic deletion.

Current disposition: the broad code-value request remained pending.

## Prompt and workflow effectiveness

The repository tests at audit time covered prompt presence, prompt drift, byte limits, and selected contract clauses. These were structural checks.

No controlled experiment compared prompt variants on the same task set. No record linked prompt version to acceptance success, rework, time, or token cost.

The 13 August audit evaluated the dogfood workflow on this repository. It did not establish general workflow effectiveness across projects.

The audit found one plausible prompt effect. A 26 July reviewer-evidence rule coincided with a large rise in review prose and findings. The 14 August causation report rated that link at moderate confidence and proposed a matched differential prompt test, but that test never ran.

The old Q-58 design specified a controlled output ablation for `next` with fixed variants, held-out states, token cost, model replication, and a deterministic oracle. The human later reopened that experiment in `4960a7dd`. The reset occurred before the experiment ran.

Current disposition: prompt and workflow outcome evaluation remained pending.

## Static limits after the reset

The reset added byte, step, output, and pass limits after direct evidence of unbounded growth, including:

- `next` output at 765,503 bytes
- active plan state near 2.9 MiB
- 92.2 percent documentation-only commits in the measured period
- hundreds of review files and process-only commits

These limits act as recurrence circuit breakers. They prevent the known failure mode from returning at the same scale.

They do not measure usefulness, correctness, or token efficiency. They count bytes rather than model tokens. No experiment established 4 KiB, 8 KiB, 16 KiB, or 64 KiB as optimal thresholds.

Current disposition: the limits are justified as upper bounds, not as validated performance targets.

## Cluster status

### Shipped or retained

- core scaffold, write safety, custom packs, Git setup, principle selection, and the TUI
- deterministic lint and format checks with temporary check worktrees
- bounded `.agents/work.toml`, truthful `next`, validation, and paragraph-safe prose
- standalone whole-tree and diff review prompts
- independent product review, conditional triage, one fix, and one verification
- human scope and merge authority
- safe path boundaries and current repository attribution checks
- the `agent-flow` crate and repository rename
- durable Git history and the two 13 August audit records

### Superseded by the reset

- active plan trees, ledgers, review directories, and JSONL round logs
- plan review and repeated convergence rounds
- self-certified review evidence and decision receipts
- product-owned agent launch and model orchestration
- compaction and resume state machines in the default pack
- the Mealy workflow driver and ready-frontier scheduler

### Pending or unresolved

- a bounded mutation-testing policy
- a meaningful-path test strategy
- the broader code-value and deletion experiment
- prompt and workflow outcome benchmarks
- token and cost measurement tied to task outcomes
- a provider-neutral external sandbox runner contract

Historical deferred ideas also included custom-pack TUI authoring and workflow visualisation. No current request revived them.

## Current residue found during the audit

The audit found three current accuracy issues. It created no task for them.

1. `src/main.rs` still told users about `.agents/user-prompts/audit.md`. The reset deleted that prompt from the built-in pack.
2. `flake.nix` still used the older general workflow description. `Cargo.toml` and the GitHub description used the bounded description.
3. `src/checks.rs` retained skipped `test` and `mutation` schema plus fields promised to later modules. No current task owned those promises.

The historical corpus also recorded a deferred `status --resume --json` concern and no explicit salvage-test verdict. Those needed reproduction before any product action.

## Limits

Many messages contained several requests. Cluster status is therefore more reliable than raw disposition counts.

This audit is about one repository and one pre-reset session tree. It does not create new product scope by itself.

No true escape rate was available because there was no field defect data. Agent time and token cost were not recorded. The quality of any residual-defect estimate was limited by the available reviewer data.

## Conclusions

The full tree adds no hidden requirement that overrides the reset. Its branch-exclusive project intent reinforces structured data, isolation, dogfood use, and careful human decisions.

The main omission in the earlier audit was not an unseen branch. It was the legacy question-tool corpus and its decisions.

The human's metrics recollection was correct. The data existed to evaluate the process and support changes or ablation.

That programme produced useful evidence and contributed to the reset. It also became part of the process burden and lacked the outcome and cost fields needed for a stable evaluation system.

Mutation testing was designed and used once for historical audit evidence. It was never integrated into current delivery or CI.

Future evaluation should preserve the empirical goal without per-round proof state. A suitable design would run periodically in scratch against fixed tasks and independent oracles.

No old request becomes a product task from this audit alone.
