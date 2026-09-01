#!/usr/bin/env bash
# Deterministic proof of `.agents/checks/attribution.sh`. Each case builds a
# throwaway repository under the temporary directory, so no case reads or writes
# the tracked tree, and `.agents/checks/ci-gate.sh` runs this file before it reads
# the live history.
#
# Every case supplies its own identity, drops host Git configuration, and clears the
# variables that name a repository, so a maintainer's own name, a global mailmap, a
# signing setting, or an inherited `GIT_DIR` cannot change a result.
set -euo pipefail

check=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/attribution.sh

readonly owner_name='nothingnesses'
readonly owner_email='18732253+nothingnesses@users.noreply.github.com'

export GIT_CONFIG_GLOBAL=/dev/null
export GIT_CONFIG_SYSTEM=/dev/null
export GIT_CONFIG_NOSYSTEM=1

# Git honours these over `-C` and over any repository configuration, so an inherited
# value would send every command below, and the check this file runs, at the caller's
# repository instead of the scratch one: the cases would then read a history they did
# not build, and a case that commits would write into that repository. `unset` drops
# them from the environment, so the check inherits the cleared set too.
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY \
	GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_COMMON_DIR GIT_NAMESPACE

scratch=$(mktemp -d)
trap 'rm -rf "${scratch}"' EXIT

cases=0
failures=0
commits=0

new_repository() {
	local repository=${scratch}/$1
	mkdir "${repository}"
	git -C "${repository}" init --quiet --initial-branch=main
	printf '%s' "${repository}"
}

# The author identity travels in the environment, which outranks configuration, so
# a `GIT_AUTHOR_NAME` in the caller's shell cannot reach the commit. `verbatim`
# cleanup stores the message exactly as the case writes it.
add_commit() {
	local repository=$1 name=$2 email=$3 message=$4
	commits=$((commits + 1))
	printf 'change %d\n' "${commits}" >>"${repository}/history.txt"
	git -C "${repository}" add history.txt
	GIT_AUTHOR_NAME=${name} GIT_AUTHOR_EMAIL=${email} \
		GIT_COMMITTER_NAME=${name} GIT_COMMITTER_EMAIL=${email} \
		git -C "${repository}" commit --quiet --cleanup=verbatim --message "${message}"
}

record_failure() {
	failures=$((failures + 1))
	printf 'FAIL %s: %s\n' "$1" "$2" >&2
}

# Each case names the scratch repository's own `HEAD` as the target, so an
# `ATTRIBUTION_TARGET` the caller set, as GitHub CI does, cannot reach a case and
# turn a built history into an unresolvable one.
expect_pass() {
	local label=$1 repository=$2 output status=0
	cases=$((cases + 1))
	output=$(ATTRIBUTION_TARGET=HEAD bash "${check}" "${repository}" 2>&1) || status=$?
	if ((status != 0)); then
		record_failure "${label}" "the check rejected a valid history: ${output}"
		return
	fi
	printf 'ok %s\n' "${label}"
}

# The report has to name what it rejected and give the reason. The subject is the
# offending commit for a history violation, and the repository itself where the walk
# stops before it reads a commit.
expect_failure() {
	local label=$1 repository=$2 subject=$3 reason=$4 output status=0
	cases=$((cases + 1))
	output=$(ATTRIBUTION_TARGET=HEAD bash "${check}" "${repository}" 2>&1) || status=$?
	if ((status == 0)); then
		record_failure "${label}" 'the check accepted a repository it must reject'
		return
	fi
	if [[ ${output} != *"${subject}"* ]]; then
		record_failure "${label}" "the report does not name ${subject}: ${output}"
		return
	fi
	if [[ ${output} != *"${reason}"* ]]; then
		record_failure "${label}" "the report does not give the reason: ${output}"
		return
	fi
	printf 'ok %s\n' "${label}"
}

readonly foreign_author='is not the repository owner'
readonly foreign_trailer='has a Co-Authored-By trailer'
readonly shallow_history='is shallow, so the check cannot read the complete history'

repository=$(new_repository valid-history)
add_commit "${repository}" "${owner_name}" "${owner_email}" 'feat: add the first change'
add_commit "${repository}" "${owner_name}" "${owner_email}" \
	$'feat: add the second change\n\nThe body names Co-Authored-By in a sentence, which is not a trailer.'
add_commit "${repository}" "${owner_name}" "${owner_email}" 'docs: describe the second change'
expect_pass 'a valid history passes' "${repository}"

