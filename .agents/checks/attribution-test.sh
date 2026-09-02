#!/usr/bin/env bash
# Deterministic proof of `.agents/checks/attribution.sh` and of
# `.agents/checks/attribution-metadata.sh`, which hold the same line rules over a
# history and over a pull request's title and body. Each case builds a throwaway
# repository or event file under the temporary directory, so no case reads or writes
# the tracked tree or GitHub's real event, and `.agents/checks/ci-gate.sh` runs this
# file before either check reads anything live.
#
# Every case supplies its own identity, drops host Git configuration, and clears the
# variables that name a repository, so a maintainer's own name, a global mailmap, a
# signing setting, or an inherited `GIT_DIR` cannot change a result.
#
# The event cases need `jq`, which the flake's development shell supplies for the same
# reason the check needs it.
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
# stops before it reads a commit. The optional last argument is text the report must
# not carry: a message rule names the rule, so the offending line stays out of the log.
expect_failure() {
	local label=$1 repository=$2 subject=$3 reason=$4 forbidden=${5:-} output status=0
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
	if [[ -n ${forbidden} && ${output} == *"${forbidden}"* ]]; then
		record_failure "${label}" "the report echoed the message content: ${output}"
		return
	fi
	printf 'ok %s\n' "${label}"
}

readonly foreign_author='is not the repository owner'
readonly foreign_trailer='has a Co-Authored-By trailer'
readonly generated_footer='has a generated attribution footer'
readonly generated_trailer='has an attribution trailer that names a generated actor'
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

# The rule is about the trailer, not about who it credits, so a plainly human co-author
# fails on the same line as an agent one.
repository=$(new_repository human-co-author)
add_commit "${repository}" "${owner_name}" "${owner_email}" \
	$'feat: add a paired change\n\nCo-authored-by: A Human <human@example.invalid>'
expect_failure 'a co-author trailer naming a human fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${foreign_trailer}" 'human@example.invalid'

# The footers the current tools write, each one whole: the decoration it leads with,
# the phrase, and the link it ends on. The Claude Code case carries its robot emoji as
# an escape, so the case holds the real bytes while this file stays ASCII.
repository=$(new_repository claude-footer)
add_commit "${repository}" "${owner_name}" "${owner_email}" \
	$'feat: add a generated change\n\n\xf0\x9f\xa4\x96 Generated with [Claude Code](https://claude.com/claude-code)'
expect_failure 'the Claude Code footer fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${generated_footer}" 'claude.com'

repository=$(new_repository codex-footer)
add_commit "${repository}" "${owner_name}" "${owner_email}" \
	$'feat: add a delegated change\n\nGenerated by Codex (https://chatgpt.com/codex)'
expect_failure 'a GPT or Codex footer fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${generated_footer}" 'chatgpt.com'

# The same family under a versioned model name. The split drops the model number, so
# these leave a bare `o` where the Codex footer above leaves a whole word, and a
# vocabulary without it would read them as sentences and accept the history.
repository=$(new_repository gpt-model-footer)
add_commit "${repository}" "${owner_name}" "${owner_email}" \
	$'feat: add a versioned change\n\nGenerated by GPT-4o (https://chatgpt.com)'
expect_failure 'a versioned GPT model footer fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${generated_footer}" 'chatgpt.com'

repository=$(new_repository gpt-edition-footer)
add_commit "${repository}" "${owner_name}" "${owner_email}" \
	$'feat: add a smaller change\n\n\xf0\x9f\xa4\x96 Generated with GPT-4o-mini'
expect_failure 'a GPT edition footer fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${generated_footer}" 'GPT'

repository=$(new_repository gemini-footer)
add_commit "${repository}" "${owner_name}" "${owner_email}" \
	$'feat: add an assisted change\n\nGenerated with [Gemini CLI](https://github.com/google-gemini/gemini-cli)'
expect_failure 'a Gemini footer fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${generated_footer}" 'gemini-cli'

repository=$(new_repository copilot-footer)
add_commit "${repository}" "${owner_name}" "${owner_email}" \
	$'feat: add a suggested change\n\nThis pull request was created by GitHub Copilot.'
expect_failure 'a Copilot footer fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${generated_footer}" 'Copilot'

# A trailer key that attributes the work, with an actor in its value, is the other
# structural form, and it reports its own rule rather than the footer one.
repository=$(new_repository attribution-trailer)
add_commit "${repository}" "${owner_name}" "${owner_email}" \
	$'feat: add a credited change\n\nGenerated-By: Claude Code'
expect_failure 'an attribution trailer naming an actor fails' "${repository}" \
	"$(git -C "${repository}" rev-parse HEAD)" "${generated_trailer}" 'Claude Code'

