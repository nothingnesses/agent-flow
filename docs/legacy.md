# Legacy compatibility and audit

This reference supports projects that already use legacy interfaces. It is not an adoption or conversion procedure. For the minimal workflow, use the [adoption guide](adoption.md).

Existing project plans remain legitimate project material. Adoption does not authorise their conversion or deletion.

## Mode selection

An existing `.agents/work.toml` selects bounded mode by default. Explicit legacy inputs select compatibility mode for these commands:

- `validate`, with a legacy plan or metrics input. A workflow check also selects compatibility mode.
- `status`, with a legacy plan or metrics input. Resume flags also select compatibility mode.
- `next`, with an explicit legacy plan source.

Without `.agents/work.toml`, all three retain legacy fallback behaviour. Legacy `next` no longer emits free-form ledger or resume text.

## Structured plans and render

A legacy plan contains a `<task>.plan.toml` skeleton and Markdown sidecars. The TOML describes these structured regions:

- Roadmap steps.
- The question queue.
- Principles.

Sidecars hold the remaining prose. `render` inserts sidecars verbatim into the generated `<task>.md` projection. The source consists of TOML and sidecars, not the generated Markdown.

```sh
agent-flow render docs/plans/my-task.plan.toml
agent-flow render --check docs/plans/my-task.plan.toml
agent-flow render --check --strict docs/plans/my-task.plan.toml
```

A schema violation or missing sidecar prevents output. Unresolved cross-references also fail.

`--check` compares an in-memory render with the committed view without writes. Drift produces a warning at exit 0, while `--strict` makes drift nonzero. Invalid source always fails.

The minimal pack emits no legacy plan template. Custom packs can still supply one. Scaffold preserves an existing generated view whose bytes differ, with a `keep (edited)` message.

## Legacy validation

Explicit legacy validation checks metrics records against their schema. `--plan` checks the Markdown plan's structured regions. A legacy TOML `--source` checks its schema and internal references.

```sh
agent-flow validate --metrics docs/metrics/workflow.jsonl
agent-flow validate --source docs/plans/my-task.plan.toml
agent-flow validate --source docs/plans/my-task.plan.toml --workflow
agent-flow validate --plan docs/plans/my-task.md --workflow
```

`--workflow` cross-references plan completion with round records and applicable waivers. A TOML source with `[meta].primary = "toml"` supplies the plan without `--plan`. Otherwise, the check uses Markdown.

Malformed records and workflow disagreements produce nonzero exits. Without `--workflow`, an absent legacy log produces a note at exit 0.

With `--workflow`, an absent log or unresolved plan fails the check. A log outside the plan's project root also fails. Containment cannot identify foreign records copied inside the correct project tree.

`--workflow-spec` selects a control-constants specification and requires `--workflow`. A malformed specification fails.

## Legacy path resolution

Without explicit `--metrics`, the log resolves from the plan source rather than the current directory.

The project root comes from the nearest `<root>/docs/plans/` ancestor of `--source`, or otherwise `--plan`. Without such an ancestor, it comes from the source's directory.

The default log is `docs/metrics/workflow.jsonl` under that root. Legacy ledger readers use `<task>.ledger.md` beside the plan source.

Explicit `--metrics` and `--ledger-fragment` paths remain verbatim. With neither source nor plan, defaults remain relative to the current directory.

Root derivation is textual and does not inspect `.git`. A bare filename from inside `docs/plans` lacks the ancestors needed for the intended project root. Run legacy commands from the project root with project-relative paths.

Containment compares real on-disk locations, so symbolic links cannot disguise an external log or ledger. Symlink layouts that separate plans from their evidence can fail containment.

When no plan is read, projections derive roots from every supplied anchor that exists on disk. The artefact must remain under all those roots.

If no supplied anchor exists, roots derive from partially resolved paths. A stderr note identifies absent or inaccessible anchors. An inaccessible anchor does not overrule an existing one.

With no anchors, projections perform no containment check. `validate --workflow` instead refuses when no plan resolves.

## Legacy status and next

`status` projects these legacy fields:

- Roadmap steps grouped by status.
- The question count.
- The metrics count.

It prefers TOML-primary source data, otherwise Markdown.

Unlike bounded mode, legacy projections are best-effort. Missing or malformed parts do not necessarily fail the command. `--json` emits the available projection.

```sh
agent-flow status --source docs/plans/my-task.plan.toml
agent-flow status --plan docs/plans/my-task.md
agent-flow status --source docs/plans/my-task.plan.toml --json
agent-flow status --source docs/plans/my-task.plan.toml --resume
```

A rejected log makes `status` print `metrics: unavailable` with a reason. Legacy `next` omits the metrics count and `ACTIVE LOOP` block for that condition. `status --resume` reports a rejected ledger instead of its `## RESUME STATE` section.

These projections still exit 0. This differs from the nonzero refusal in `validate --workflow`.

Legacy JSON carries reason fields:

`metrics_absent_reason` accepts `log-absent` or `log-not-this-project`.

`resume_state_absent_reason` belongs to legacy `next` and accepts:

- `ledger-absent`.
- `no-resume-section`.
- `ledger-not-this-project`.

`no_active_loop_reason` belongs to legacy `next` and accepts:

- `no-plan-steps`.
- `all-steps-terminal`.
- `metrics-not-this-project`.
A present component has a null absence reason. Legacy `next` has no free-form `resume_state` field.

## Code-value audit

`audit` creates an advisory static report. Its current signal covers author-declared suppression reasons, such as `#[allow(dead_code)]`, as fences rather than removal proposals.

```sh
agent-flow audit --source docs/plans/my-task.plan.toml
agent-flow audit --source docs/plans/my-task.plan.toml --json
agent-flow audit --dir path/to/crate --out reports/code-value.md
```

The default report path is `docs/plans/<task>.code-value-report.md`. `--out` changes that path. `--json` emits the typed intermediate to stdout without a report file.

The command edits no product source or plan and deletes nothing. A human decides any subsequent change.

The report's caveat limits results to the named signal set. An empty report does not prove that the codebase lacks dead code.

The command is unrelated to the historical `audit.md` user prompt. The current minimal pack does not ship that prompt.
