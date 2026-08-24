# Q-78 post-escalation round 4 Claude review

## Scope and method

I reviewed `step-intent-encoding-inc1` only, on `plan/q78-design-pass` at tip `6da3e8e`, excluding every brief. I read `AGENTS.md`, the ledger's `RESUME HERE` paragraph (`docs/plans/agent-scaffold.ledger.md:535-543`), the round-3 triage, the round-3 fix brief, and the increment-1 block of `docs/plans/agent-scaffold.steps/step-intent-encoding.md` (lines 59-507) plus the shared RULES it depends on. I did not read the GPT round-4 report. My scratch child is `/tmp/claude-1000/-home-jessea-Documents-projects-agent-scaffold/2fed83bd-4a13-402b-9e76-143356c0d130/scratchpad/q78-foreclosure-r4-claude`; I used no bare `/tmp` path and no wildcard deletion.

Lenses: adoption, executability and fix verification, direnv, GNU grep.

Every command below ran with GNU grep 3.12 (`/nix/store/gn94gpcp5q08x4v6g8mvw8v4r65rcjzk-gnugrep-3.12/bin/grep`), pinned by absolute path because the interactive shell's `grep` is a function resolving to `ugrep 7.5.0`, whose regex handling differs.

**ENVIRONMENT LIMITATION, STATED PLAINLY.** The direnv toolchain is NOT reachable from this review worktree: `direnv`'s store path (`/nix/store/gv6dc61q6sprcm3hr69yxnwjn3gwcvsc-direnv-2.37.1/bin`) is on `PATH` but does not exist on disk, and `nix`, `cargo` and `rustc` are all absent from `PATH`. I therefore could NOT run `cargo test`, `cargo clippy`, `agent-flow validate`, `agent-flow render --check` or any built binary, and I make no claim about the suite or the validators. This is proportionate rather than fatal for this artifact: the object under review is a plan sidecar whose criteria are claims about code that does not exist yet plus claims about code that does, so its evidence is `file:line` citations and command output over the existing tree. Everything I assert below is backed by a command or a citation I ran or read in this worktree, including against clap's own vendored source. I flag it so the triager does not read a green gate into this report.

## Independent verification of R3-1

**R3-1 IS GENUINELY CLOSED.** I verified the fix (`step-intent-encoding.md:320-368`) against the production code rather than against the fix brief's description of it.

The defect R3-1 named was that the all-state seam starts below the pending transfer. GNU grep confirms the seam count the fix reasons about:

```
$ grep -n "LoopFacts {" src/next.rs
649:struct LoopFacts {
770:	let facts = LoopFacts {
802:		let facts = LoopFacts {
836:	let facts = LoopFacts {
```

There are exactly three `LoopFacts` construction sites: `build_pending_loop` (`src/next.rs:770`), the in-progress no-rounds early return that yields `AwaitingFirstReview` (`:802`), and the in-progress main path that yields every other in-progress state (`:836`). Before the fix, criterion 7's matrices entered only through `:802` and `:836` and the seam test at `:370` supplied `LoopFacts` directly, so `:770` was unguarded. The two new tests enter through `steps_from_toml` and reach `:770`, which closes the last uncovered site. The transfer chain TOML -> `Step` -> `steps_from_toml` -> `StepInfo` -> `LoopFacts` (all three sites) -> `build_context` -> both renderers now has an oracle at every link except the settled Markdown arm (R3-3).

Each specified expectation reproduces against the code:

