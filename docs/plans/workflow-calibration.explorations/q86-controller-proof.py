#!/usr/bin/env python3
from collections import deque
from dataclasses import dataclass
import argparse

SEVERITIES = ("low", "high", "critical")
BACKSTOP = ("high", "critical")
NON_DELIVERY = ("remove_delivery", "revert", "replan", "abandon")
FLOOR = "high"


def severity_of(finding):
    for severity in SEVERITIES:
        if finding.endswith("_" + severity):
            return severity
    return None


def is_critical(finding):
    return severity_of(finding) == "critical"


def is_outstanding(finding):
    return finding.startswith(("open", "repaired", "pending"))


def is_pending(finding):
    return finding.startswith("pending_")


def at_floor(severity):
    rank = {"low": 1, "high": 2, "critical": 3}
    return severity is not None and rank[severity] >= rank[FLOOR]


@dataclass(frozen=True)
class AState:
    control: str
    reviews: int
    streak: int
    serious_seen: bool
    finding: str


def a_limit(state, normal, reserve):
    return normal + reserve if state.serious_seen else normal


def a_settled(state, reviews, finding, need, normal, reserve):
    streak = state.streak + 1
    if streak >= need:
        return AState("complete", reviews, streak, state.serious_seen, finding)
    candidate = AState("active", reviews, streak, state.serious_seen, finding)
    if reviews >= a_limit(candidate, normal, reserve):
        return AState("terminal", reviews, streak, state.serious_seen, finding)
    return candidate


def a_open(state, reviews, finding, serious_seen, normal, reserve):
    candidate = AState("repair", reviews, 0, serious_seen, finding)
    if reviews >= a_limit(candidate, normal, reserve):
        terminal = "serious_blocked" if at_floor(severity_of(finding)) else "terminal"
        return AState(terminal, reviews, 0, serious_seen, finding)
    return candidate


def a_edges(state, need, normal, reserve):
    edges = []
    if state.control == "active":
        reviews = state.reviews + 1
        edges.append(("review_settled", a_settled(state, reviews, "none", need, normal, reserve)))
        for severity in SEVERITIES:
            serious_seen = state.serious_seen or severity in BACKSTOP
            finding = "open_" + severity
            edges.append(("review_finding_" + severity, a_open(state, reviews, finding, serious_seen, normal, reserve)))
        for severity in BACKSTOP:
            serious_seen = True
            finding = "pending_review_" + severity
            edges.append(("review_dismissed_" + severity, AState("recheck", reviews, 0, serious_seen, finding)))
    elif state.control == "repair":
        severity = severity_of(state.finding)
        edges.append(("repair_" + severity, AState("verify", state.reviews, 0, state.serious_seen, "repaired_" + severity)))
    elif state.control == "verify":
        reviews = state.reviews + 1
        old_severity = severity_of(state.finding)
        edges.append(("verify_pass_" + old_severity, a_settled(state, reviews, "none", need, normal, reserve)))
        edges.append(("verify_fail_" + old_severity, a_open(state, reviews, "open_" + old_severity, state.serious_seen, normal, reserve)))
        for severity in SEVERITIES:
            serious_seen = state.serious_seen or severity in BACKSTOP
            finding = "open_" + severity
            edges.append(("verify_pass_new_" + severity, a_open(state, reviews, finding, serious_seen, normal, reserve)))
        for severity in BACKSTOP:
            finding = "pending_verify_" + severity
            edges.append(("verify_pass_dismissed_" + severity, AState("recheck", reviews, 0, True, finding)))
    elif state.control == "recheck":
        severity = severity_of(state.finding)
        edges.append(("recheck_upheld_" + severity, a_settled(state, state.reviews, "dismissed_" + severity, need, normal, reserve)))
        edges.append(("recheck_overturned_" + severity, a_open(state, state.reviews, "open_" + severity, True, normal, reserve)))
    elif state.control in ("terminal", "serious_blocked"):
        severity = severity_of(state.finding)
        if state.control == "terminal" and not at_floor(severity):
            edges.append(("accept_residual", AState("delivered_residual", state.reviews, state.streak, state.serious_seen, "accepted_" + (severity or "none"))))
        for action in NON_DELIVERY:
            edges.append((action, AState("non_delivery", state.reviews, state.streak, state.serious_seen, action + "_" + (severity or "none"))))
    return edges


@dataclass(frozen=True)
class CState:
    control: str
    reviews: int
    finding: str
    return_stage: str


