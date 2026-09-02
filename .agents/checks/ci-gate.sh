#!/usr/bin/env bash
# The one quality gate. `just ci` and the `quality` job in
# `.github/workflows/ci.yml` both run this file, so a local run and a remote run
# cannot drift; this is the check that remote branch protection requires.
#
# It sequences checks only. The caller supplies the locked toolchain: direnv
# locally, `nix develop` in CI. Every command is read-only over the tracked tree,
# and the last step proves it.
#
# It deliberately never runs `nix fmt`. That formatter applies Rust 2024
# formatting to this Rust 2021 crate and reflows the retained `docs/audits/`
# evidence, so `cargo fmt` is the accepted formatting check here.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

step() {
	printf '\n== %s ==\n' "$1"
}

# The tracked tree as the gate found it. On a CI checkout this is empty, so the
# final comparison is literally "the tracked tree is clean"; locally it lets the
# gate run over uncommitted work while still proving the gate changed none of it.
tracked_before=$(git status --porcelain --untracked-files=no)

step 'cargo fmt'
cargo fmt --all -- --check

step 'clippy'
cargo clippy --locked --all-targets -- -D warnings

step 'tests'
cargo test --locked

step 'repository checks'
cargo run --locked -- checks

step 'work state'
cargo run --locked -- validate

step 'actionlint'
actionlint

step 'reset tripwires'
# The process families RESET.md deleted. Forbidden whether tracked or not: a
# tracked one is what branch protection has to block, and an untracked one would
# otherwise slip past the tracked-tree check below.
returned=()
for artefact in \
	docs/plans \
	docs/metrics/workflow.jsonl \
	.agents/LEDGER.template.md \
	.agents/workflow.toml \
	.agents/reviews; do
	if [[ -e ${artefact} || -n $(git ls-files -- "${artefact}") ]]; then
		returned+=("${artefact}")
	fi
done
if ((${#returned[@]} > 0)); then
	printf 'error: deleted reset artefact returned: %s\n' "${returned[*]}" >&2
	exit 1
fi

step 'workflow pins'
# actionlint has no rule for this, and an unpinned action is a mutable
# dependency of every merge the gate guards.
if unpinned=$(grep -rEn '^[[:space:]]*-?[[:space:]]*uses:' .github/workflows |
	grep -Ev 'uses: [A-Za-z0-9._/-]+@[0-9a-f]{40}([[:space:]]|$)'); then
	printf 'error: workflow action is not pinned to a commit SHA:\n%s\n' "${unpinned}" >&2
	exit 1
fi

step 'attribution tests'
# The proof runs before the live history and the live event, so a check that had
# stopped rejecting a foreign author, a co-author trailer, or a generated footer fails
# here rather than passing silently.
bash .agents/checks/attribution-test.sh

step 'attribution'
bash .agents/checks/attribution.sh

step 'attribution metadata'
# The pull request's own title and body, which no commit carries. A local run and a
# push have no pull request to read, and the check reports that rather than inventing
# a pass.
bash .agents/checks/attribution-metadata.sh

step 'tracked tree'
tracked_after=$(git status --porcelain --untracked-files=no)
if [[ ${tracked_after} != "${tracked_before}" ]]; then
	printf 'error: the gate changed the tracked tree.\nbefore:\n%s\nafter:\n%s\n' \
		"${tracked_before}" "${tracked_after}" >&2
	exit 1
fi
if [[ -n ${tracked_after} ]]; then
	printf 'note: tracked files were already modified before this run:\n%s\n' "${tracked_after}"
fi

printf '\nci: every check passed\n'