repository=$(new_repository foreign-author)
add_commit "${repository}" "${owner_name}" "${owner_email}" 'feat: add the first change'
add_commit "${repository}" 'Some Agent' 'agent@example.invalid' 'feat: add a foreign change'
expect_failure 'a foreign author fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${foreign_author}"

repository=$(new_repository placeholder-author)
add_commit "${repository}" 'Test' 'test@example.com' 'feat: add a placeholder change'
expect_failure 'a placeholder author fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${foreign_author}"

repository=$(new_repository another-name)
add_commit "${repository}" 'Another Name' "${owner_email}" 'feat: add a renamed change'
expect_failure 'the owner email under another name fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${foreign_author}"

repository=$(new_repository another-email)
add_commit "${repository}" "${owner_name}" 'nothingnesses@example.invalid' \
	'feat: add a rerouted change'
expect_failure 'the owner name under another email fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${foreign_author}"

repository=$(new_repository co-author-trailer)
add_commit "${repository}" "${owner_name}" "${owner_email}" \
	$'feat: add a shared change\n\nCo-Authored-By: Some Agent <agent@example.invalid>'
expect_failure 'a co-author trailer fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${foreign_trailer}"

repository=$(new_repository lower-case-trailer)
add_commit "${repository}" "${owner_name}" "${owner_email}" \
	$'feat: add a padded change\n\n  co-authored-by : Some Agent <agent@example.invalid>'
expect_failure 'a lower-case padded co-author trailer fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${foreign_trailer}"

repository=$(new_repository upper-case-trailer)
add_commit "${repository}" "${owner_name}" "${owner_email}" \
	$'feat: add an indented change\n\n\tCO-AUTHORED-BY:\tSome Agent <agent@example.invalid>'
expect_failure 'an upper-case indented co-author trailer fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${foreign_trailer}"

# The rewritten history put the removed identities and trailers below the tip, so
# a check that read only the tip commit would report a clean repository.
repository=$(new_repository ancestor-violation)
add_commit "${repository}" 'Some Agent' 'agent@example.invalid' 'feat: add the first change'
ancestor=$(git -C "${repository}" rev-parse HEAD)
add_commit "${repository}" "${owner_name}" "${owner_email}" 'feat: add the second change'
add_commit "${repository}" "${owner_name}" "${owner_email}" 'docs: describe both changes'
expect_failure 'a violation below the tip fails' "${repository}" "${ancestor}" "${foreign_author}"

# A `.mailmap` rewrites the identity that upper-case `%aN` and `%aE` report, so a
# check reading those would see the owner here and accept the history. The rule is
# about the stored identity, which lower-case `%an` and `%ae` report, and the report
# has to keep naming the commit that carries the foreign one.
repository=$(new_repository mailmap-rewrite)
add_commit "${repository}" 'Some Agent' 'agent@example.invalid' 'feat: add a foreign change'
foreign=$(git -C "${repository}" rev-parse HEAD)
printf '%s <%s> Some Agent <agent@example.invalid>\n' "${owner_name}" "${owner_email}" \
	>"${repository}/.mailmap"
git -C "${repository}" add .mailmap
add_commit "${repository}" "${owner_name}" "${owner_email}" 'chore: record the mailmap'
expect_failure 'a mailmap rewrite of a foreign author fails' "${repository}" \
	"${foreign}" "${foreign_author}"

# A shallow clone holds the tip and hides its ancestors, so a check without the
# shallow guard would read the one accepted commit this clone keeps and report a
# history whose root it never saw as clean. `--depth` needs a transport rather than a
# local copy, hence the `file://` URL. The rejection names the repository, because the
# walk stops before it reads a commit.
source_repository=$(new_repository shallow-source)
add_commit "${source_repository}" 'Some Agent' 'agent@example.invalid' \
	'feat: add the first change'
add_commit "${source_repository}" "${owner_name}" "${owner_email}" \
	'feat: add the second change'
clone=${scratch}/shallow-clone
git clone --quiet --depth 1 "file://${source_repository}" "${clone}"
expect_failure 'a shallow clone fails' "${clone}" "${clone}" "${shallow_history}"

if ((failures > 0)); then
	printf 'error: attribution tests: %d of %d cases failed\n' "${failures}" "${cases}" >&2
	exit 1
fi
printf 'attribution tests: %d cases passed\n' "${cases}"