def c_terminal(reviews, finding):
    control = "serious_blocked" if at_floor(severity_of(finding)) else "terminal"
    return CState(control, reviews, finding, "none")


def c_settled(stage, reviews, risk):
    if stage == "discovery" and risk == "low_risk":
        return CState("complete", reviews, "none", "none")
    if stage == "blind_closure":
        return CState("complete", reviews, "none", "none")
    return CState("blind_closure", reviews, "none", "none")


def c_open(stage, reviews, finding):
    if stage == "discovery":
        return CState("repair1", reviews, finding, "none")
    if stage == "verify1":
        return CState("repair2", reviews, finding, "none")
    return c_terminal(reviews, finding)


def c_edges(state, risk):
    edges = []
    review_stages = ("discovery", "verify1", "verify2", "blind_closure")
    if state.control in review_stages:
        stage = state.control
        reviews = state.reviews + 1
        if stage.startswith("verify"):
            old_severity = severity_of(state.finding)
            edges.append(("verify_pass_" + old_severity, c_settled(stage, reviews, risk)))
            edges.append(("verify_fail_" + old_severity, c_open(stage, reviews, "open_" + old_severity)))
            for severity in SEVERITIES:
                edges.append(("verify_pass_new_" + severity, c_open(stage, reviews, "open_" + severity)))
            for severity in BACKSTOP:
                finding = "pending_" + stage + "_" + severity
                edges.append(("verify_pass_dismissed_" + severity, CState("recheck", reviews, finding, stage)))
        else:
            edges.append(("review_settled", c_settled(stage, reviews, risk)))
            for severity in SEVERITIES:
                edges.append(("review_finding_" + severity, c_open(stage, reviews, "open_" + severity)))
            for severity in BACKSTOP:
                finding = "pending_" + stage + "_" + severity
                edges.append(("review_dismissed_" + severity, CState("recheck", reviews, finding, stage)))
    elif state.control in ("repair1", "repair2"):
        generation = state.control[-1]
        severity = severity_of(state.finding)
        edges.append(("repair" + generation + "_" + severity, CState("verify" + generation, state.reviews, "repaired_" + severity, "none")))
    elif state.control == "recheck":
        severity = severity_of(state.finding)
        stage = state.return_stage
        edges.append(("recheck_upheld_" + severity, c_settled(stage, state.reviews, risk)))
        edges.append(("recheck_overturned_" + severity, c_open(stage, state.reviews, "open_" + severity)))
    elif state.control in ("terminal", "serious_blocked"):
        severity = severity_of(state.finding)
        if state.control == "terminal" and not at_floor(severity):
            edges.append(("accept_residual", CState("delivered_residual", state.reviews, "accepted_" + (severity or "none"), "none")))
        for action in NON_DELIVERY:
            edges.append((action, CState("non_delivery", state.reviews, action + "_" + (severity or "none"), "none")))
    return edges


@dataclass(frozen=True)
class BState:
    phase: str
    obligations: tuple
    reviews: int
    control: str
    finding: str


def b_all_closed(obligations):
    return all(value in ("closed0", "closed1") for value in obligations)


def replace(values, index, value):
    result = list(values)
    result[index] = value
    return tuple(result)


def b_terminal(state, finding):
    serious_open = at_floor(severity_of(finding)) or any(at_floor(severity_of(value)) and is_outstanding(value) for value in state.obligations)
    control = "serious_blocked" if serious_open else "terminal"
    return BState(state.phase, state.obligations, state.reviews, control, finding)


def b_dispose(obligations, action):
    result = []
    label = {
        "accept_residual": "accepted",
        "remove_delivery": "removed",
        "revert": "reverted",
        "replan": "carried",
        "abandon": "abandoned",
        "scope_digest_changed": "carried",
    }[action]
    for value in obligations:
        severity = severity_of(value)
        if is_outstanding(value):
            result.append(label + "_" + (severity or "unrated"))
        elif value == "untested":
            result.append(label + "_untested")
        else:
            result.append(value)
    return tuple(result)


