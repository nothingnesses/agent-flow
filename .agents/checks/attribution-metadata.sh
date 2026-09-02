#!/usr/bin/env bash
# The pull request metadata gate. It holds `.agents/checks/attribution-lines.sh`, the
# classifier `.agents/checks/attribution.sh` holds over commit messages, over the title
# and body of the pull request the run is for.
#
# GitHub writes the event as JSON at `GITHUB_EVENT_PATH`. That file carries text a
# stranger wrote, so the text never reaches the shell as anything but a string: `jq`
# parses the file, the fields arrive through a quoted command substitution, they are
# compared against fixed patterns, and no path here expands or evaluates them. `jq`'s
# own diagnostics are dropped for the same reason, because a parse error quotes the
# text that failed to parse. The workflow must not interpolate the title or the body
# into the run step either; it passes only the event name and the event path, which
# GitHub itself controls.
#
# A run that is not for a pull request has no title or body and says so. A run that is
# for one has to be able to read both: a missing, unreadable, malformed, or wrongly
# shaped event fails, because the alternative is a check that passes quietly exactly
# when the metadata it guards cannot be read.
#
# Read-only: it reads one file and writes nothing.
#
# Usage: attribution-metadata.sh
#
# `GITHUB_EVENT_NAME` names the event and `GITHUB_EVENT_PATH` locates it. GitHub CI
# sets both. A local run sets neither, so the check reports that there is nothing to
# read rather than inventing a pull request.
set -euo pipefail

# ASCII case folding and ASCII character classes, whatever locale the host sets. The
# classifier is sourced after it, because it reads that setting rather than its own.
export LC_ALL=C

source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/attribution-lines.sh"

event_name=${GITHUB_EVENT_NAME:-}
event_path=${GITHUB_EVENT_PATH:-}

refuse() {
	printf 'error: pull request event: %s\n' "$1" >&2
	exit 1
}

# The event name is GitHub's, but a local caller can set anything, so it is printed
# only when it looks like one of the names GitHub uses.
if [[ ${event_name} =~ ^[a-z_]+$ ]]; then
	event_label="event ${event_name}"
else
	event_label='an event this check cannot name'
fi

case ${event_name} in
pull_request | pull_request_target) ;;
'')
	printf 'attribution metadata: no GitHub event is set, so there is no pull request title or body to check\n'
	exit 0
	;;
*)
	printf 'attribution metadata: %s is not a pull request, so there is no title or body to check\n' \
		"${event_label}"
	exit 0
	;;
esac

if ! command -v jq >/dev/null 2>&1; then
	refuse 'jq is not on PATH, so the event file cannot be parsed'
fi

if [[ -z ${event_path} ]]; then
	refuse 'GITHUB_EVENT_PATH is not set, so the title and body cannot be read'
fi

if [[ ! -f ${event_path} || ! -r ${event_path} ]]; then
	refuse 'the event file is missing or unreadable'
fi

# One pass over the event that reports a fixed word for each way it can fail to hold a
# title and a body. Only that word crosses back into the shell. A null body is the
# empty description GitHub writes for a pull request that has none, so it is a body;
# any other type means the file is not the payload it claims to be.
shape=$(jq -r '
	if (type != "object") then "event-not-an-object"
	elif (has("pull_request") | not) then "no-pull-request"
	elif ((.pull_request | type) != "object") then "pull-request-not-an-object"
	elif ((.pull_request | has("title")) | not) then "no-title"
	elif ((.pull_request.title | type) != "string") then "title-not-a-string"
	elif ((.pull_request | has("body")) | not) then "no-body"
	elif ((.pull_request.body | type) as $t | ($t != "string" and $t != "null")) then "body-not-a-string"
	else "ok"
	end' <"${event_path}" 2>/dev/null) || shape='not-json'

case ${shape} in
ok) ;;
not-json) refuse 'the event file is not valid JSON' ;;
event-not-an-object) refuse 'the event file is not a JSON object' ;;
no-pull-request) refuse 'the event has no pull_request object' ;;
pull-request-not-an-object) refuse 'the event pull_request value is not an object' ;;
no-title) refuse 'the pull request has no title field' ;;
title-not-a-string) refuse 'the pull request title is not a string' ;;
no-body) refuse 'the pull request has no body field' ;;
body-not-a-string) refuse 'the pull request body is neither a string nor null' ;;
*) refuse 'the event file could not be read' ;;
esac

# The report names the field and the rule, never the line: the title and the body are
# untrusted text, and a run's own metadata already locates them.
check_field() {
	local field=$1 filter=$2 text line status=0
	if ! text=$(jq -r "${filter}" <"${event_path}" 2>/dev/null); then
		printf 'error: pull request event: the %s could not be read\n' "${field}" >&2
		return 1
	fi
	# A title with a newline in it is several lines, and each of them is a line the
	# rules are about. A body edited through a browser arrives with carriage returns.
	while IFS= read -r line; do
		line=${line%$'\r'}
		if attribution_classify "${line}"; then
			printf 'error: the pull request %s has %s\n' "${field}" "${attribution_rule}" >&2
			status=1
			break
		fi
	done <<<"${text}"
	return "${status}"
}

failures=0
check_field title '.pull_request.title' || failures=$((failures + 1))
check_field body '.pull_request.body // ""' || failures=$((failures + 1))

if ((failures > 0)); then
	printf 'error: attribution metadata: %d of the 2 pull request fields break a rule\n' \
		"${failures}" >&2
	exit 1
fi

printf 'attribution metadata: the pull request title and body carry no attribution line\n'
