#!/usr/bin/env python3
from collections import deque
from dataclasses import dataclass
from itertools import combinations_with_replacement
import argparse

SEVERITIES = ("low", "medium", "high", "critical")
BACKSTOP = ("high", "critical")
NON_DELIVERY = ("remove_delivery", "revert", "replan", "abandon")
TERMINAL_DISPOSITIONS = ("accepted_residual", "removed", "reverted", "carried", "abandoned")
OUTSTANDING = ("open", "pending_verification", "awaiting_recheck")
FLOOR = "high"
FINDING_CAP = 2


@dataclass(frozen=True, order=True)
class Finding:
    finding_id: int
    owner: str
    severity: str
    disposition: str
    origin: str
    parent_id: int


def rank(severity):
    return {"low": 1, "medium": 2, "high": 3, "critical": 4}[severity]


def at_floor(severity):
    return rank(severity) >= rank(FLOOR)


def is_outstanding(finding):
    return finding.disposition in OUTSTANDING


def is_pending_recheck(finding):
    return finding.disposition == "awaiting_recheck"


def update_findings(findings, predicate, disposition):
    return tuple(Finding(f.finding_id, f.owner, f.severity, disposition if predicate(f) else f.disposition, f.origin, f.parent_id) for f in findings)


def next_finding_id(findings):
    return 1 + max((f.finding_id for f in findings), default=0)


def severity_profiles(remaining, allowed=SEVERITIES):
    profiles = []
    for size in range(1, min(FINDING_CAP, remaining) + 1):
        profiles.extend(combinations_with_replacement(allowed, size))
    return tuple(profiles)


def profile_name(profile):
    return "_".join(profile)


def mint_profile(findings, profile, owner, origin, disposition="open", parent_id=0):
    result = list(findings)
    finding_id = next_finding_id(findings)
    for severity in profile:
        result.append(Finding(finding_id, owner, severity, disposition, origin, parent_id))
        finding_id += 1
    return tuple(result)


def open_findings(findings):
    return tuple(f for f in findings if f.disposition == "open")


def pending_verification_findings(findings):
    return tuple(f for f in findings if f.disposition == "pending_verification")


def outstanding_at_floor(findings):
    return any(is_outstanding(f) and at_floor(f.severity) for f in findings)


def has_pending_recheck(findings):
    return any(is_pending_recheck(f) for f in findings)


def all_settled(findings):
    return not any(is_outstanding(f) for f in findings)


def dispose_outstanding(findings, disposition):
    return update_findings(findings, is_outstanding, disposition)


def repair_joint(findings, owner=None):
    return update_findings(findings, lambda f: f.disposition == "open" and (owner is None or f.owner == owner), "pending_verification")


def verification_pass_joint(findings, owner=None):
    return update_findings(findings, lambda f: f.disposition == "pending_verification" and (owner is None or f.owner == owner), "resolved")


def verification_fail_joint(findings, owner=None):
    return update_findings(findings, lambda f: f.disposition == "pending_verification" and (owner is None or f.owner == owner), "open")


def dismissal_profiles(findings):
    return severity_profiles(FINDING_CAP - len(findings), BACKSTOP)


def terminal_control(findings):
    return "serious_blocked" if outstanding_at_floor(findings) else "terminal"


@dataclass(frozen=True)
class AState:
    control: str
    reviews: int
    streak: int
    serious_seen: bool
    findings: tuple


def a_limit(state, normal, reserve):
    return normal + reserve if state.serious_seen else normal


def a_settled(state, reviews, findings, need, normal, reserve):
    assert all_settled(findings)
    streak = state.streak + 1
    if streak >= need:
        return AState("complete", reviews, streak, state.serious_seen, findings)
    candidate = AState("active", reviews, streak, state.serious_seen, findings)
    if reviews >= a_limit(candidate, normal, reserve):
        return AState("terminal", reviews, streak, state.serious_seen, findings)
    return candidate


def a_open(state, reviews, findings, serious_seen, normal, reserve):
    assert any(f.disposition == "open" for f in findings)
    candidate = AState("repair", reviews, 0, serious_seen, findings)
    if reviews >= a_limit(candidate, normal, reserve):
        return AState(terminal_control(findings), reviews, 0, serious_seen, findings)
    return candidate