def b_edges(state):
    edges = []
    if state.control == "active":
        limit = 4 * len(state.obligations) + 1
        active = [index for index, value in enumerate(state.obligations) if value.startswith(("open", "repaired", "pending"))]
        pending = [index for index, value in enumerate(state.obligations) if value.startswith("pending")]
        if state.reviews >= limit:
            permitted = {pending[0]} if pending else set()
        else:
            permitted = {active[0]} if active else set(range(len(state.obligations)))
        for index, value in enumerate(state.obligations):
            if index not in permitted:
                continue
            prefix = "o" + str(index + 1) + "_"
            if value == "untested":
                edges.append((prefix + "initial_clean", BState(state.phase, replace(state.obligations, index, "closed0"), state.reviews + 1, "active", "none")))
                for severity in SEVERITIES:
                    finding = "open0_" + severity
                    edges.append((prefix + "initial_finding_" + severity, BState(state.phase, replace(state.obligations, index, finding), state.reviews + 1, "active", finding)))
                for severity in BACKSTOP:
                    pending = "pending_initial_" + severity
                    edges.append((prefix + "initial_dismissed_" + severity, BState(state.phase, replace(state.obligations, index, pending), state.reviews + 1, "active", pending)))
            elif value.startswith("open0_"):
                severity = severity_of(value)
                repaired = "repaired0_" + severity
                edges.append((prefix + "repair_initial_" + severity, BState(state.phase, replace(state.obligations, index, repaired), state.reviews, "active", repaired)))
            elif value.startswith("repaired0_"):
                severity = severity_of(value)
                edges.append((prefix + "verify_initial_pass_" + severity, BState(state.phase, replace(state.obligations, index, "closed0"), state.reviews + 1, "active", "none")))
                failed = replace(state.obligations, index, "open0_" + severity)
                edges.append((prefix + "verify_initial_fail_" + severity, b_terminal(BState(state.phase, failed, state.reviews + 1, "active", "open0_" + severity), "open0_" + severity)))
                for new_severity in SEVERITIES:
                    failed = replace(state.obligations, index, "open0_" + new_severity)
                    candidate = BState(state.phase, failed, state.reviews + 1, "active", "open0_" + new_severity)
                    edges.append((prefix + "verify_initial_pass_new_" + new_severity, b_terminal(candidate, "open0_" + new_severity)))
                for dismissed_severity in BACKSTOP:
                    pending = "pending_verify0_" + dismissed_severity
                    edges.append((prefix + "verify_initial_pass_dismissed_" + dismissed_severity, BState(state.phase, replace(state.obligations, index, pending), state.reviews + 1, "active", pending)))
            elif value == "closed0":
                for severity in SEVERITIES:
                    reopened = "open1_" + severity
                    edges.append((prefix + "material_new_evidence_" + severity, BState(state.phase, replace(state.obligations, index, reopened), state.reviews + 1, "active", reopened)))
                for dismissed_severity in BACKSTOP:
                    pending = "pending_reopen_" + dismissed_severity
                    edges.append((prefix + "material_new_evidence_dismissed_" + dismissed_severity, BState(state.phase, replace(state.obligations, index, pending), state.reviews + 1, "active", pending)))
            elif value.startswith("open1_"):
                severity = severity_of(value)
                repaired = "repaired1_" + severity
                edges.append((prefix + "repair_reopen_" + severity, BState(state.phase, replace(state.obligations, index, repaired), state.reviews, "active", repaired)))
            elif value.startswith("repaired1_"):
                severity = severity_of(value)
                edges.append((prefix + "verify_reopen_pass_" + severity, BState(state.phase, replace(state.obligations, index, "closed1"), state.reviews + 1, "active", "none")))
                failed = replace(state.obligations, index, "open1_" + severity)
                edges.append((prefix + "verify_reopen_fail_" + severity, b_terminal(BState(state.phase, failed, state.reviews + 1, "active", "open1_" + severity), "open1_" + severity)))
                for new_severity in SEVERITIES:
                    failed = replace(state.obligations, index, "open1_" + new_severity)
                    candidate = BState(state.phase, failed, state.reviews + 1, "active", "open1_" + new_severity)
                    edges.append((prefix + "verify_reopen_pass_new_" + new_severity, b_terminal(candidate, "open1_" + new_severity)))
                for dismissed_severity in BACKSTOP:
                    pending = "pending_verify1_" + dismissed_severity
                    edges.append((prefix + "verify_reopen_pass_dismissed_" + dismissed_severity, BState(state.phase, replace(state.obligations, index, pending), state.reviews + 1, "active", pending)))
            elif value.startswith("pending_"):
                severity = severity_of(value)
                if value.startswith("pending_initial_"):
                    edges.append((prefix + "recheck_upheld_" + severity, BState(state.phase, replace(state.obligations, index, "closed0"), state.reviews, "active", "none")))
                    overturned = "open0_" + severity
                    edges.append((prefix + "recheck_overturned_" + severity, BState(state.phase, replace(state.obligations, index, overturned), state.reviews, "active", overturned)))
                elif value.startswith("pending_reopen_"):
                    edges.append((prefix + "recheck_upheld_" + severity, BState(state.phase, replace(state.obligations, index, "closed1"), state.reviews, "active", "none")))
                    overturned = "open1_" + severity
                    edges.append((prefix + "recheck_overturned_" + severity, BState(state.phase, replace(state.obligations, index, overturned), state.reviews, "active", overturned)))
                elif value.startswith("pending_verify0_"):
                    edges.append((prefix + "recheck_upheld_" + severity, BState(state.phase, replace(state.obligations, index, "closed0"), state.reviews, "active", "none")))
                    failed = replace(state.obligations, index, "open0_" + severity)
                    candidate = BState(state.phase, failed, state.reviews, "active", "open0_" + severity)
                    edges.append((prefix + "recheck_overturned_" + severity, b_terminal(candidate, "open0_" + severity)))
                elif value.startswith("pending_verify1_"):
                    edges.append((prefix + "recheck_upheld_" + severity, BState(state.phase, replace(state.obligations, index, "closed1"), state.reviews, "active", "none")))
                    failed = replace(state.obligations, index, "open1_" + severity)
                    candidate = BState(state.phase, failed, state.reviews, "active", "open1_" + severity)
                    edges.append((prefix + "recheck_overturned_" + severity, b_terminal(candidate, "open1_" + severity)))
        if state.reviews < limit and b_all_closed(state.obligations):
            edges.append(("blind_closure_clean", BState(state.phase, state.obligations, state.reviews + 1, "complete", "none")))
            for severity in SEVERITIES:
                finding = "open_blind_" + severity
                edges.append(("blind_closure_finding_" + severity, b_terminal(BState(state.phase, state.obligations, state.reviews + 1, "active", finding), finding)))
            for severity in BACKSTOP:
                finding = "pending_blind_" + severity
                edges.append(("blind_closure_dismissed_" + severity, BState(state.phase, state.obligations, state.reviews + 1, "recheck_blind", finding)))
        carried = b_dispose(state.obligations, "scope_digest_changed")
        edges.append(("scope_digest_changed", BState(state.phase, carried, state.reviews, "replanned", "carried")))
        serious_open = at_floor(severity_of(state.finding)) or any(at_floor(severity_of(value)) and is_outstanding(value) for value in state.obligations)
        exhausted_control = "serious_blocked" if serious_open else "exhausted"
        edges.append(("request_beyond_declared_authority", BState(state.phase, state.obligations, state.reviews, exhausted_control, state.finding)))
    elif state.control == "recheck_blind":
        severity = severity_of(state.finding)
        edges.append(("recheck_upheld_" + severity, BState(state.phase, state.obligations, state.reviews, "complete", "dismissed_" + severity)))
        finding = "open_blind_" + severity
        edges.append(("recheck_overturned_" + severity, b_terminal(BState(state.phase, state.obligations, state.reviews, "active", finding), finding)))
    elif state.control in ("terminal", "exhausted", "serious_blocked"):
        severity = severity_of(state.finding)
        serious_open = at_floor(severity) or any(at_floor(severity_of(value)) and is_outstanding(value) for value in state.obligations)
        pending = any(is_pending(value) for value in state.obligations)
        if state.control != "serious_blocked" and not serious_open and not pending:
            accepted = b_dispose(state.obligations, "accept_residual")
            edges.append(("accept_residual", BState(state.phase, accepted, state.reviews, "delivered_residual", "accepted_" + (severity or "none"))))
        for action in NON_DELIVERY:
            disposed = b_dispose(state.obligations, action)
            edges.append((action, BState(state.phase, disposed, state.reviews, "non_delivery", action + "_" + (severity or "none"))))
    return edges


