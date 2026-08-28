#!/bin/sh
set -eu

log=${1:-docs/metrics/workflow.jsonl}
family=1
replans=0
passes=0

jq -r '[inputs] | map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | to_entries[] | [(.key + 1), .value.artifact] | @tsv' -n "$log" |
while IFS="	" read -r pass artifact
do
    passes=$((passes + 1))
    delta=""
    if printf '%s\n' "$artifact" | grep -Fq 'Q-58/Q-82 scheduling fold'
    then
        delta="Q-58/Q-82 scheduling fold"
    elif printf '%s\n' "$artifact" | grep -Fq 'after Q-83 and'
    then
        delta="Q-83"
    elif printf '%s\n' "$artifact" | grep -Fq 'Q-85/Q-86 convergence-investigation fold'
    then
        delta="Q-85/Q-86 convergence-investigation fold"
    elif printf '%s\n' "$artifact" | grep -Fq 'Q-87 dynamic-selector decision'
    then
        delta="Q-87 dynamic-selector decision"
    fi
    if [ -n "$delta" ]
    then
        old=$family
        family=$((family + 1))
        replans=$((replans + 1))
        printf 'pass=%s family=F%s event=scope_digest_changed delta=%s terminal=Replanned dispositions=CarriedToSuccessor successor=F%s\n' "$pass" "$old" "$delta" "$family"
        printf 'pass=%s family=F%s event=successor_scope_frozen review=admitted obligation_result=historically_unreconstructible\n' "$pass" "$family"
    else
        printf 'pass=%s family=F%s event=scope_digest_matched review=admitted obligation_result=historically_unreconstructible\n' "$pass" "$family"
    fi
    if [ "$pass" -eq 10 ]
    then
        printf 'summary passes=%s terminal_replans=%s families=%s additional_human_receipts=%s additional_plan_review_and_freeze_cycles=%s\n' "$passes" "$replans" "$family" "$replans" "$replans"
    fi
done