def a_edges(state, need, normal, reserve):
    edges = []
    if state.control == "active":
        if state.reviews >= a_limit(state, normal, reserve):
            edges.append(("authority_exhausted", AState("terminal", state.reviews, state.streak, state.serious_seen, state.findings)))
            return edges
        reviews = state.reviews + 1
        edges.append(("review_settled", a_settled(state, reviews, state.findings, need, normal, reserve)))
        for profile in severity_profiles(FINDING_CAP - len(state.findings)):
            findings = mint_profile(state.findings, profile, "phase", "pre_existing")
            serious_seen = state.serious_seen or any(severity in BACKSTOP for severity in profile)
            edges.append(("review_findings_" + profile_name(profile), a_open(state, reviews, findings, serious_seen, normal, reserve)))
        for profile in dismissal_profiles(state.findings):
            findings = mint_profile(state.findings, profile, "phase", "pre_existing", "awaiting_recheck")
            edges.append(("review_dismissed_" + profile_name(profile), AState("recheck", reviews, 0, state.serious_seen, findings)))
    elif state.control == "repair":
        findings = repair_joint(state.findings)
        assert pending_verification_findings(findings)
        edges.append(("repair_joint", AState("verify", state.reviews, 0, state.serious_seen, findings)))
    elif state.control == "verify":
        reviews = state.reviews + 1
        passed = verification_pass_joint(state.findings)
        edges.append(("verify_pass_joint", a_settled(state, reviews, passed, need, normal, reserve)))
        failed = verification_fail_joint(state.findings)
        edges.append(("verify_fail_joint", a_open(state, reviews, failed, state.serious_seen, normal, reserve)))
        parents = pending_verification_findings(state.findings)
        if parents and len(state.findings) < FINDING_CAP:
            for severity in SEVERITIES:
                with_child = mint_profile(failed, (severity,), "phase", "fix_induced", "open", parents[0].finding_id)
                serious_seen = state.serious_seen or severity in BACKSTOP
                edges.append(("verify_fail_with_child_" + severity, a_open(state, reviews, with_child, serious_seen, normal, reserve)))
        resolved = verification_pass_joint(state.findings)
        parent_id = parents[0].finding_id if parents else 0
        for profile in dismissal_profiles(resolved):
            findings = mint_profile(resolved, profile, "phase", "fix_induced", "awaiting_recheck", parent_id)
            edges.append(("verify_dismissed_" + profile_name(profile), AState("recheck", reviews, 0, state.serious_seen, findings)))
    elif state.control == "recheck":
        upheld = update_findings(state.findings, is_pending_recheck, "dismissed")
        edges.append(("recheck_upheld", a_settled(state, state.reviews, upheld, need, normal, reserve)))
        overturned = update_findings(state.findings, is_pending_recheck, "open")
        edges.append(("recheck_overturned", a_open(state, state.reviews, overturned, True, normal, reserve)))
    elif state.control in ("terminal", "serious_blocked"):
        if state.control == "terminal" and not outstanding_at_floor(state.findings) and not has_pending_recheck(state.findings):
            accepted = dispose_outstanding(state.findings, "accepted_residual")
            edges.append(("accept_residual", AState("delivered_residual", state.reviews, state.streak, state.serious_seen, accepted)))
        for action in NON_DELIVERY:
            disposed = dispose_outstanding(state.findings, {"remove_delivery": "removed", "revert": "reverted", "replan": "carried", "abandon": "abandoned"}[action])
            edges.append((action, AState("non_delivery", state.reviews, state.streak, state.serious_seen, disposed)))
    return edges


@dataclass(frozen=True)
class CState:
    control: str
    reviews: int
    findings: tuple
    return_stage: str


def c_terminal(reviews, findings):
    return CState(terminal_control(findings), reviews, findings, "none")


def c_settled(stage, reviews, findings, risk):
    assert all_settled(findings)
    if stage == "discovery" and risk == "low_risk":
        return CState("complete", reviews, findings, "none")
    if stage == "blind_closure":
        return CState("complete", reviews, findings, "none")
    return CState("blind_closure", reviews, findings, "none")


def c_open(stage, reviews, findings):
    assert any(f.disposition == "open" for f in findings)
    if stage == "discovery":
        return CState("repair1", reviews, findings, "none")
    if stage == "verify1":
        return CState("repair2", reviews, findings, "none")
    return c_terminal(reviews, findings)