def critical_keys(state):
    if isinstance(state, BState):
        keys = set()
        for index, value in enumerate(state.obligations):
            if is_critical(value) and is_outstanding(value):
                keys.add("o" + str(index + 1))
        if state.finding.startswith("open_blind_") and is_critical(state.finding):
            keys.add("blind")
        return keys
    if is_critical(state.finding) and is_outstanding(state.finding):
        return {"finding"}
    return set()


def has_pending(state):
    if isinstance(state, BState):
        return any(is_pending(value) for value in state.obligations)
    return is_pending(state.finding)


def walk(start, edge_function, delivery_controls, review_bound):
    queue = deque([start])
    seen = {start}
    edges = []
    max_reviews = 0
    bad_delivery = []
    bad_clear = []
    bad_bound = []
    while queue:
        state = queue.popleft()
        max_reviews = max(max_reviews, state.reviews)
        if state.reviews > review_bound:
            bad_bound.append(state)
        for action, target in edge_function(state):
            edges.append((state, action, target))
            cleared = critical_keys(state) - critical_keys(target)
            allowed_clear = action.startswith("verify_pass_") or "verify_initial_pass_" in action or "verify_reopen_pass_" in action or action.startswith("recheck_upheld_") or "recheck_upheld_" in action or action in NON_DELIVERY or action == "scope_digest_changed"
            if cleared and not allowed_clear:
                bad_clear.append((state, action, target))
            if target.control in delivery_controls:
                if critical_keys(target) or has_pending(target):
                    bad_delivery.append((state, action, target))
            if target not in seen:
                seen.add(target)
                queue.append(target)
    terminal = sum(1 for state in seen if not edge_function(state))
    indegree = {state: 0 for state in seen}
    adjacency = {state: set() for state in seen}
    for source, action, target in edges:
        if target not in adjacency[source]:
            adjacency[source].add(target)
            indegree[target] += 1
    ready = deque(state for state, degree in indegree.items() if degree == 0)
    removed = 0
    while ready:
        source = ready.popleft()
        removed += 1
        for target in adjacency[source]:
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)
    return {
        "states": len(seen),
        "edges": len(edges),
        "terminal": terminal,
        "acyclic": removed == len(seen),
        "max_reviews": max_reviews,
        "bad_delivery": len(bad_delivery),
        "bad_clear": len(bad_clear),
        "bad_bound": len(bad_bound),
    }


