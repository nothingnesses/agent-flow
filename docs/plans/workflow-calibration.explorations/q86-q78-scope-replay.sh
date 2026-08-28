#!/bin/sh
set -eu

select_rows()
{
    jq -r '[inputs] | map(select(.type == "round" and .task == "q78-design-pass" and .phase == "acceptance")) | to_entries[] | [(.key + 1), .value.artifact] | @tsv' -n "$1"
}

replay_rows()
{
    family=1
    assumed_replans=0
    passes=0
    seen_folds='|'
    while IFS="	" read -r pass artifact
    do
        [ -n "$pass" ] || continue
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
            if printf '%s\n' "$seen_folds" | grep -Fq "|$observed_fold|"
            then
                printf 'pass=%s family=F%s observed_named_fold=%s fold_identity=repeated digest_mapping=already_counted conditional_review=admitted obligation_result=historically_unreconstructible\n' "$pass" "$family" "$observed_fold"
                continue
            fi
            seen_folds="${seen_folds}${observed_fold}|"
            old=$family
            family=$((family + 1))
            assumed_replans=$((assumed_replans + 1))
            printf 'pass=%s family=F%s observed_named_fold=%s fold_identity=first_observation digest_mapping=assumed_material_scope_delta conditional_terminal=Replanned dispositions=CarriedToSuccessor successor=F%s\n' "$pass" "$old" "$observed_fold" "$family"
            printf 'pass=%s family=F%s conditional_event=successor_scope_frozen receipt=required structured_scope_delta=required review=admitted obligation_result=historically_unreconstructible\n' "$pass" "$family"
        else
            printf 'pass=%s family=F%s observed_named_fold=none digest_mapping=assumed_unchanged conditional_review=admitted obligation_result=historically_unreconstructible\n' "$pass" "$family"
        fi
    done
    printf 'summary passes=%s observed_named_folds=%s assumed_digest_changes=%s conditional_terminal_replans=%s conditional_families=%s conditional_additional_human_receipts=%s conditional_additional_plan_review_and_freeze_cycles=%s\n' "$passes" "$assumed_replans" "$assumed_replans" "$assumed_replans" "$family" "$assumed_replans" "$assumed_replans"
}

synthetic_rows()
{
    count=$1
    pass=1
    while [ "$pass" -le "$count" ]
    do
        artifact='unchanged acceptance target'
        if [ "$pass" -eq 2 ]
        then
            artifact='Q-58/Q-82 scheduling fold'
        elif [ "$pass" -eq 4 ]
        then
            artifact='target after Q-83 and repair'
        elif [ "$pass" -eq 7 ]
        then
            artifact='Q-85/Q-86 convergence-investigation fold'
        elif [ "$pass" -eq 8 ] || [ "$pass" -eq 11 ]
        then
            artifact='Q-87 dynamic-selector decision'
        fi
        printf '%s\t%s\n' "$pass" "$artifact"
        pass=$((pass + 1))
    done
}

run_replay()
{
    rows=$(select_rows "$1")
    if [ -n "$rows" ]
    then
        replay_rows <<EOF
$rows
EOF
    else
        replay_rows </dev/null
    fi
}

check_synthetic()
{
    count=$1
    expected=$2
    rows=$(synthetic_rows "$count")
    output=$(replay_rows <<EOF
$rows
EOF
)
    summary=$(printf '%s\n' "$output" | awk '
        /^summary / {
            seen += 1
            line = $0
        }
        END {
            if (seen != 1) exit 1
            print line
        }
    ')
    if [ "$summary" != "$expected" ]
    then
        printf 'self-test failed for %s selected passes\nexpected: %s\nactual: %s\n' "$count" "$expected" "$summary" >&2
        exit 1
    fi
    printf 'self_test selected_passes=%s %s\n' "$count" "$summary"
}

if [ "${1:-}" = "--self-test" ]
then
    check_synthetic 9 'summary passes=9 observed_named_folds=4 assumed_digest_changes=4 conditional_terminal_replans=4 conditional_families=5 conditional_additional_human_receipts=4 conditional_additional_plan_review_and_freeze_cycles=4'
    check_synthetic 11 'summary passes=11 observed_named_folds=4 assumed_digest_changes=4 conditional_terminal_replans=4 conditional_families=5 conditional_additional_human_receipts=4 conditional_additional_plan_review_and_freeze_cycles=4'
    exit 0
fi

run_replay "${1:-docs/metrics/workflow.jsonl}"