def c_edges(state, risk):
    edges = []
    review_stages = ("discovery", "verify1", "verify2", "blind_closure")
    if state.control in review_stages:
        stage = state.control
        reviews = state.reviews + 1
        if stage.startswith("verify"):
            passed = verification_pass_joint(state.findings)
            edges.append(("verify_pass_joint", c_settled(stage, reviews, passed, risk)))
            failed = verification_fail_joint(state.findings)
            edges.append(("verify_fail_joint", c_open(stage, reviews, failed)))
            parents = pending_verification_findings(state.findings)
            if parents and len(state.findings) < FINDING_CAP:
                for severity in SEVERITIES:
                    with_child = mint_profile(failed, (severity,), "phase", "fix_induced", "open", parents[0].finding_id)
                    edges.append(("verify_fail_with_child_" + severity, c_open(stage, reviews, with_child)))
            resolved = verification_pass_joint(state.findings)
            parent_id = parents[0].finding_id if parents else 0
            for profile in dismissal_profiles(resolved):
                findings = mint_profile(resolved, profile, "phase", "fix_induced", "awaiting_recheck", parent_id)
                edges.append(("verify_dismissed_" + profile_name(profile), CState("recheck", reviews, findings, stage)))
        else:
            edges.append(("review_settled", c_settled(stage, reviews, state.findings, risk)))
            for profile in severity_profiles(FINDING_CAP - len(state.findings)):
                findings = mint_profile(state.findings, profile, "phase", "pre_existing")
                edges.append(("review_findings_" + profile_name(profile), c_open(stage, reviews, findings)))
            for profile in dismissal_profiles(state.findings):
                findings = mint_profile(state.findings, profile, "phase", "pre_existing", "awaiting_recheck")
                edges.append(("review_dismissed_" + profile_name(profile), CState("recheck", reviews, findings, stage)))
    elif state.control in ("repair1", "repair2"):
        findings = repair_joint(state.findings)
        edges.append((state.control + "_joint", CState("verify" + state.control[-1], state.reviews, findings, "none")))
    elif state.control == "recheck":
        upheld = update_findings(state.findings, is_pending_recheck, "dismissed")
        edges.append(("recheck_upheld", c_settled(state.return_stage, state.reviews, upheld, risk)))
        overturned = update_findings(state.findings, is_pending_recheck, "open")
        edges.append(("recheck_overturned", c_open(state.return_stage, state.reviews, overturned)))
    elif state.control in ("terminal", "serious_blocked"):
        if state.control == "terminal" and not outstanding_at_floor(state.findings) and not has_pending_recheck(state.findings):
            accepted = dispose_outstanding(state.findings, "accepted_residual")
            edges.append(("accept_residual", CState("delivered_residual", state.reviews, accepted, "none")))
        for action in NON_DELIVERY:
            disposed = dispose_outstanding(state.findings, {"remove_delivery": "removed", "revert": "reverted", "replan": "carried", "abandon": "abandoned"}[action])
            edges.append((action, CState("non_delivery", state.reviews, disposed, "none")))
    return edges


@dataclass(frozen=True)
class BState:
    phase: str
    obligations: tuple
    reviews: int
    control: str
    findings: tuple


def b_owner(index):
    return "o" + str(index + 1)


def b_all_closed(obligations):
    return all(value in ("closed0", "closed1") for value in obligations)


def replace(values, index, value):
    result = list(values)
    result[index] = value
    return tuple(result)


def b_terminal(state, findings=None):
    findings = state.findings if findings is None else findings
    return BState(state.phase, state.obligations, state.reviews, terminal_control(findings), findings)


def b_owner_update(findings, owner, source, target):
    return update_findings(findings, lambda f: f.owner == owner and f.disposition == source, target)


def b_dispose(findings, action):
    label = {"accept_residual": "accepted_residual", "remove_delivery": "removed", "revert": "reverted", "replan": "carried", "abandon": "abandoned", "scope_digest_changed": "carried"}[action]
    return dispose_outstanding(findings, label)


def b_unowned_edge(state, reviews, severity, action_prefix):
    findings = mint_profile(state.findings, (severity,), "unowned", "origin_indeterminate")
    candidate = BState(state.phase, state.obligations, reviews, "active", findings)
    return action_prefix + "_UnownedInScopeFinding_" + severity, b_terminal(candidate)


def b_valid_from_attempt(state, index, stage, reviews, profile, origin):
    owner = b_owner(index)
    findings = mint_profile(state.findings, profile, owner, origin)
    obligations = replace(state.obligations, index, stage)
    candidate = BState(state.phase, obligations, reviews, "active", findings)
    if reviews >= 4 * len(state.obligations) + 1:
        return b_terminal(candidate)
    return candidate


