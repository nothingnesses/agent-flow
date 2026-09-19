# Custom packs

For normal adoption, use the [default-pack guide](adoption.md). A custom pack can produce a different layout and workflow.

## Manifest and variables

`--template` selects a directory pack instead of the embedded pack:

```sh
agent-flow scaffold --template path/to/my-pack --var project=my-service --var author=maintainer --dry-run
```

The directory contains `pack.toml`:

```toml
[[asset]]
source = "AGENTS.md"
dest = "AGENTS.md"
ownership = "working"
render = true

[[asset]]
source = "principles.toml"
dest = ".agents/principles.toml"
ownership = "reference"

[[asset]]
source = "hooks/pre-commit"
dest = ".agents/hooks/pre-commit"
ownership = "reference"
executable = true

[[var]]
name = "project"
default = "my-project"

[[var]]
name = "author"
```

Each asset maps a source to a relative destination. One source can supply several destinations.

`working` assets are create-if-absent unless forced. `reference` assets refresh on every write. `executable = true` sets Unix mode `0o755`, with no mode change on non-Unix systems.

`render = true` enables minimal `{{name}}` substitution, not a template language. Without it, the file is copied verbatim. Rendered content ends with one newline. Unknown placeholders remain unchanged.

Variables without a default require `--var name=value`. An undeclared variable or absent required value causes an error before writes.

The tool reserves these variables:

- `principles`.
- `instrument`.
- `modules`.
- `workflow_control`.
- `isolation_policy`.
- `recommendation_rule`.
- `findings_naming`.

Packs cannot declare reserved variables or override them with `--var`.

`principles` contains the selected principles. A directory pack uses its own `principles.toml`. A pack without that file has no principles.

`instrument` contains the optional `instrument.md` fragment when `--instrument` is present. Otherwise it is empty. The minimal built-in pack has no instrumentation slot and creates no round log.

`modules` contains enabled module guidance in declaration order. The remaining reserved fragments support compatibility guidance.

## Containment

Every pack source must remain inside the pack directory. This includes:

- Asset sources.
- Module guidance.
- `pack.toml`.
- `principles.toml`.
- `instrument.md`.

The loader rejects absolute paths and `..` components. It also rejects files that resolve outside the pack through symbolic links. A refusal names the file and prevents writes.

Links within the pack work. A `--template` link to the pack directory also works.

If all linked files resolve into one real directory, select that directory. Otherwise, materialise the pack into real files, for example with `cp -rL`, or use a clone.

Destination paths must be relative without `..` components. This lexical check does not protect against symlinked destination directories. Inspect the consuming project's destinations before any write.

## Optional modules

Modules group opt-in assets and variables:

```toml
[[module]]
name = "diagrams"
description = "Adds a diagram template."
guidance = "diagrams-guidance.md"
requires = ["checks"]

[[module]]
name = "checks"
description = "Adds project checks."

[[asset]]
source = "diagram.md"
dest = "docs/diagram.md"
ownership = "working"
render = true
module = "diagrams"

[[var]]
name = "diagram_title"
module = "diagrams"
```

`--module <name>` is repeatable. Untagged entries always apply. Tagged entries apply only when their module is enabled.

Disabled variables contribute no defaults and require no values. A `--var` for a disabled variable is undeclared and fails.

An optional `guidance` file contributes to `{{modules}}` rather than a separate output asset. Enabled guidance files must exist.

`requires` enables dependencies transitively. Cycles terminate through fixed-point expansion.

These errors prevent writes:

- Unknown selected modules.
- Unknown module tags.
- Unknown dependencies.
- Duplicate module declarations.

With no selected modules, tagged entries do not affect the core output.
