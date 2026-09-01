#!/usr/bin/env bash
# The attribution gate. It reads every commit reachable from its target and holds
# two rules the human selected: each commit carries the repository owner's raw
# author identity, and no commit message carries a co-author trailer.
#
# `.agents/checks/ci-gate.sh` runs `.agents/checks/attribution-test.sh` first, so
# scratch repositories prove both rules before this file reads the live history.
#
# Read-only: it runs `git rev-parse`, `git log`, and `git rev-list`, and writes
# nothing.
#
# Usage: attribution.sh [<repository>]
#
# `ATTRIBUTION_TARGET` names the commit to scan from; it defaults to `HEAD`. On a
# pull request GitHub CI keeps the merge-result checkout, so that builds and tests
# run against the merge, and sets this to the head commit of the branch instead:
# the merge commit's own author is GitHub's, which no allowlist can accept, and
# the branch commits are what the rules are about.
set -euo pipefail

# The allowlist, as one exact name and one exact email. It takes no environment
# override, so nothing that runs the gate can widen it.
readonly owner_name='nothingnesses'
readonly owner_email='18732253+nothingnesses@users.noreply.github.com'

repository=${1:-.}
target=${ATTRIBUTION_TARGET:-HEAD}

# ASCII case folding and ASCII character classes, whatever locale the host sets.
export LC_ALL=C

# A target the repository does not hold, such as a head SHA a partial fetch left
# out, would otherwise stop the walk before it read anything.
if ! git -C "${repository}" rev-parse --verify --quiet "${target}^{commit}" >/dev/null; then
	printf 'error: %s has no commit at %s\n' "${repository}" "${target}" >&2
	exit 1
fi

# A shallow clone hides ancestors, so the walk below would read a partial history
# and report it as a complete one.
if [[ $(git -C "${repository}" rev-parse --is-shallow-repository) == true ]]; then
	printf 'error: %s is shallow, so the check cannot read the complete history\n' \
		"${repository}" >&2
	exit 1
fi

scan() {
	local failures=0 record commit name email line folded
	local -a lines
	while IFS= read -r -d '' record; do
		# git separates entries with a newline, so every record after the first
		# arrives with one in front of the commit hash.
		record=${record#$'\n'}
		mapfile -t lines <<<"${record}"
		commit=${lines[0]}
		name=${lines[1]}
		email=${lines[2]}
		if [[ ${name} != "${owner_name}" || ${email} != "${owner_email}" ]]; then
			printf 'error: %s: author "%s <%s>" is not the repository owner "%s <%s>"\n' \
				"${commit}" "${name}" "${email}" "${owner_name}" "${owner_email}" >&2
			failures=$((failures + 1))
		fi
		# The report names the rule and the commit, never the trailer line: the line
		# holds a person's name and email, and the hash already locates it.
		for line in "${lines[@]:3}"; do
			folded=${line,,}
			if [[ ${folded} =~ ^[[:blank:]]*co-authored-by[[:blank:]]*: ]]; then
				printf 'error: %s: the commit message has a Co-Authored-By trailer\n' \
					"${commit}" >&2
				failures=$((failures + 1))
				break
			fi
		done
	done
	if ((failures > 0)); then
		printf 'error: attribution: %d violations in the history reachable from %s\n' \
			"${failures}" "${target}" >&2
		return 1
	fi
	return 0
}

# Lower-case `%an` and `%ae` report the stored identity, which is the identity the
# rule is about. A `.mailmap` reaches only their upper-case forms, whatever
# `log.mailmap` is set to, so no flag here supplies that protection and the format
# string alone carries it. The mailmap case in `.agents/checks/attribution-test.sh`
# holds the requirement: it maps a foreign author onto the owner and still expects a
# rejection, so a change to `%aN` and `%aE` fails there.
if ! git -C "${repository}" log --format='%H%n%an%n%ae%n%B%x00' "${target}" | scan; then
	exit 1
fi

printf 'attribution: %s commits reachable from %s carry the owner identity and no co-author trailer\n' \
	"$(git -C "${repository}" rev-list --count "${target}")" "${target}"