def b_dismissed_from_attempt(state, index, stage, reviews, profile, origin, parent_id=0):
    owner = b_owner(index)
    findings = mint_profile(state.findings, profile, owner, origin, "awaiting_recheck", parent_id)
    obligations = replace(state.obligations, index, stage)
    return BState(state.phase, obligations, reviews, "active", findings)


def b_attempt_edges(state, index, generation):
    edges = []
    owner = b_owner(index)
    limit = 4 * len(state.obligations) + 1
    reviews = state.reviews + 1
    prefix = owner + "_"
    if generation == 0:
        edges.append((prefix + "initial_clean", BState(state.phase, replace(state.obligations, index, "closed0"), reviews, "active", state.findings)))
        for profile in severity_profiles(FINDING_CAP - len(state.findings)):
            edges.append((prefix + "initial_findings_" + profile_name(profile), b_valid_from_attempt(state, index, "open0", reviews, profile, "pre_existing")))
        for profile in dismissal_profiles(state.findings):
            edges.append((prefix + "initial_dismissed_" + profile_name(profile), b_dismissed_from_attempt(state, index, "recheck_initial", reviews, profile, "pre_existing")))
    else:
        edges.append((prefix + "reopen_clean", BState(state.phase, replace(state.obligations, index, "closed1"), reviews, "active", state.findings)))
        settled_owner = tuple(f for f in state.findings if f.owner == owner and f.disposition in ("resolved", "dismissed"))
        if settled_owner:
            findings = update_findings(state.findings, lambda f: f.owner == owner and f.disposition in ("resolved", "dismissed"), "open")
            edges.append((prefix + "material_new_evidence_existing", BState(state.phase, replace(state.obligations, index, "open1"), reviews, "active", findings)))
        for profile in severity_profiles(FINDING_CAP - len(state.findings)):
            edges.append((prefix + "material_new_evidence_" + profile_name(profile), b_valid_from_attempt(state, index, "open1", reviews, profile, "reopened")))
        for profile in dismissal_profiles(state.findings):
            edges.append((prefix + "material_new_evidence_dismissed_" + profile_name(profile), b_dismissed_from_attempt(state, index, "recheck_reopen", reviews, profile, "reopened")))
    if len(state.findings) < FINDING_CAP:
        for severity in SEVERITIES:
            edges.append(b_unowned_edge(state, reviews, severity, prefix + ("initial" if generation == 0 else "reopen")))
    if reviews > limit:
        return []
    return edges


def b_repair_edges(state, index, generation):
    owner = b_owner(index)
    limit = 4 * len(state.obligations) + 1
    if state.reviews >= limit:
        return [(owner + "_authority_exhausted_before_verification", b_terminal(state))]
    findings = b_owner_update(state.findings, owner, "open", "pending_verification")
    obligations = replace(state.obligations, index, "pending" + str(generation))
    return [(owner + "_repair" + str(generation) + "_joint", BState(state.phase, obligations, state.reviews, "active", findings))]


def b_verify_edges(state, index, generation):
    edges = []
    owner = b_owner(index)
    reviews = state.reviews + 1
    next_closed = "closed" + str(generation)
    prefix = owner + "_verify" + str(generation) + "_"
    passed = b_owner_update(state.findings, owner, "pending_verification", "resolved")
    edges.append((prefix + "pass_joint", BState(state.phase, replace(state.obligations, index, next_closed), reviews, "active", passed)))
    failed = b_owner_update(state.findings, owner, "pending_verification", "open")
    failed_state = BState(state.phase, replace(state.obligations, index, "open" + str(generation)), reviews, "active", failed)
    edges.append((prefix + "fail_joint", b_terminal(failed_state)))
    parents = tuple(f for f in state.findings if f.owner == owner and f.disposition == "pending_verification")
    if parents and len(state.findings) < FINDING_CAP:
        for severity in SEVERITIES:
            with_child = mint_profile(failed, (severity,), owner, "fix_induced", "open", parents[0].finding_id)
            candidate = BState(state.phase, replace(state.obligations, index, "open" + str(generation)), reviews, "active", with_child)
            edges.append((prefix + "fail_with_child_" + severity, b_terminal(candidate)))
    parent_id = parents[0].finding_id if parents else 0
    for profile in dismissal_profiles(passed):
        stage = "recheck_verify" + str(generation)
        edges.append((prefix + "dismissed_" + profile_name(profile), b_dismissed_from_attempt(BState(state.phase, replace(state.obligations, index, next_closed), state.reviews, "active", passed), index, stage, reviews, profile, "fix_induced", parent_id)))
    if len(state.findings) < FINDING_CAP:
        for severity in SEVERITIES:
            edges.append(b_unowned_edge(state, reviews, severity, prefix))
    return edges