def check_a(phase, risk):
    need = 1 if phase == "acceptance" or risk == "low_risk" else 2
    start = AState("active", 0, 0, False, "none")
    result = walk(start, lambda state: a_edges(state, need, 5, 2), ("complete", "delivered_residual"), 7)
    print("A phase=%s risk=%s floor=%s normal=5 reserve=2 required=%d states=%d edges=%d terminal=%d acyclic=%s max_reviews=%d bad_delivery=%d bad_critical_clear=%d bad_bound=%d" % (
        phase,
        risk,
        FLOOR,
        need,
        result["states"],
        result["edges"],
        result["terminal"],
        str(result["acyclic"]).lower(),
        result["max_reviews"],
        result["bad_delivery"],
        result["bad_clear"],
        result["bad_bound"],
    ))


def check_c(phase, risk):
    start = CState("discovery", 0, "none", "none")
    result = walk(start, lambda state: c_edges(state, risk), ("complete", "delivered_residual"), 4)
    print("C phase=%s risk=%s floor=%s stages=4 repairs=2 states=%d edges=%d terminal=%d acyclic=%s max_reviews=%d bad_delivery=%d bad_critical_clear=%d bad_bound=%d" % (
        phase,
        risk,
        FLOOR,
        result["states"],
        result["edges"],
        result["terminal"],
        str(result["acyclic"]).lower(),
        result["max_reviews"],
        result["bad_delivery"],
        result["bad_clear"],
        result["bad_bound"],
    ))


def check_b(phase, obligations):
    start = BState(phase, tuple("untested" for _ in range(obligations)), 0, "active", "none")
    bound = 4 * obligations + 1
    result = walk(start, b_edges, ("complete", "delivered_residual"), bound)
    print("B phase=%s obligations=%d floor=%s bound=%d states=%d edges=%d terminal=%d acyclic=%s max_reviews=%d bad_delivery=%d bad_critical_clear=%d bad_bound=%d" % (
        phase,
        obligations,
        FLOOR,
        bound,
        result["states"],
        result["edges"],
        result["terminal"],
        str(result["acyclic"]).lower(),
        result["max_reviews"],
        result["bad_delivery"],
        result["bad_clear"],
        result["bad_bound"],
    ))


def main():
    global FLOOR
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("A", "B", "C", "all"), default="all")
    parser.add_argument("--phase", default="acceptance")
    parser.add_argument("--risk", choices=("low_risk", "risky"), default="risky")
    parser.add_argument("--obligations", type=int, default=2)
    parser.add_argument("--floor", choices=("high", "critical"), default="high")
    args = parser.parse_args()
    FLOOR = args.floor
    if args.mode in ("A", "all"):
        check_a(args.phase, args.risk)
    if args.mode in ("B", "all"):
        check_b(args.phase, args.obligations)
    if args.mode in ("C", "all"):
        check_c(args.phase, args.risk)


if __name__ == "__main__":
    main()