- **Both fixtures reach the intended state.** `StepPhase::is_pending()` is `matches!(self, StepPhase::NotStarted | StepPhase::Next)` (`src/next.rs:499-501`) and `is_terminal()` covers `Deferred` (`:505-510`). So for the `ReadyToPlan` fixture, `status = "next"` maps through `phase_from_toml_status` (`:577`) to `StepPhase::Next`, is pending, has no blockers, and `select_active_loop`'s second arm selects it (`:720-726`). For the `Blocked` fixture, the sidecar's stated reason at `:343` is exactly right and both halves hold: `dep` being `deferred` is not pending, so it cannot pre-empt through the ready arm; and `is_complete(dep)` is false (`:753-758`), so `blockers_met(a)` fails and the third arm builds the blocked loop with `unmet_blockers = ["dep"]` (`:727-732`).
- **The complete JSON key sets are correct.** `build_context` (`src/next.rs:993-1021`) always inserts `ledger` and `isolation_tier`, adds nothing for `ReadyToPlan`, and adds `blocked_by` = `facts.blockers.join(", ")` for `Blocked`. With the two intent slots that gives exactly the four keys pinned at `:326-331` and exactly the five keys pinned at `:349-355`, and `BTreeMap` ordering puts `blocked_by` between `approach` and `isolation_tier`, which is the order the fix wrote.
- **The two fixed non-intent values are emittable, unlike the settled `FR1-4` literals.** `ledger` and `isolation_tier` come straight from `LoopContext` (`src/next.rs:640-644`), which a test fills through `NextInputs`, so `ledger.md` and `worktree` are reachable. The new tests use no findings-path slot, so the fix adds no new instance of the settled false-refusal.
- **The human shape matches the renderer.** `render_active_loop` emits `  context:\n` then one `    {key}: {value}\n` per entry (`src/next.rs:1219-1222`), which is the two-space/four-space frame the fix's blocks at `:334-341` and `:357-366` use, with the intent slots re-shaped per the `:112` display rule.
- **The red control at `:368` discriminates.** Nulling only `build_pending_loop`'s two fields leaves `:802` and `:836` untouched, so `next_json_preserves_the_parser_value_matrix` and `human_next_preserves_the_display_matrix` (which run `AwaitingFirstReview` and `AwaitingFixes`) stay green, and `build_context_carries_intent_in_every_loop_state` supplies `LoopFacts` directly so it also stays green. Only the two new tests fail. The control isolates exactly the seam it claims to.

## Independent verification of R3-2

**R3-2 IS GENUINELY CLOSED.** I verified the replacement oracle (`step-intent-encoding.md:454-463`) against clap's own source, not from memory.

The defect R3-2 named was that `grep -cE '^  [a-z]+ '` over the `Commands:` block stops at a hyphen, so a hyphenated eighth subcommand still counts 8. The replacement drops the transcript entirely and reads Clap's model:

- **The expected vector matches the declaration order.** `enum Command` declares `Scaffold, Validate, Status, Next, Checks, Render, Audit` (`src/main.rs:411-426`), which kebab-cases to the first seven names at `:458`.
- **`get_subcommands()` really is declaration order.** In the vendored clap builder source (`/nix/store/1q1l6c7wicr4kg41p11qdsqr0ylagdhj-cargo-package-clap_builder-4.5.46/src/builder/command.rs:3884-3886`) it is `self.subcommands.iter()`, an unsorted `Vec` walk.
- **`render_long_help()` really does materialise `help`, and appends it last.** `pub fn render_long_help(&mut self)` opens with `self._build_self(false)` (`command.rs:1003-1004`), and `_check_help_and_version` builds the generated subcommand and finishes with `self.subcommands.push(help_subcmd)` (`command.rs:4796-4834`). So the eighth name is `help` and it is last, exactly as `:458` states. `render_long_help` carries no `#[must_use]` attribute (`command.rs:990-1003`) and `StyledStr` is a plain `pub struct StyledStr(String)` with no `#[must_use]` (`styled_str.rs:23-24`), so calling it for its side effect does not trip `-D warnings`.
- **`CommandFactory` is available and the test can see the private types.** `clap = { version = "4", features = ["derive"] }` (`Cargo.toml:14`), `Cli` derives `Parser` (`src/main.rs:397-407`), and `src/main.rs` already carries a `mod tests` (`:2356`) with in-crate visibility.
- **The red control discriminates.** A unit `IntentQuery` variant on a `#[derive(Subcommand)]` enum is exposed by clap's default kebab-case rename as `intent-query`, which makes the collected vector nine names and fails the exact comparison. The old selector counted 8 on the same mutation; the new one cannot.

The store copy is clap_builder 4.5.46 while `Cargo.lock:194-196` pins clap 4.6.1. I could not read 4.6.1 itself, so I state the version gap rather than hide it; the help-subcommand construction path above is long-standing clap 4.x behaviour and nothing in the fix depends on a 4.6-only API.

Housekeeping around both fixes also holds: the authoritative list at `:452` gained both new `next` test names and the Clap test name and now enumerates 13 names, the heading was widened to "PROJECTION AND CLI-SURFACE CONTRACT", and increment 3's retention clause was widened to match, so the two copies did not drift.