def b_recheck_edges(state, index, stage):
    owner = b_owner(index)
    generation = 1 if stage in ("recheck_reopen", "recheck_verify1") else 0
    upheld = b_owner_update(state.findings, owner, "awaiting_recheck", "dismissed")
    obligations = replace(state.obligations, index, "closed" + str(generation))
    edges = [(owner + "_recheck_upheld", BState(state.phase, obligations, state.reviews, "active", upheld))]
    overturned = b_owner_update(state.findings, owner, "awaiting_recheck", "open")
    if stage in ("recheck_initial", "recheck_reopen"):
        obligations = replace(state.obligations, index, "open" + str(generation))
        edges.append((owner + "_recheck_overturned", BState(state.phase, obligations, state.reviews, "active", overturned)))
    else:
        obligations = replace(state.obligations, index, "open" + str(generation))
        candidate = BState(state.phase, obligations, state.reviews, "active", overturned)
        edges.append((owner + "_recheck_overturned", b_terminal(candidate)))
    return edges


def b_blind_edges(state):
    edges = []
    reviews = state.reviews + 1
    edges.append(("blind_closure_clean", BState(state.phase, state.obligations, reviews, "complete", state.findings)))
    for profile in severity_profiles(FINDING_CAP - len(state.findings)):
        findings = mint_profile(state.findings, profile, "blind", "pre_existing")
        candidate = BState(state.phase, state.obligations, reviews, "active", findings)
        edges.append(("blind_closure_findings_" + profile_name(profile), b_terminal(candidate)))
    for profile in dismissal_profiles(state.findings):
        findings = mint_profile(state.findings, profile, "blind", "pre_existing", "awaiting_recheck")
        edges.append(("blind_closure_dismissed_" + profile_name(profile), BState(state.phase, state.obligations, reviews, "recheck_blind", findings)))
    if len(state.findings) < FINDING_CAP:
        for severity in SEVERITIES:
            edges.append(b_unowned_edge(state, reviews, severity, "blind_closure"))
    return edges


def b_edges(state):
    edges = []
    if state.control == "active":
        limit = 4 * len(state.obligations) + 1
        special = [index for index, value in enumerate(state.obligations) if value.startswith(("open", "pending", "recheck"))]
        if special:
            index = special[0]
            stage = state.obligations[index]
            if stage.startswith("open"):
                edges.extend(b_repair_edges(state, index, int(stage[-1])))
            elif stage.startswith("pending"):
                if state.reviews < limit:
                    edges.extend(b_verify_edges(state, index, int(stage[-1])))
                else:
                    edges.append((b_owner(index) + "_authority_exhausted", b_terminal(state)))
            else:
                edges.extend(b_recheck_edges(state, index, stage))
        else:
            untested = [index for index, value in enumerate(state.obligations) if value == "untested"]
            if untested and state.reviews < limit:
                edges.extend(b_attempt_edges(state, untested[0], 0))
            elif untested:
                edges.append(("authority_exhausted_with_untested", b_terminal(state)))
            elif state.reviews < limit and b_all_closed(state.obligations):
                closed0 = [index for index, value in enumerate(state.obligations) if value == "closed0"]
                if closed0:
                    edges.extend(b_attempt_edges(state, closed0[0], 1))
                edges.extend(b_blind_edges(state))
            else:
                edges.append(("authority_exhausted", b_terminal(state)))
        carried = b_dispose(state.findings, "scope_digest_changed")
        edges.append(("scope_digest_changed", BState(state.phase, state.obligations, state.reviews, "replanned", carried)))
    elif state.control == "recheck_blind":
        upheld = update_findings(state.findings, lambda f: f.owner == "blind" and is_pending_recheck(f), "dismissed")
        edges.append(("blind_recheck_upheld", BState(state.phase, state.obligations, state.reviews, "complete", upheld)))
        overturned = update_findings(state.findings, lambda f: f.owner == "blind" and is_pending_recheck(f), "open")
        edges.append(("blind_recheck_overturned", b_terminal(BState(state.phase, state.obligations, state.reviews, "active", overturned))))
    elif state.control in ("terminal", "serious_blocked"):
        no_untested = all(value != "untested" for value in state.obligations)
        if state.control == "terminal" and no_untested and not outstanding_at_floor(state.findings) and not has_pending_recheck(state.findings):
            accepted = b_dispose(state.findings, "accept_residual")
            edges.append(("accept_residual", BState(state.phase, state.obligations, state.reviews, "delivered_residual", accepted)))
        for action in NON_DELIVERY:
            disposed = b_dispose(state.findings, action)
            edges.append((action, BState(state.phase, state.obligations, state.reviews, "non_delivery", disposed)))
    return edges


