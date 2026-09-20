# agent-flow

[![crates.io](https://img.shields.io/crates/v/agent-flow.svg)](https://crates.io/crates/agent-flow) [![GitHub License](https://img.shields.io/github/license/nothingnesses/agent-flow?color=blue)](https://github.com/nothingnesses/agent-flow/blob/main/LICENSE)

agent-flow scaffolds a bounded agent delivery workflow into a project. It provides one compact work file and role prompts for a single implementation branch.

The delivery sequence contains at most five passes:

1. Implementation.
2. Independent product review.
3. Separate triage, only for review findings.
4. One scoped fix, only for valid findings within scope.
5. Focused verification, only after a fix.

The prompts are contracts, not agent launchers. agent-flow does not enforce role isolation or independent review. The harness or external runner supplies those properties.

The default creates no process plan tree or review records. Checks and hooks stay opt-in.

## Install the current workflow

The minimal workflow is **unreleased**. The published `agent-flow` 0.0.4 crate predates it, although current source still reports version 0.0.4. Version output alone cannot identify this workflow.

Use Rust 1.88 or newer to install from source:

```sh
git clone https://github.com/nothingnesses/agent-flow
cd agent-flow
git rev-parse HEAD
cargo install --locked --path . --root "$HOME/.local/agent-flow-source"
export PATH="$HOME/.local/agent-flow-source/bin:$PATH"
```

Record the source commit from `git rev-parse HEAD`. Check that the checkout contains [`pack/user-prompts/adopt.md`](pack/user-prompts/adopt.md) before adoption.

The separate installation root leaves other installed binaries unchanged. The binary runs without Nix.

For published versions and the former `agent-scaffold` name, see [release history](docs/reference.md#releases-and-the-rename).

## Adopt into an existing project

Follow the [adoption guide](docs/adoption.md) before any scaffold write. It covers project authority and preservation of existing material.

For agent-assisted adoption, copy the [canonical adoption prompt](pack/user-prompts/adopt.md) into your harness. The default pack installs the same prompt at `.agents/user-prompts/adopt.md`.

Scaffold preserves existing working files unless forced, but always refreshes reference assets. A preserved `AGENTS.md` does not automatically include the new workflow instructions.

## Reference

- [Workflow and command reference](docs/reference.md).
- [Custom packs and optional modules](docs/packs.md).
- [Legacy compatibility and code-value audit](docs/legacy.md).
- [Changelog](CHANGELOG.md).

## Decision and research context

- [Historical decision revalidation](docs/audits/2026-09-09-historical-decision-revalidation.md) preserves the retained direction without implementation authority.
- [Tooling research and Rust library trial](docs/audits/2026-09-16-tooling-research-and-trial.md) records later evidence and its limits.

## Licence

This project uses the [Blue Oak Model License 1.0.0](LICENSE).