## Findings

One finding. It is `low` and, under the foreclosure decision's clean bar, class 2.

### C4-1 (`low`, class 2, owner `step-intent-encoding-inc1`): increment 1 declares a Markdown-substrate `status --step` state that no increment-1 criterion reaches

**The stated contract.** Increment 1's `status` block requires, for a field the substrate does not carry, the human line `  > (not recorded)` and, on JSON, `found: true` with a `null` value (`step-intent-encoding.md:144`). It then rules explicitly on the distinction: "This keeps the documented best-effort stance while distinguishing an unknown step from a known Markdown step whose intent is not recorded" (`:150`). Criterion 8 heads itself "`status --step` ANSWERS EVERY DECLARED DATA STATE" (`:376`).

**The gap.** Every `status --step` run inside increment 1 (lines 59-507) is a TOML `--source` run. GNU grep over the whole sidecar:

```
$ grep -n -- "status --source\|status --plan" docs/plans/agent-scaffold.steps/step-intent-encoding.md
154:...`status --source <plan> --plan /nonexistent.md`...        <- prose about today's behaviour, not a criterion
379:./target/debug/agent-flow status --source <matrix.plan.toml> --step a
399:./target/debug/agent-flow status --source <matrix.plan.toml> --step a --json
431:./target/debug/agent-flow status --source good.plan.toml --step nope
437:./target/debug/agent-flow status --source no-intent.plan.toml --step a
443:./target/debug/agent-flow status --source good.plan.toml --step a --resume
580, 628, 671, 702: ... --source "$PLAN" ...                    <- increments 2a-2f batch scripts
905, 906: ... --source docs/plans/TEMPLATE.plan.toml ...        <- increment 3
992:./target/debug/agent-flow status --plan docs/plans/agent-scaffold.md --step core-assets
```

The only `--plan` run of `status --step` in the whole step is `:992`, and it sits in increment 3 criterion 12 (`:989-993`), which says of itself: "What the criterion holds is increment 1's sentence". The partial fixtures at `:409-427`, the no-intent fixture at `:437` and the unknown-slug fixture at `:431` are all TOML sources, so none of them separates the two outcomes on a Markdown-declared slug.

**What a wrong implementation ships.** An implementation that resolves `--step` only against a parsed TOML source, and answers `step: <slug> not in this plan` with `found: false` for a slug the Markdown Roadmap declares, satisfies every increment-1 criterion: the eight-row matrix, both partial-state fixtures, `no-intent.plan.toml`, the unknown-slug case, the `--resume` conflict, the two field-and-surface red mutations and the three shared-helper red mutations are all TOML-source runs. It contradicts `:150` directly. The case is a real product input, not a hypothetical: `status` reads the Markdown `--plan` whenever no TOML-primary `--source` resolves (`src/main.rs:497-502`), and `steps_from_markdown` is the parallel normaliser that yields slug-bearing steps with no intent column (`src/next.rs:552-567`). The defect would survive increment 1's converged loop and all six risky backfill loops (2a-2f, none of which runs `status --step` against a Markdown source) and be caught only at increment 3.

**Why class 2 and not class 1.** The violated statement is an explicit prose expectation in the increment's `status` block, not a numbered RULE, a risk ground or a cited Principle, and a second guard does exist two increments later. This is the same classification the round-3 triage applied to R3-3 for the mirror gap on `next` (`q78-foreclosure-r3-triage.md`, E3) and the round-2 triage applied to R2-1. `status` is a report surface, not the instruction surface that made FR1-2 class 1. Severity is `low`: no data is corrupted and the mistake is one an ordinary unified-step-list implementation avoids for free; what is missing is the requirement that it do so.

**This is not R3-3 and not a re-raise.** R3-3 is the Markdown boundary on `next`, and the round-3 triage's own words separate them: "A correct status test cannot close this: it exercises `status`, not `next`." Its prescribed correction is a Markdown `next --plan` fixture and names no `status` obligation. The `status` side has not been raised in any round of this series.