@dataclass(frozen=True)
class LegacyState:
    control: str
    human_receipt: bool
    prospective_rows: int
    historical_round_credit: int


def legacy_edges(state):
    if state.control == "LegacyNoRubric":
        return [
            ("terminally_preserve_legacy_disposition", LegacyState("LegacyTerminal", True, 0, 0)),
            ("author_prospective_plan_review", LegacyState("ProspectivePlanReview", True, 0, 0)),
        ]
    if state.control == "ProspectivePlanReview":
        return [("freeze_new_prospective_rubric", LegacyState("ProspectiveFreeze", state.human_receipt, 1, 0))]
    if state.control == "ProspectiveFreeze":
        return [("enter_frozen_campaign", LegacyState("FrozenCampaignReady", state.human_receipt, state.prospective_rows, 0))]
    return []


@dataclass(frozen=True)
class Predecessor:
    family_id: str
    obligations: tuple
    exclusions: tuple
    terminal: bool


@dataclass(frozen=True)
class SuccessorReceipt:
    present: bool
    materially_different: bool


def successor_authorised(predecessor, obligations, exclusions, receipt):
    structured_delta = frozenset(predecessor.obligations) != frozenset(obligations) or frozenset(predecessor.exclusions) != frozenset(exclusions)
    return predecessor.terminal and receipt.present and receipt.materially_different and structured_delta


def findings_of(state):
    return getattr(state, "findings", ())


def critical_map(state):
    return {f.finding_id: f for f in findings_of(state) if f.severity == "critical" and is_outstanding(f)}


def legal_critical_clear(source_finding, target_finding, action):
    if target_finding is None:
        return False
    if source_finding.disposition == "pending_verification" and target_finding.disposition == "resolved" and "verify" in action and ("pass" in action or "dismissed" in action):
        return True
    if source_finding.disposition == "awaiting_recheck" and target_finding.disposition == "dismissed" and "recheck_upheld" in action:
        return True
    if target_finding.disposition in ("removed", "reverted", "carried", "abandoned") and (action in NON_DELIVERY or action == "scope_digest_changed"):
        return True
    return False


def delivery_is_verified(state):
    if any(is_outstanding(f) for f in findings_of(state)):
        return False
    if isinstance(state, BState):
        if any(value == "untested" for value in state.obligations):
            return False
        if state.control == "complete" and not b_all_closed(state.obligations):
            return False
    return True


def walk(start, edge_function, delivery_controls, review_bound):
    queue = deque([start])
    seen = {start}
    edges = []
    max_reviews = 0
    bad_delivery = []
    bad_unverified_delivery = []
    bad_clear = []
    bad_bound = []
    while queue:
        state = queue.popleft()
        max_reviews = max(max_reviews, state.reviews)
        if state.reviews > review_bound:
            bad_bound.append(state)
        for action, target in edge_function(state):
            edges.append((state, action, target))
            source_critical = critical_map(state)
            target_by_id = {f.finding_id: f for f in findings_of(target)}
            for finding_id, source_finding in source_critical.items():
                target_finding = target_by_id.get(finding_id)
                if target_finding is None or not is_outstanding(target_finding):
                    if not legal_critical_clear(source_finding, target_finding, action):
                        bad_clear.append((state, action, target, finding_id))
            if target.control in delivery_controls:
                if critical_map(target) or has_pending_recheck(findings_of(target)):
                    bad_delivery.append((state, action, target))
                if not delivery_is_verified(target):
                    bad_unverified_delivery.append((state, action, target))
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
    complete_reviews = [state.reviews for state in seen if state.control == "complete"]
    mixed = sum(1 for state in seen if {f.severity for f in findings_of(state) if is_outstanding(f)} >= {"low", "critical"})
    parent_child = 0
    for state in seen:
        by_id = {f.finding_id: f for f in findings_of(state)}
        if any(f.parent_id in by_id and is_outstanding(f) and is_outstanding(by_id[f.parent_id]) for f in findings_of(state) if f.parent_id):
            parent_child += 1
    return {
        "seen": seen,
        "edges_data": edges,
        "states": len(seen),
        "edges": len(edges),
        "terminal": terminal,
        "acyclic": removed == len(seen),
        "max_reviews": max_reviews,
        "min_complete_reviews": min(complete_reviews) if complete_reviews else -1,
        "bad_delivery": len(bad_delivery),
        "bad_unverified_delivery": len(bad_unverified_delivery),
        "bad_clear": len(bad_clear),
        "bad_clear_data": bad_clear,
        "bad_bound": len(bad_bound),
        "mixed": mixed,
        "parent_child": parent_child,
    }