# The other half of the rule. These lines name the same tools, and one of them opens on
# the same verb a footer opens on, but each is a sentence rather than an attribution, so
# the history is valid and the check has to say so. A trailer key with no actor in its
# value is a sentence too.
repository=$(new_repository safe-mentions)
add_commit "${repository}" "${owner_name}" "${owner_email}" \
	$'docs: describe the attribution rules\n\nThe gate rejects a footer generated with Claude Code and a trailer that names Codex, Gemini or Copilot.\n\nOrdinary prose about an AI agent, an LLM, or the Copilot commit footer stays valid, because a sentence carries a word no footer carries.\n\nGenerated footers name their tool, which is what the classifier keys on.\n\nGenerated by GPT-4o and by o3, those footers now fail, and this sentence about them does not.\n\nCreated by hand, this change carries no generated footer.\n\nAssisted-by: a human reviewer'
expect_pass 'safe technical mentions pass' "${repository}"

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

# The pull request half of the gate. Each case writes its own event file under the same
# temporary directory and names it explicitly, so no case reads GitHub's real event or
# another case's, and the two variables a run supplies are set per case rather than
# inherited: a real pull request run sets both, and a maintainer's shell sets neither.
metadata_check=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/attribution-metadata.sh

# `jq` writes the event, so a title or a body holding quotes, backslashes, or shell
# punctuation is escaped by the same parser the check reads it back with, and the case
# proves the check rather than the fixture.
new_event() {
	local name=$1 title=$2 body=$3
	local path=${scratch}/${name}.json
	jq -n --arg title "${title}" --arg body "${body}" \
		'{pull_request: {title: $title, body: $body}}' >"${path}"
	printf '%s' "${path}"
}

# The cases that are about a broken payload write it byte for byte instead.
raw_event() {
	local name=$1 content=$2
	local path=${scratch}/${name}.json
	printf '%s' "${content}" >"${path}"
	printf '%s' "${path}"
}

expect_metadata_pass() {
	local label=$1 name=$2 path=$3 output status=0
	cases=$((cases + 1))
	output=$(GITHUB_EVENT_NAME="${name}" GITHUB_EVENT_PATH="${path}" \
		bash "${metadata_check}" 2>&1) || status=$?
	if ((status != 0)); then
		record_failure "${label}" "the check rejected valid metadata: ${output}"
		return
	fi
	printf 'ok %s\n' "${label}"
}

expect_metadata_failure() {
	local label=$1 name=$2 path=$3 subject=$4 reason=$5 forbidden=${6:-} output status=0
	cases=$((cases + 1))
	output=$(GITHUB_EVENT_NAME="${name}" GITHUB_EVENT_PATH="${path}" \
		bash "${metadata_check}" 2>&1) || status=$?
	if ((status == 0)); then
		record_failure "${label}" 'the check accepted metadata it must reject'
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
	if [[ -n ${forbidden} && ${output} == *"${forbidden}"* ]]; then
		record_failure "${label}" "the report echoed the event content: ${output}"
		return
	fi
	printf 'ok %s\n' "${label}"
}

event=$(new_event clean-pull-request 'fix: reject generated attribution messages' \
	$'The body explains the change.\n\nIt mentions Claude Code and Copilot in a sentence, which is not a footer.')
expect_metadata_pass 'a clean pull request passes' pull_request "${event}"

# The same classifier over the other surface: the title and the body break the same
# rules a commit message breaks, and the report names the field rather than the line.
event=$(new_event generated-title \
	"$(printf '\xf0\x9f\xa4\x96 Generated with [Claude Code](https://claude.com/claude-code)')" \
	'A body that says nothing about its author.')
expect_metadata_failure 'a generated title fails' pull_request "${event}" \
	'pull request title' "${generated_footer}" 'claude.com'

event=$(new_event generated-body 'fix: correct the rule' \
	$'The change is small.\n\nCo-Authored-By: Claude <noreply@anthropic.com>')
expect_metadata_failure 'a co-author trailer in the body fails' pull_request "${event}" \
	'pull request body' "${foreign_trailer}" 'noreply@anthropic.com'

event=$(new_event codex-body 'fix: correct the other rule' \
	$'The change is small.\n\nGenerated by Codex (https://chatgpt.com/codex)')
expect_metadata_failure 'a generated footer in the body fails' pull_request "${event}" \
	'pull request body' "${generated_footer}" 'chatgpt.com'

# The versioned model name reaches this surface too, and the classifier is the same one,
# so the vocabulary that closes the phrase has to hold for a body and a title as well.
event=$(new_event gpt-model-body 'fix: correct the versioned rule' \
	$'The change is small.\n\nGenerated with GPT-4o (https://chatgpt.com)')
expect_metadata_failure 'a versioned GPT model footer in the body fails' pull_request \
	"${event}" 'pull request body' "${generated_footer}" 'chatgpt.com'

event=$(new_event gpt-model-title 'This pull request was created by GPT-4o' \
	'A body that says nothing about its author.')
expect_metadata_failure 'a versioned GPT model footer in the title fails' pull_request \
	"${event}" 'pull request title' "${generated_footer}" 'GPT'

