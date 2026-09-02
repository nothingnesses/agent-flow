#!/usr/bin/env bash
# The attribution-line classifier. `.agents/checks/attribution.sh` holds it over every
# reachable commit message and `.agents/checks/attribution-metadata.sh` holds it over a
# pull request's title and body, so one line reaches one verdict wherever it is written.
# This file is sourced, never run.
#
# It reads a whole line at a time, never a substring of one, and holds three rules:
#
#   1. A `Co-Authored-By:` trailer, whoever it names. This repository's commits carry
#      one author, so the actor cannot change the verdict.
#   2. An attribution trailer: a trailer whose key attributes the work and whose value
#      names a generated actor, such as `Generated-by: Claude Code`.
#   3. A generated footer: a line that is nothing but an attribution phrase, such as
#      `Generated with [Claude Code](https://claude.com/claude-code)`.
#
# Rule 3 has no key to recognise, so it has to read the whole line. The line must open
# with the attribution phrase, and every word after it must be a word a footer uses.
# That closed vocabulary is what keeps ordinary prose valid: a sentence about Claude,
# Codex, Gemini, Copilot, or about this detector, carries some word no footer carries,
# so it cannot match. The cost is a bespoke attribution sentence that no known tool
# writes, which this check does not claim to catch.
#
# The rule phrases below name the broken rule and nothing else. A caller reports the
# phrase and the place, so untrusted message content never reaches a log.
#
# Callers must export `LC_ALL=C`: the folding and the character classes here are ASCII,
# and a commit message or a pull request body may hold any bytes at all.

# The words that name a generated actor. Whole words only, because the classifier
# splits a line into words first: `ai` cannot match inside `said`, and `gpt` cannot
# match inside a hash.
attribution_actor_word() {
	case $1 in
	claude | anthropic | chatgpt | gpt | openai | codex | gemini | copilot | \
		llm | llms | ai | agent | agents | assistant | assistants | \
		bot | bots | model | models) return 0 ;;
	esac
	return 1
}

# The rest of a footer's vocabulary: the connectives a footer puts between its words,
# the vendor and edition words that finish an actor's name, and the words that are left
# of a link to the actor's home page once the punctuation is gone.
#
# The bare `o` is an edition word too. A model number is a separator, so a versioned GPT
# name leaves it behind on its own: `GPT-4o` splits into `gpt` and `o`, and `o3` into
# `o`. Without it those footers would carry a word no footer carries and read as
# sentences. It names no actor by itself, so a line still has to name one to match.
attribution_footer_word() {
	case $1 in
	a | an | the | and | my | our | its | this | of | in | on | at | to | for | \
		with | by | using | via | from | \
		google | github | microsoft | amazon | mistral | deepseek | \
		code | coding | cli | app | chat | desktop | web | studio | \
		assist | assistance | assisted | help | tool | tools | \
		o | pro | flash | ultra | mini | nano | turbo | preview | latest | \
		sonnet | opus | haiku | \
		https | http | www | com | org | net | io | dev | sh) return 0 ;;
	esac
	return 1
}

# The ASCII letter words of an already folded line, in order. Everything else is a
# separator: a footer's version number, its link punctuation, and whatever bytes a
# message carries are noise, and the rules are about the words around them.
attribution_split() {
	local IFS=$' \t\n' text=${1//[^a-z]/ }
	# The unquoted expansion is the split itself, and the text holds only letters and
	# spaces by now, so there is nothing here for a glob to match.
	attribution_words=(${text})
}

attribution_names_actor() {
	local word
	for word in "${attribution_words[@]}"; do
		if attribution_actor_word "${word}"; then
			return 0
		fi
	done
	return 1
}

# A footer phrase names an actor and says nothing else. One word outside the vocabulary
# is enough to make the line a sentence rather than a footer.
attribution_is_footer_phrase() {
	local word named=1
	for word in "${attribution_words[@]}"; do
		if attribution_actor_word "${word}"; then
			named=0
			continue
		fi
		if ! attribution_footer_word "${word}"; then
			return 1
		fi
	done
	return "${named}"
}

# The trailer keys that attribute the work. `Co-Authored-By` is rule 1 and is not here,
# because rule 1 needs no actor.
readonly attribution_trailer_key='(generated-by|generated-with|generated-using|created-by|created-with|authored-by|written-by|made-by|made-with|built-by|built-with|assisted-by|committed-by|signed-off-by|co-authored-with|co-written-by|on-behalf-of|attribution|agent|assistant|model|llm|ai|bot|tool)'

# The opening of a generated footer: the decoration a footer leads with, such as the
# robot emoji Claude Code writes or a list marker; an optional subject clause, so
# `This pull request was created by ...` reads as one phrase; then the verb and the
# preposition that start the attribution.
readonly attribution_footer_head='^[^[:alpha:]]*((this|these|it|they|the)[[:blank:]]+([a-z]+[[:blank:]]+){0,2}(was|were|is|are)[[:blank:]]+)?(co-)?(generated|created|authored|written|produced|made|built|drafted|committed|assisted|developed|implemented)[[:blank:]]+(with|by|using|via|from)[[:blank:]]+'

# The one entry point. It sets `attribution_rule` to the phrase that names the broken
# rule and returns 0 when the line is an attribution line, and clears the phrase and
# returns 1 when it is not.
attribution_classify() {
	local folded=${1,,}
	attribution_rule=''

	if [[ ${folded} =~ ^[[:blank:]]*co-authored-by[[:blank:]]*: ]]; then
		attribution_rule='a Co-Authored-By trailer'
		return 0
	fi

	# `BASH_REMATCH[0]` ends at the colon, so the rest of the line is the value.
	if [[ ${folded} =~ ^[[:blank:]]*${attribution_trailer_key}[[:blank:]]*: ]]; then
		attribution_split "${folded:${#BASH_REMATCH[0]}}"
		if attribution_names_actor; then
			attribution_rule='an attribution trailer that names a generated actor'
			return 0
		fi
	fi

	if [[ ${folded} =~ ${attribution_footer_head} ]]; then
		attribution_split "${folded:${#BASH_REMATCH[0]}}"
		if attribution_is_footer_phrase; then
			attribution_rule='a generated attribution footer'
			return 0
		fi
	fi

	return 1
}