def assert_common(result):
    assert result["acyclic"]
    assert result["bad_delivery"] == 0
    assert result["bad_unverified_delivery"] == 0
    assert result["bad_clear"] == 0
    assert result["bad_bound"] == 0
    assert result["mixed"] > 0
    assert result["parent_child"] > 0


def check_a(phase, risk):
    need = 1 if phase == "acceptance" or risk == "low_risk" else 2
    start = AState("active", 0, 0, False, ())
    result = walk(start, lambda state: a_edges(state, need, 5, 2), ("complete", "delivered_residual"), 7)
    assert_common(result)
    bad_upheld_unlock = sum(1 for source, action, target in result["edges_data"] if action == "recheck_upheld" and not source.serious_seen and target.serious_seen)
    assert bad_upheld_unlock == 0
    print("A phase=%s risk=%s floor=%s finding_cap=%d normal=5 reserve=2 required=%d states=%d edges=%d terminal=%d acyclic=%s min_reviews=%d max_reviews=%d mixed_low_critical=%d parent_child=%d bad_delivery=%d bad_unverified_delivery=%d bad_critical_clear=%d bad_bound=%d bad_upheld_unlock=%d" % (
        phase,
        risk,
        FLOOR,
        FINDING_CAP,
        need,
        result["states"],
        result["edges"],
        result["terminal"],
        str(result["acyclic"]).lower(),
        result["min_complete_reviews"],
        result["max_reviews"],
        result["mixed"],
        result["parent_child"],
        result["bad_delivery"],
        result["bad_unverified_delivery"],
        result["bad_clear"],
        result["bad_bound"],
        bad_upheld_unlock,
    ))


def check_c(phase, risk):
    start = CState("discovery", 0, (), "none")
    result = walk(start, lambda state: c_edges(state, risk), ("complete", "delivered_residual"), 4)
    assert_common(result)
    print("C phase=%s risk=%s floor=%s finding_cap=%d stages=4 repairs=2 states=%d edges=%d terminal=%d acyclic=%s min_reviews=%d max_reviews=%d mixed_low_critical=%d parent_child=%d bad_delivery=%d bad_unverified_delivery=%d bad_critical_clear=%d bad_bound=%d" % (
        phase,
        risk,
        FLOOR,
        FINDING_CAP,
        result["states"],
        result["edges"],
        result["terminal"],
        str(result["acyclic"]).lower(),
        result["min_complete_reviews"],
        result["max_reviews"],
        result["mixed"],
        result["parent_child"],
        result["bad_delivery"],
        result["bad_unverified_delivery"],
        result["bad_clear"],
        result["bad_bound"],
    ))


def check_legacy():
    start = LegacyState("LegacyNoRubric", False, 0, 0)
    queue = deque([start])
    seen = {start}
    edges = []
    while queue:
        state = queue.popleft()
        for action, target in legacy_edges(state):
            edges.append((state, action, target))
            if target not in seen:
                seen.add(target)
                queue.append(target)
    direct_campaign = sum(1 for source, action, target in edges if source.control == "LegacyNoRubric" and target.control == "FrozenCampaignReady")
    historical_credit = sum(1 for state in seen if state.control == "FrozenCampaignReady" and state.historical_round_credit != 0)
    zero_obligation = sum(1 for state in seen if state.control == "FrozenCampaignReady" and state.prospective_rows == 0)
    assert direct_campaign == 0
    assert historical_credit == 0
    assert zero_obligation == 0
    print("B legacy states=%d edges=%d legal_start_paths=2 bad_direct_campaign=%d bad_historical_credit=%d bad_zero_obligation=%d" % (len(seen), len(edges), direct_campaign, historical_credit, zero_obligation))