# The other half of the rule on this surface: a body that names the same model in a
# sentence is prose, so it stays valid.
event=$(new_event gpt-model-mention 'fix: describe the versioned rule' \
	$'The change is small.\n\nGenerated by GPT-4o and by o3, those footers now fail, and this sentence about them does not.')
expect_metadata_pass 'a safe mention of a GPT model passes' pull_request "${event}"

# A title split across lines would otherwise hide an attribution line behind the first
# one, so every line of both fields is classified.
event=$(new_event multi-line-title \
	$'fix: correct the rule\nGenerated with Claude Code' 'A body.')
expect_metadata_failure 'an attribution line below a title fails' pull_request "${event}" \
	'pull request title' "${generated_footer}" 'Claude'

# Untrusted text that looks like a command. It has to pass the rules, because it
# attributes nothing, and it has to stay text: the sentinel below exists only if some
# part of the check let the event's own words run.
sentinel=${scratch}/executed
event=$(new_event command-like-text \
	"fix: quote \$(touch ${sentinel}) and \`touch ${sentinel}\` safely" \
	"$(printf 'The body carries ; touch %s and $(touch %s) and `touch %s`.\nIt still names no author.' \
		"${sentinel}" "${sentinel}" "${sentinel}")")
expect_metadata_pass 'command-like untrusted text passes' pull_request "${event}"
cases=$((cases + 1))
if [[ -e ${sentinel} ]]; then
	record_failure 'command-like untrusted text stays inert' 'the check ran text from the event'
else
	printf 'ok %s\n' 'command-like untrusted text stays inert'
fi

# A push carries no pull request, so the metadata rules have nothing to read. The event
# here would fail every one of them, which is what makes the skip visible.
event=$(new_event pushed-event 'Generated with [Claude Code](https://claude.com/claude-code)' \
	'Co-Authored-By: Claude <noreply@anthropic.com>')
expect_metadata_pass 'a push skips the pull request metadata' push "${event}"
expect_metadata_pass 'a run with no event skips the pull request metadata' '' ''

# Once the event claims to be a pull request, every way of not producing a title and a
# body is a failure. A check that skipped here would pass exactly when the metadata it
# guards became unreadable.
expect_metadata_failure 'a pull request event with no event path fails' pull_request '' \
	'pull request event' 'GITHUB_EVENT_PATH is not set'
expect_metadata_failure 'a missing event file fails' pull_request "${scratch}/absent.json" \
	'pull request event' 'the event file is missing or unreadable'

event=$(raw_event malformed-event '{"pull_request": {"title": "fix: correct the rule",')
expect_metadata_failure 'a malformed event file fails' pull_request "${event}" \
	'pull request event' 'the event file is not valid JSON' 'fix: correct the rule'

event=$(raw_event array-event '["pull_request"]')
expect_metadata_failure 'an event that is not an object fails' pull_request "${event}" \
	'pull request event' 'the event file is not a JSON object'

event=$(raw_event no-pull-request-event '{"repository": {"name": "agent-scaffold"}}')
expect_metadata_failure 'an event with no pull request fails' pull_request "${event}" \
	'pull request event' 'the event has no pull_request object'

event=$(raw_event pull-request-not-an-object '{"pull_request": "fix: correct the rule"}')
expect_metadata_failure 'a pull request that is not an object fails' pull_request "${event}" \
	'pull request event' 'the event pull_request value is not an object'

event=$(raw_event no-title '{"pull_request": {"body": "A body."}}')
expect_metadata_failure 'a pull request with no title fails' pull_request "${event}" \
	'pull request event' 'the pull request has no title field'

event=$(raw_event title-not-a-string '{"pull_request": {"title": 12, "body": "A body."}}')
expect_metadata_failure 'a title that is not a string fails' pull_request "${event}" \
	'pull request event' 'the pull request title is not a string'

event=$(raw_event no-body '{"pull_request": {"title": "fix: correct the rule"}}')
expect_metadata_failure 'a pull request with no body fails' pull_request "${event}" \
	'pull request event' 'the pull request has no body field'

event=$(raw_event body-not-a-string '{"pull_request": {"title": "fix: correct the rule", "body": []}}')
expect_metadata_failure 'a body that is neither a string nor null fails' pull_request "${event}" \
	'pull request event' 'the pull request body is neither a string nor null'

# GitHub writes a null body for a pull request that has no description, so a null body
# is an empty one rather than a broken payload.
event=$(raw_event null-body '{"pull_request": {"title": "fix: correct the rule", "body": null}}')
expect_metadata_pass 'a null body is an empty description' pull_request "${event}"

if ((failures > 0)); then
	printf 'error: attribution tests: %d of %d cases failed\n' "${failures}" "${cases}" >&2
	exit 1
fi
printf 'attribution tests: %d cases passed\n' "${cases}"
