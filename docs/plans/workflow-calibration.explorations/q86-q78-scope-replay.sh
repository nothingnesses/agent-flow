#!/bin/sh
set -eu

log=${1:-docs/metrics/workflow.jsonl}
family=1
assumed_replans=0
passes=0

jq -r '[inputs] | map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | to_entries[] | [(.key + 1), .value.artifact] | @tsv' -n "$log" |
while IFS="	" read -r pass artifact
do
    passes=$((passes + 1))
    observed_fold=""
    if printf '%s\n' "$artifact" | grep -Fq 'Q-58/Q-82 scheduling fold'
    then
        observed_fold="Q-58/Q-82 scheduling fold"
    elif printf '%s\n' "$artifact" | grep -Fq 'after Q-83 and'
    then
        observed_fold="Q-83"
    elif printf '%s\n' "$artifact" | grep -Fq 'Q-85/Q-86 convergence-investigation fold'
    then
        observed_fold="Q-85/Q-86 convergence-investigation fold"
    elif printf '%s\n' "$artifact" | grep -Fq 'Q-87 dynamic-selector decision'
    then
        observed_fold="Q-87 dynamic-selector decision"
    fi
    if [ -n "$observed_fold" ]
    then
        old=$family
        family=$((family + 1))
        assumed_replans=$((assumed_replans + 1))
        printf 'pass=%s family=F%s observed_named_fold=%s digest_mapping=assumed_material_scope_delta conditional_terminal=Replanned dispositions=CarriedToSuccessor successor=F%s\n' "$pass" "$old" "$observed_fold" "$family"
        printf 'pass=%s family=F%s conditional_event=successor_scope_frozen receipt=required structured_scope_delta=required review=admitted obligation_result=historically_unreconstructible\n' "$pass" "$family"
    else
        printf 'pass=%s family=F%s observed_named_fold=none digest_mapping=assumed_unchanged conditional_review=admitted obligation_result=historically_unreconstructible\n' "$pass" "$family"
    fi
    if [ "$pass" -eq 10 ]
    then
        printf 'summary passes=%s observed_named_folds=%s assumed_digest_changes=%s conditional_terminal_replans=%s conditional_families=%s conditional_additional_human_receipts=%s conditional_additional_plan_review_and_freeze_cycles=%s\n' "$passes" "$assumed_replans" "$assumed_replans" "$assumed_replans" "$family" "$assumed_replans" "$assumed_replans"
    fi
done