def check_successor():
    predecessor = Predecessor("F1", ("O1", "O2"), (), True)
    unchanged = (predecessor.family_id, predecessor.obligations, predecessor.exclusions, predecessor.terminal)
    receipt = SuccessorReceipt(True, True)
    missing = SuccessorReceipt(False, True)
    accepted_different = successor_authorised(predecessor, ("O1", "O2", "O3"), (), receipt)
    accepted_same = successor_authorised(predecessor, predecessor.obligations, predecessor.exclusions, receipt)
    accepted_reordered = successor_authorised(predecessor, ("O2", "O1"), (), receipt)
    accepted_missing_receipt = successor_authorised(predecessor, ("O1", "O2", "O3"), (), missing)
    predecessor_immutable = unchanged == (predecessor.family_id, predecessor.obligations, predecessor.exclusions, predecessor.terminal)
    assert accepted_different
    assert not accepted_same
    assert not accepted_reordered
    assert not accepted_missing_receipt
    assert predecessor_immutable
    print("B successor structured_cases=4 accepted_different=%s bad_same_scope=%d bad_reordered_scope=%d bad_missing_receipt=%d bad_predecessor_mutation=%d" % (str(accepted_different).lower(), int(accepted_same), int(accepted_reordered), int(accepted_missing_receipt), int(not predecessor_immutable)))


def check_b(phase, obligations):
    start = BState(phase, tuple("untested" for _ in range(obligations)), 0, "active", ())
    bound = 4 * obligations + 1
    result = walk(start, b_edges, ("complete", "delivered_residual"), bound)
    assert result["acyclic"]
    assert result["bad_delivery"] == 0
    assert result["bad_unverified_delivery"] == 0
    assert result["bad_clear"] == 0
    assert result["bad_bound"] == 0
    if obligations > 0:
        assert result["mixed"] > 0
        assert result["parent_child"] > 0
    bad_reopen_before_initial = sum(1 for source, action, target in result["edges_data"] if ("material_new_evidence" in action or "reopen_clean" in action) and "untested" in source.obligations)
    unowned_critical_states = sum(1 for state in result["seen"] if any(f.owner == "unowned" and f.severity == "critical" and is_outstanding(f) for f in state.findings))
    unowned_critical_delivery = sum(1 for state in result["seen"] if state.control in ("complete", "delivered_residual") and any(f.owner == "unowned" and f.severity == "critical" for f in state.findings))
    assert bad_reopen_before_initial == 0
    if obligations > 0:
        assert unowned_critical_states > 0
    assert unowned_critical_delivery == 0
    print("B phase=%s obligations=%d floor=%s finding_cap=%d bound=%d states=%d edges=%d terminal=%d acyclic=%s min_reviews=%d max_reviews=%d mixed_low_critical=%d parent_child=%d unowned_critical=%d bad_unowned_critical_delivery=%d bad_reopen_before_initial=%d bad_delivery=%d bad_unverified_delivery=%d bad_critical_clear=%d bad_bound=%d" % (
        phase,
        obligations,
        FLOOR,
        FINDING_CAP,
        bound,
        result["states"],
        result["edges"],
        result["terminal"],
        str(result["acyclic"]).lower(),
        result["min_complete_reviews"],
        result["max_reviews"],
        result["mixed"],
        result["parent_child"],
        unowned_critical_states,
        unowned_critical_delivery,
        bad_reopen_before_initial,
        result["bad_delivery"],
        result["bad_unverified_delivery"],
        result["bad_clear"],
        result["bad_bound"],
    ))


def main():
    global FLOOR
    global FINDING_CAP
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("A", "B", "C", "all"), default="all")
    parser.add_argument("--phase", default="acceptance")
    parser.add_argument("--risk", choices=("low_risk", "risky"), default="risky")
    parser.add_argument("--obligations", type=int, default=2)
    parser.add_argument("--floor", choices=("high", "critical"), default="high")
    parser.add_argument("--finding-cap", type=int, choices=(2,), default=2)
    args = parser.parse_args()
    FLOOR = args.floor
    FINDING_CAP = args.finding_cap
    if args.mode in ("A", "all"):
        check_a(args.phase, args.risk)
    if args.mode in ("B", "all"):
        check_b(args.phase, args.obligations)
    if args.mode == "all":
        check_legacy()
        check_successor()
    if args.mode in ("C", "all"):
        check_c(args.phase, args.risk)


if __name__ == "__main__":
    main()