**Smallest correction.** Add one Markdown fixture to increment 1 criterion 8: run `status --step` against a `--plan` Markdown plan that declares slug `a`, assert the exact five human lines `step: a`, `problem:`, `  > (not recorded)`, `approach:`, `  > (not recorded)` at exit 0, and assert `found: true` with both fields `null` on `--json`; add a red control that resolves `--step` against the TOML source only and must fail it on `found`. No changed-path-set edit is needed, because the fixture is a scratch plan exactly like the criterion-2 matrix. The alternative, if the deferral is deliberate, is to say so in increment 1 and narrow criterion 8's "EVERY DECLARED DATA STATE" heading to the TOML substrate, naming increment 3 criterion 12 as where the Markdown state is held.

## Severities I did not find

- **No `critical` findings.**
- **No `high` findings.**
- **No `medium` findings.** In particular I looked for, and did not find, a class-1 hole: the intent transfer chain now has an oracle at every `LoopFacts` construction site, the `build_context` state axis is exhaustive by construction, and the three display surfaces each carry their own complete matrix plus red controls.
- **One `low` finding**, `C4-1` above.

## Other checks that passed, recorded so they are not re-run

- **The generated projection is current for this step.** I sliced the 1030 sidecar lines out of `docs/plans/agent-scaffold.md` starting at the line matching the sidecar's first line (found at `agent-scaffold.md:3565`) and diffed: zero difference. The R3 fix regenerated the view.
- **Criterion 10's sizing script is sound on the live tree.** `grep -c '^\[\[step\]\]'` prints 105, `grep -c '^slug = '` prints 105, and every `slug = ` line sits under a `[[step]]` table (checked with an awk table-context census), so the `sed` extraction cannot pick up a question, increment or waiver id. K = 6 and S = 18 by the stated rule, and `grep -c 'id = "step-intent-encoding-inc2'` prints 6, so the declared-loops-versus-manifest-batches comparison at `:480-484` passes today.
- **The leading-heading reproduction at `:107-109` reproduces exactly.** The loop prints `docs/plans/agent-scaffold.steps/core-assets.md` and nothing else, and that file's first `#` line is line 9, as the sidecar states.
- **The render-fixture claims are grounded in the real fixture.** `src/plan/testdata/render-fixture.plan.toml` has seven `[[step]]` blocks (alpha, beta, gamma, delta, zeta, epsilon, eta), all seven sidecars exist, and criterion 6's quoted `beta` body is byte-identical to the committed `beta.md` body.
- **The message and summary formats the criteria pin are the real ones.** `validate`'s clean-source line is `"{}: {} steps, {} questions, valid"` (`src/main.rs:936`), so criterion 2's expected `1 steps, 0 questions, valid` is right including the unpluralised `1 steps`; source problems are prefixed `"{}: {}"` (`src/main.rs:944-946`), matching criterion 3's expected lines; and a missing metrics log is a stderr note, not a problem (`src/main.rs:915`), so criterion 2's bare `validate --source <file>` really does exit 0.
- **The schema change follows the existing convention.** `Step` already carries `provenance` as `#[serde(default, skip_serializing_if = "Option::is_none")] pub(crate) provenance: Option<Provenance>` with the same "deserialises to `None` and re-serialises to nothing" doc phrasing (`src/plan/source.rs:149-152`), so the increment's schema paragraph adopts a shape the file already uses. Criterion 1's `grep -c 'problem: Option<String>'` still matches the `pub(crate) problem: Option<String>,` line the repo's style would produce.
- **Criterion 12's ASCII sweep is executable here.** This GNU grep has PCRE support, so `grep -cP '[^\t\x20-\x7e]'` runs rather than erroring out.
- **`conflicts_with = "resume"` names a real arg id.** `StatusArgs` declares `resume: bool` with `#[arg(long)]` (`src/main.rs:509-511`), so the id is `resume`.

## Settled findings I did not re-raise

I found no changed evidence against any of them, so `FR1-1`, `FR1-4`, `R2-1`, `R2-2`, `R3-3`, `R3-4`, the accepted residuals `GB-4`, `GB-9`, `F2` and `F3`, and the dismissed `PE1C-3` all stand as settled. I confirmed in passing that `FR1-4`'s literals at `:283-300` are still unemittable (`findings_naming::review_findings_path` hard-codes the `docs/plans/<task>.reviews` prefix, `src/findings_naming.rs:31-72`) and that R3-4's declaration-site sentence is still at `:156-158` and `:492`; both are permitted class-2 findings the round-1 and round-3 fix briefs deliberately left in place, and neither is re-raised here. No waiver is claimed or used.
