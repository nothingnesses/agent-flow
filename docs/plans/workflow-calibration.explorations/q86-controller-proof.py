#!/usr/bin/env python3
"""Adversarial prototype retained as evidence, not a safety or recommendation-eligibility proof.

Zero-valued controls and counts do not establish eligibility. See the Prototype boundary in `docs/plans/workflow-calibration.explorations/Q-86-synthesis.md` and the round-5 triage at `docs/plans/agent-scaffold.reviews/q86-synthesis-r5-triage.md`.
"""

from collections import deque
from dataclasses import dataclass, replace as dc_replace
from itertools import combinations_with_replacement, product
from hashlib import sha256
import argparse

SEVERITIES = ("low", "medium", "high", "critical")
BACKSTOP = ("high", "critical")
NON_DELIVERY = ("remove_delivery", "revert", "replan", "abandon")
TERMINAL_DISPOSITIONS = ("accepted_residual", "removed", "reverted", "carried", "abandoned")
OUTSTANDING = ("open", "pending_verification", "awaiting_recheck", "awaiting_scope_recheck")
FLOOR = "high"
FINDING_CAP = 2


@dataclass(frozen=True, order=True)
class ScopeRelation:
    kind: str
    identity: str


IN_SCOPE = ScopeRelation("in_scope", "frozen_scope")
SCOPE_EXPANDED = ScopeRelation("scope_expanded", "scope_delta")


@dataclass(frozen=True, order=True)
class Finding:
    finding_id: int
    owner: str
    severity: str
    disposition: str
    origin: str
    parent_id: int
    scope_relation: ScopeRelation = IN_SCOPE
    evidence_id: int = 0


def rank(severity):
    return {"low": 1, "medium": 2, "high": 3, "critical": 4}[severity]


def at_floor(severity):
    return rank(severity) >= rank(FLOOR)


def is_outstanding(finding):
    return finding.disposition in OUTSTANDING


def is_pending_recheck(finding):
    return finding.disposition == "awaiting_recheck"


def is_pending_scope_recheck(finding):
    return finding.disposition == "awaiting_scope_recheck"


def update_findings(findings, predicate, disposition):
    return tuple(Finding(f.finding_id, f.owner, f.severity, disposition if predicate(f) else f.disposition, f.origin, f.parent_id, f.scope_relation, f.evidence_id) for f in findings)


def update_scope(findings, predicate, scope_relation):
    return tuple(Finding(f.finding_id, f.owner, f.severity, f.disposition, f.origin, f.parent_id, scope_relation if predicate(f) else f.scope_relation, f.evidence_id) for f in findings)


def next_finding_id(findings):
    return 1 + max((f.finding_id for f in findings), default=0)


def severity_profiles(remaining, allowed=SEVERITIES):
    profiles = []
    for size in range(1, min(FINDING_CAP, remaining) + 1):
        profiles.extend(combinations_with_replacement(allowed, size))
    return tuple(profiles)


def mixed_disposition_profiles(remaining):
    if remaining < 2:
        return ()
    return tuple(product(SEVERITIES, BACKSTOP))


def profile_name(profile):
    return "_".join(profile)


def mint_profile(findings, profile, owner, origin, disposition="open", parent_id=0, scope_relation=IN_SCOPE):
    result = list(findings)
    finding_id = next_finding_id(findings)
    for severity in profile:
        result.append(Finding(finding_id, owner, severity, disposition, origin, parent_id, scope_relation, finding_id))
        finding_id += 1
    return tuple(result)


def mint_mixed_disposition(findings, valid_severity, dismissed_severity, owner, origin, parent_id=0):
    with_valid = mint_profile(findings, (valid_severity,), owner, origin, "open", parent_id)
    return mint_profile(with_valid, (dismissed_severity,), owner, origin, "awaiting_recheck", parent_id)


def mint_scope_expansion(findings, severity, owner, origin, disposition):
    return mint_profile(findings, (severity,), owner, origin, disposition, 0, SCOPE_EXPANDED)


def open_findings(findings):
    return tuple(f for f in findings if f.disposition == "open")


def pending_verification_findings(findings):
    return tuple(f for f in findings if f.disposition == "pending_verification")


def outstanding_at_floor(findings):
    return any(is_outstanding(f) and at_floor(f.severity) for f in findings)


def has_pending_recheck(findings):
    return any(is_pending_recheck(f) for f in findings)


def has_pending_scope_recheck(findings):
    return any(is_pending_scope_recheck(f) for f in findings)


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


def a_clean_needed(state, need):
    return max(0, need - state.streak) if state.control == "active" else need


def a_cannot_complete(state, need, normal, reserve):
    return a_limit(state, normal, reserve) - state.reviews < a_clean_needed(state, need)


def a_settled(state, reviews, findings, need, normal, reserve):
    assert all_settled(findings)
    streak = state.streak + 1
    if streak >= need:
        return AState("complete", reviews, streak, state.serious_seen, findings)
    candidate = AState("active", reviews, streak, state.serious_seen, findings)
    if a_cannot_complete(candidate, need, normal, reserve):
        return AState("terminal", reviews, streak, state.serious_seen, findings)
    return candidate


def a_open(state, reviews, findings, serious_seen, need, normal, reserve):
    assert any(f.disposition == "open" for f in findings)
    candidate = AState("repair", reviews, 0, serious_seen, findings)
    if a_cannot_complete(candidate, need, normal, reserve):
        return AState(terminal_control(findings), reviews, 0, serious_seen, findings)
    return candidate


def a_dismissal_recheck_edges(state, need, normal, reserve):
    upheld = update_findings(state.findings, is_pending_recheck, "dismissed")
    if any(f.disposition == "open" for f in upheld):
        upheld_target = a_open(state, state.reviews, upheld, state.serious_seen, need, normal, reserve)
    else:
        upheld_target = a_settled(state, state.reviews, upheld, need, normal, reserve)
    overturned = update_findings(state.findings, is_pending_recheck, "open")
    serious_seen = state.serious_seen or any(f.disposition == "open" and f.severity in BACKSTOP for f in overturned)
    overturned_target = a_open(state, state.reviews, overturned, serious_seen, need, normal, reserve)
    return [("dismissal_recheck_upheld", upheld_target), ("dismissal_recheck_overturned", overturned_target)]


def a_scope_recheck_edges(state, need, normal, reserve):
    referral = next(f for f in state.findings if is_pending_scope_recheck(f))
    if referral.severity == "high":
        upheld = update_findings(state.findings, is_pending_scope_recheck, "scope_terminal")
        upheld_target = AState("terminal_scope_decision", state.reviews, state.streak, state.serious_seen, upheld)
        overturned = update_findings(state.findings, is_pending_scope_recheck, "open")
        overturned = update_scope(overturned, lambda f: f.finding_id == referral.finding_id, IN_SCOPE)
        overturned_target = a_open(state, state.reviews, overturned, True, need, normal, reserve)
    else:
        upheld = update_findings(state.findings, is_pending_scope_recheck, "open")
        upheld_target = AState("serious_blocked", state.reviews, state.streak, state.serious_seen, upheld)
        overturned = update_findings(state.findings, is_pending_scope_recheck, "open")
        overturned = update_scope(overturned, lambda f: f.finding_id == referral.finding_id, IN_SCOPE)
        overturned_target = AState("serious_blocked", state.reviews, state.streak, True, overturned)
    return [("scope_recheck_upheld", upheld_target), ("scope_recheck_overturned", overturned_target)]


def a_scope_review_edges(state, reviews, need, normal, reserve, origin):
    if len(state.findings) >= FINDING_CAP:
        return []
    edges = []
    for severity in SEVERITIES:
        if severity == "low":
            findings = mint_scope_expansion(state.findings, severity, "phase", origin, "backlogged")
            target = a_settled(state, reviews, findings, need, normal, reserve)
        elif severity == "medium":
            findings = mint_scope_expansion(state.findings, severity, "phase", origin, "scope_terminal")
            target = AState("terminal_scope_decision", reviews, state.streak, state.serious_seen, findings)
        else:
            findings = mint_scope_expansion(state.findings, severity, "phase", origin, "awaiting_scope_recheck")
            target = AState(state.control, reviews, state.streak, state.serious_seen, findings)
        prefix = "verify_pass_with_" if state.control == "verify" else ""
        edges.append((prefix + "scope_expanded_" + severity, target))
    return edges


def a_edges(state, need, normal, reserve):
    if has_pending_scope_recheck(state.findings):
        return a_scope_recheck_edges(state, need, normal, reserve)
    if has_pending_recheck(state.findings):
        return a_dismissal_recheck_edges(state, need, normal, reserve)
    edges = []
    if state.control == "active":
        if a_cannot_complete(state, need, normal, reserve):
            edges.append(("foreclose_before_review", AState("terminal", state.reviews, state.streak, state.serious_seen, state.findings)))
            return edges
        reviews = state.reviews + 1
        edges.append(("review_settled", a_settled(state, reviews, state.findings, need, normal, reserve)))
        for profile in severity_profiles(FINDING_CAP - len(state.findings)):
            findings = mint_profile(state.findings, profile, "phase", "pre_existing")
            serious_seen = state.serious_seen or any(severity in BACKSTOP for severity in profile)
            edges.append(("review_findings_" + profile_name(profile), a_open(state, reviews, findings, serious_seen, need, normal, reserve)))
        for profile in dismissal_profiles(state.findings):
            findings = mint_profile(state.findings, profile, "phase", "pre_existing", "awaiting_recheck")
            edges.append(("review_dismissed_" + profile_name(profile), AState("active", reviews, state.streak, state.serious_seen, findings)))
        for valid_severity, dismissed_severity in mixed_disposition_profiles(FINDING_CAP - len(state.findings)):
            findings = mint_mixed_disposition(state.findings, valid_severity, dismissed_severity, "phase", "pre_existing")
            serious_seen = state.serious_seen or valid_severity in BACKSTOP
            edges.append(("review_mixed_" + valid_severity + "_dismissed_" + dismissed_severity, AState("active", reviews, 0, serious_seen, findings)))
        edges.extend(a_scope_review_edges(state, reviews, need, normal, reserve, "pre_existing"))
    elif state.control == "repair":
        if a_cannot_complete(state, need, normal, reserve):
            edges.append(("foreclose_before_repair", AState(terminal_control(state.findings), state.reviews, 0, state.serious_seen, state.findings)))
            return edges
        findings = repair_joint(state.findings)
        assert pending_verification_findings(findings)
        edges.append(("repair_joint", AState("verify", state.reviews, 0, state.serious_seen, findings)))
    elif state.control == "verify":
        if a_cannot_complete(state, need, normal, reserve):
            edges.append(("foreclose_before_verification", AState(terminal_control(state.findings), state.reviews, 0, state.serious_seen, state.findings)))
            return edges
        reviews = state.reviews + 1
        passed = verification_pass_joint(state.findings)
        edges.append(("verify_pass_joint", a_settled(state, reviews, passed, need, normal, reserve)))
        failed = verification_fail_joint(state.findings)
        edges.append(("verify_fail_joint", a_open(state, reviews, failed, state.serious_seen, need, normal, reserve)))
        parents = pending_verification_findings(state.findings)
        if len(failed) < FINDING_CAP:
            parent_id = parents[0].finding_id if parents else 0
            for dismissed_severity in BACKSTOP:
                mixed = mint_profile(failed, (dismissed_severity,), "phase", "fix_induced", "awaiting_recheck", parent_id)
                edges.append(("verify_fail_with_dismissed_" + dismissed_severity, AState("verify", reviews, 0, state.serious_seen, mixed)))
        if parents and len(state.findings) < FINDING_CAP:
            for severity in SEVERITIES:
                with_child = mint_profile(failed, (severity,), "phase", "fix_induced", "open", parents[0].finding_id)
                serious_seen = state.serious_seen or severity in BACKSTOP
                edges.append(("verify_fail_with_child_" + severity, a_open(state, reviews, with_child, serious_seen, need, normal, reserve)))
        resolved = verification_pass_joint(state.findings)
        parent_id = parents[0].finding_id if parents else 0
        for profile in dismissal_profiles(resolved):
            findings = mint_profile(resolved, profile, "phase", "fix_induced", "awaiting_recheck", parent_id)
            edges.append(("verify_dismissed_" + profile_name(profile), AState("verify", reviews, state.streak, state.serious_seen, findings)))
        for valid_severity, dismissed_severity in mixed_disposition_profiles(FINDING_CAP - len(resolved)):
            findings = mint_mixed_disposition(resolved, valid_severity, dismissed_severity, "phase", "fix_induced", parent_id)
            serious_seen = state.serious_seen or valid_severity in BACKSTOP
            edges.append(("verify_mixed_" + valid_severity + "_dismissed_" + dismissed_severity, AState("verify", reviews, 0, serious_seen, findings)))
        edges.extend(a_scope_review_edges(AState("verify", state.reviews, state.streak, state.serious_seen, resolved), reviews, need, normal, reserve, "fix_induced"))
    elif state.control in ("terminal", "serious_blocked"):
        if state.control == "terminal" and not outstanding_at_floor(state.findings) and not has_pending_recheck(state.findings) and not has_pending_scope_recheck(state.findings):
            accepted = dispose_outstanding(state.findings, "accepted_residual")
            edges.append(("accept_residual", AState("delivered_residual", state.reviews, state.streak, state.serious_seen, accepted)))
        for action in NON_DELIVERY:
            disposed = dispose_outstanding(state.findings, {"remove_delivery": "removed", "revert": "reverted", "replan": "carried", "abandon": "abandoned"}[action])
            edges.append((action, AState("non_delivery", state.reviews, state.streak, state.serious_seen, disposed)))
    return edges


@dataclass(frozen=True)
class CState:
    phase: str
    control: str
    reviews: int
    findings: tuple
    return_stage: str
    blind_visited: bool


def c_terminal(state, reviews, findings):
    return CState(state.phase, terminal_control(findings), reviews, findings, "none", state.blind_visited)


def c_settled(state, stage, reviews, findings, risk):
    assert all_settled(findings)
    if stage == "discovery" and risk == "low_risk" and state.phase != "acceptance":
        return CState(state.phase, "complete", reviews, findings, "none", state.blind_visited)
    if stage == "blind_closure":
        return CState(state.phase, "complete", reviews, findings, "none", True)
    return CState(state.phase, "blind_closure", reviews, findings, "none", state.blind_visited)


def c_open(state, stage, reviews, findings):
    assert any(f.disposition == "open" for f in findings)
    if stage == "discovery":
        return CState(state.phase, "repair1", reviews, findings, "none", state.blind_visited)
    if stage == "verify1":
        return CState(state.phase, "repair2", reviews, findings, "none", state.blind_visited)
    return c_terminal(state, reviews, findings)


def c_dismissal_recheck_edges(state, risk):
    upheld = update_findings(state.findings, is_pending_recheck, "dismissed")
    if any(f.disposition == "open" for f in upheld):
        upheld_target = c_open(state, state.return_stage, state.reviews, upheld)
    else:
        upheld_target = c_settled(state, state.return_stage, state.reviews, upheld, risk)
    overturned = update_findings(state.findings, is_pending_recheck, "open")
    overturned_target = c_open(state, state.return_stage, state.reviews, overturned)
    return [("dismissal_recheck_upheld", upheld_target), ("dismissal_recheck_overturned", overturned_target)]


def c_scope_recheck_edges(state):
    referral = next(f for f in state.findings if is_pending_scope_recheck(f))
    if referral.severity == "high":
        upheld = update_findings(state.findings, is_pending_scope_recheck, "scope_terminal")
        upheld_target = CState(state.phase, "terminal_scope_decision", state.reviews, upheld, "none", state.blind_visited)
        overturned = update_findings(state.findings, is_pending_scope_recheck, "open")
        overturned = update_scope(overturned, lambda f: f.finding_id == referral.finding_id, IN_SCOPE)
        overturned_target = c_open(state, state.return_stage, state.reviews, overturned)
    else:
        upheld = update_findings(state.findings, is_pending_scope_recheck, "open")
        upheld_target = CState(state.phase, "serious_blocked", state.reviews, upheld, "none", state.blind_visited)
        overturned = update_findings(state.findings, is_pending_scope_recheck, "open")
        overturned = update_scope(overturned, lambda f: f.finding_id == referral.finding_id, IN_SCOPE)
        overturned_target = CState(state.phase, "serious_blocked", state.reviews, overturned, "none", state.blind_visited)
    return [("scope_recheck_upheld", upheld_target), ("scope_recheck_overturned", overturned_target)]


def c_scope_review_edges(state, stage, reviews, risk, origin):
    if len(state.findings) >= FINDING_CAP:
        return []
    edges = []
    for severity in SEVERITIES:
        if severity == "low":
            findings = mint_scope_expansion(state.findings, severity, "phase", origin, "backlogged")
            target = c_settled(state, stage, reviews, findings, risk)
        elif severity == "medium":
            findings = mint_scope_expansion(state.findings, severity, "phase", origin, "scope_terminal")
            target = CState(state.phase, "terminal_scope_decision", reviews, findings, "none", state.blind_visited)
        else:
            findings = mint_scope_expansion(state.findings, severity, "phase", origin, "awaiting_scope_recheck")
            target = CState(state.phase, state.control, reviews, findings, stage, state.blind_visited)
        prefix = "verify_pass_with_" if stage.startswith("verify") else ""
        edges.append((prefix + "scope_expanded_" + severity, target))
    return edges


def c_edges(state, risk):
    if has_pending_scope_recheck(state.findings):
        return c_scope_recheck_edges(state)
    if has_pending_recheck(state.findings):
        return c_dismissal_recheck_edges(state, risk)
    edges = []
    review_stages = ("discovery", "verify1", "verify2", "blind_closure")
    if state.control in review_stages:
        stage = state.control
        reviews = state.reviews + 1
        if stage.startswith("verify"):
            passed = verification_pass_joint(state.findings)
            edges.append(("verify_pass_joint", c_settled(state, stage, reviews, passed, risk)))
            failed = verification_fail_joint(state.findings)
            edges.append(("verify_fail_joint", c_open(state, stage, reviews, failed)))
            parents = pending_verification_findings(state.findings)
            if len(failed) < FINDING_CAP:
                parent_id = parents[0].finding_id if parents else 0
                for dismissed_severity in BACKSTOP:
                    mixed = mint_profile(failed, (dismissed_severity,), "phase", "fix_induced", "awaiting_recheck", parent_id)
                    edges.append(("verify_fail_with_dismissed_" + dismissed_severity, CState(state.phase, state.control, reviews, mixed, stage, state.blind_visited)))
            if parents and len(state.findings) < FINDING_CAP:
                for severity in SEVERITIES:
                    with_child = mint_profile(failed, (severity,), "phase", "fix_induced", "open", parents[0].finding_id)
                    edges.append(("verify_fail_with_child_" + severity, c_open(state, stage, reviews, with_child)))
            resolved = verification_pass_joint(state.findings)
            parent_id = parents[0].finding_id if parents else 0
            for profile in dismissal_profiles(resolved):
                findings = mint_profile(resolved, profile, "phase", "fix_induced", "awaiting_recheck", parent_id)
                edges.append(("verify_dismissed_" + profile_name(profile), CState(state.phase, state.control, reviews, findings, stage, state.blind_visited)))
            for valid_severity, dismissed_severity in mixed_disposition_profiles(FINDING_CAP - len(resolved)):
                findings = mint_mixed_disposition(resolved, valid_severity, dismissed_severity, "phase", "fix_induced", parent_id)
                edges.append(("verify_mixed_" + valid_severity + "_dismissed_" + dismissed_severity, CState(state.phase, state.control, reviews, findings, stage, state.blind_visited)))
            edges.extend(c_scope_review_edges(CState(state.phase, state.control, state.reviews, resolved, stage, state.blind_visited), stage, reviews, risk, "fix_induced"))
        else:
            edges.append(("review_settled", c_settled(state, stage, reviews, state.findings, risk)))
            for profile in severity_profiles(FINDING_CAP - len(state.findings)):
                findings = mint_profile(state.findings, profile, "phase", "pre_existing")
                edges.append(("review_findings_" + profile_name(profile), c_open(state, stage, reviews, findings)))
            for profile in dismissal_profiles(state.findings):
                findings = mint_profile(state.findings, profile, "phase", "pre_existing", "awaiting_recheck")
                edges.append(("review_dismissed_" + profile_name(profile), CState(state.phase, state.control, reviews, findings, stage, state.blind_visited)))
            for valid_severity, dismissed_severity in mixed_disposition_profiles(FINDING_CAP - len(state.findings)):
                findings = mint_mixed_disposition(state.findings, valid_severity, dismissed_severity, "phase", "pre_existing")
                edges.append(("review_mixed_" + valid_severity + "_dismissed_" + dismissed_severity, CState(state.phase, state.control, reviews, findings, stage, state.blind_visited)))
            edges.extend(c_scope_review_edges(state, stage, reviews, risk, "pre_existing"))
    elif state.control in ("repair1", "repair2"):
        findings = repair_joint(state.findings)
        edges.append((state.control + "_joint", CState(state.phase, "verify" + state.control[-1], state.reviews, findings, "none", state.blind_visited)))
    elif state.control in ("terminal", "serious_blocked"):
        if state.control == "terminal" and not outstanding_at_floor(state.findings) and not has_pending_recheck(state.findings) and not has_pending_scope_recheck(state.findings):
            accepted = dispose_outstanding(state.findings, "accepted_residual")
            edges.append(("accept_residual", CState(state.phase, "delivered_residual", state.reviews, accepted, "none", state.blind_visited)))
        for action in NON_DELIVERY:
            disposed = dispose_outstanding(state.findings, {"remove_delivery": "removed", "revert": "reverted", "replan": "carried", "abandon": "abandoned"}[action])
            edges.append((action, CState(state.phase, "non_delivery", state.reviews, disposed, "none", state.blind_visited)))
    return edges


@dataclass(frozen=True)
class BState:
    phase: str
    obligations: tuple
    reviews: int
    control: str
    findings: tuple


@dataclass(frozen=True)
class ReviewBatch:
    primary_index: int
    entries: tuple


def b_owner(index):
    return "o" + str(index + 1)


def b_owner_index(owner):
    return int(owner[1:]) - 1


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


def b_batch_tokens(owner_indices, severities, disposition):
    owners = tuple(b_owner(index) for index in owner_indices) + ("unowned",)
    return tuple((owner, severity, disposition) for owner in owners for severity in severities)


def b_valid_batches(state, index, owner_indices=None):
    remaining = FINDING_CAP - len(state.findings)
    owner_indices = range(len(state.obligations)) if owner_indices is None else owner_indices
    tokens = b_batch_tokens(tuple(owner_indices), SEVERITIES, "open")
    batches = []
    for size in range(1, remaining + 1):
        for selected in combinations_with_replacement(tokens, size):
            batches.append(ReviewBatch(index, tuple(selected)))
    return tuple(batches)


def b_mixed_batches(state, index, owner_indices=None):
    if FINDING_CAP - len(state.findings) < 2:
        return ()
    owner_indices = range(len(state.obligations)) if owner_indices is None else owner_indices
    valid_tokens = b_batch_tokens(tuple(owner_indices), SEVERITIES, "open")
    dismissed_tokens = b_batch_tokens(tuple(owner_indices), BACKSTOP, "awaiting_recheck")
    batches = {tuple(sorted((valid, dismissed))) for valid in valid_tokens for dismissed in dismissed_tokens}
    return tuple(ReviewBatch(index, entries) for entries in sorted(batches))


def b_batch_name(batch):
    return "_".join(owner + "-" + severity + "-" + ("valid" if disposition == "open" else "dismissed") for owner, severity, disposition in batch.entries)


def b_reduce_review_batch(state, batch, generation, reviews, settle_primary=True):
    obligations = list(state.obligations)
    findings = state.findings
    by_owner = {}
    for owner, severity, disposition in batch.entries:
        by_owner.setdefault(owner, {"open": [], "awaiting_recheck": []})[disposition].append(severity)
    primary_owner = b_owner(batch.primary_index) if batch.primary_index >= 0 else ""
    if settle_primary and primary_owner not in by_owner:
        expected = "untested" if generation == 0 else "closed0"
        assert obligations[batch.primary_index] == expected
        obligations[batch.primary_index] = "closed" + str(generation)
    terminal_owner = False
    for owner, dispositions in sorted(by_owner.items()):
        valid_profile = tuple(dispositions["open"])
        dismissed_profile = tuple(dispositions["awaiting_recheck"])
        if owner == "unowned":
            if valid_profile:
                findings = mint_profile(findings, valid_profile, owner, "origin_indeterminate")
                terminal_owner = True
            if dismissed_profile:
                findings = mint_profile(findings, dismissed_profile, owner, "origin_indeterminate", "awaiting_recheck")
            continue
        owner_index = b_owner_index(owner)
        stage = obligations[owner_index]
        if stage == "untested":
            generation_for_owner = 0
            origin = "pre_existing"
        elif stage == "closed0":
            generation_for_owner = 1
            origin = "reopened"
        elif stage == "closed1":
            generation_for_owner = 1
            origin = "reopened"
            terminal_owner = True
        else:
            raise AssertionError("finding batch targeted an obligation with unresolved work")
        if valid_profile:
            if stage == "closed1":
                obligations[owner_index] = "open_exhausted"
            else:
                obligations[owner_index] = "open" + str(generation_for_owner)
            findings = mint_profile(findings, valid_profile, owner, origin)
        elif dismissed_profile:
            is_scheduled_primary = settle_primary and owner_index == batch.primary_index
            if stage == "closed1":
                obligations[owner_index] = "recheck_exhausted"
            elif is_scheduled_primary:
                obligations[owner_index] = "recheck_initial" if generation_for_owner == 0 else "recheck_reopen"
            else:
                obligations[owner_index] = "recheck_incidental_initial" if generation_for_owner == 0 else "recheck_incidental_reopen"
        if dismissed_profile:
            findings = mint_profile(findings, dismissed_profile, owner, origin, "awaiting_recheck")
    initials_incomplete = any(stage in ("untested", "recheck_incidental_initial") for stage in obligations)
    if initials_incomplete:
        obligations = ["deferred1" if stage == "open1" else "deferred_recheck1" if stage == "recheck_reopen" else stage for stage in obligations]
    candidate = BState(state.phase, tuple(obligations), reviews, "active", findings)
    if terminal_owner or reviews >= 4 * len(state.obligations) + 1:
        return b_terminal(candidate)
    return candidate


def b_dismissed_from_attempt(state, index, stage, reviews, profile, origin, parent_id=0):
    owner = b_owner(index)
    findings = mint_profile(state.findings, profile, owner, origin, "awaiting_recheck", parent_id)
    obligations = replace(state.obligations, index, stage)
    return BState(state.phase, obligations, reviews, "active", findings)


def b_scope_from_attempt(state, index, generation, reviews, severity):
    owner = b_owner(index)
    origin = "pre_existing" if generation == 0 else "reopened"
    if severity == "low":
        findings = mint_scope_expansion(state.findings, severity, owner, origin, "backlogged")
        obligations = replace(state.obligations, index, "closed" + str(generation))
        return BState(state.phase, obligations, reviews, "active", findings)
    if severity == "medium":
        findings = mint_scope_expansion(state.findings, severity, owner, origin, "scope_terminal")
        return BState(state.phase, state.obligations, reviews, "terminal_scope_decision", findings)
    findings = mint_scope_expansion(state.findings, severity, owner, origin, "awaiting_scope_recheck")
    stage = "scope_recheck_initial" if generation == 0 else "scope_recheck_reopen"
    return BState(state.phase, replace(state.obligations, index, stage), reviews, "active", findings)


def b_attempt_edges(state, index, generation):
    edges = []
    owner = b_owner(index)
    limit = 4 * len(state.obligations) + 1
    reviews = state.reviews + 1
    prefix = owner + "_"
    eligible = tuple(owner_index for owner_index, stage in enumerate(state.obligations) if stage in (("untested", "closed0") if generation == 0 else ("closed0", "closed1")))
    if generation == 0:
        edges.append((prefix + "initial_clean", BState(state.phase, replace(state.obligations, index, "closed0"), reviews, "active", state.findings)))
        for batch in b_valid_batches(state, index, eligible):
            edges.append((prefix + "initial_batch_" + b_batch_name(batch), b_reduce_review_batch(state, batch, generation, reviews)))
        for batch in b_mixed_batches(state, index, eligible):
            edges.append((prefix + "initial_mixed_batch_" + b_batch_name(batch), b_reduce_review_batch(state, batch, generation, reviews)))
        for profile in dismissal_profiles(state.findings):
            edges.append((prefix + "initial_dismissed_" + profile_name(profile), b_dismissed_from_attempt(state, index, "recheck_initial", reviews, profile, "pre_existing")))
    else:
        edges.append((prefix + "reopen_clean", BState(state.phase, replace(state.obligations, index, "closed1"), reviews, "active", state.findings)))
        settled_owner = tuple(f for f in state.findings if f.owner == owner and f.disposition in ("resolved", "dismissed"))
        if settled_owner:
            findings = update_findings(state.findings, lambda f: f.owner == owner and f.disposition in ("resolved", "dismissed"), "open")
            edges.append((prefix + "material_new_evidence_existing", BState(state.phase, replace(state.obligations, index, "open1"), reviews, "active", findings)))
        for batch in b_valid_batches(state, index, eligible):
            edges.append((prefix + "reopen_batch_" + b_batch_name(batch), b_reduce_review_batch(state, batch, generation, reviews)))
        for batch in b_mixed_batches(state, index, eligible):
            edges.append((prefix + "reopen_mixed_batch_" + b_batch_name(batch), b_reduce_review_batch(state, batch, generation, reviews)))
        for profile in dismissal_profiles(state.findings):
            edges.append((prefix + "material_new_evidence_dismissed_" + profile_name(profile), b_dismissed_from_attempt(state, index, "recheck_reopen", reviews, profile, "reopened")))
    if len(state.findings) < FINDING_CAP:
        for severity in SEVERITIES:
            edges.append((prefix + "scope_expanded_" + severity, b_scope_from_attempt(state, index, generation, reviews, severity)))
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


def b_scope_from_verification(state, index, generation, reviews, passed, severity):
    owner = b_owner(index)
    if severity == "low":
        findings = mint_scope_expansion(passed, severity, owner, "fix_induced", "backlogged")
        return BState(state.phase, replace(state.obligations, index, "closed" + str(generation)), reviews, "active", findings)
    if severity == "medium":
        findings = mint_scope_expansion(passed, severity, owner, "fix_induced", "scope_terminal")
        return BState(state.phase, state.obligations, reviews, "terminal_scope_decision", findings)
    findings = mint_scope_expansion(passed, severity, owner, "fix_induced", "awaiting_scope_recheck")
    obligations = replace(state.obligations, index, "scope_recheck_verify" + str(generation))
    return BState(state.phase, obligations, reviews, "active", findings)


def b_verify_edges(state, index, generation):
    edges = []
    owner = b_owner(index)
    reviews = state.reviews + 1
    next_closed = "closed" + str(generation)
    prefix = owner + "_verify" + str(generation) + "_"
    passed = b_owner_update(state.findings, owner, "pending_verification", "resolved")
    passed_state = BState(state.phase, replace(state.obligations, index, next_closed), reviews, "active", passed)
    edges.append((prefix + "pass_joint", passed_state))
    other_owners = tuple(owner_index for owner_index, stage in enumerate(state.obligations) if owner_index != index and stage in ("untested", "closed0", "closed1"))
    for batch in b_valid_batches(state, index, other_owners):
        observed = b_reduce_review_batch(passed_state, batch, generation, reviews, False)
        edges.append((prefix + "pass_with_batch_" + b_batch_name(batch), observed))
    for batch in b_mixed_batches(state, index, other_owners):
        observed = b_reduce_review_batch(passed_state, batch, generation, reviews, False)
        edges.append((prefix + "pass_with_mixed_batch_" + b_batch_name(batch), observed))
    failed = b_owner_update(state.findings, owner, "pending_verification", "open")
    failed_state = BState(state.phase, replace(state.obligations, index, "open" + str(generation)), reviews, "active", failed)
    edges.append((prefix + "fail_joint", b_terminal(failed_state)))
    parents = tuple(f for f in state.findings if f.owner == owner and f.disposition == "pending_verification")
    if len(failed) < FINDING_CAP:
        parent_id = parents[0].finding_id if parents else 0
        for dismissed_severity in BACKSTOP:
            mixed = mint_profile(failed, (dismissed_severity,), owner, "fix_induced", "awaiting_recheck", parent_id)
            candidate = BState(state.phase, replace(state.obligations, index, "open" + str(generation)), reviews, "active", mixed)
            edges.append((prefix + "fail_with_dismissed_" + dismissed_severity, b_terminal(candidate)))
    if parents and len(state.findings) < FINDING_CAP:
        for severity in SEVERITIES:
            with_child = mint_profile(failed, (severity,), owner, "fix_induced", "open", parents[0].finding_id)
            candidate = BState(state.phase, replace(state.obligations, index, "open" + str(generation)), reviews, "active", with_child)
            edges.append((prefix + "fail_with_child_" + severity, b_terminal(candidate)))
    parent_id = parents[0].finding_id if parents else 0
    for profile in dismissal_profiles(passed):
        stage = "recheck_verify" + str(generation)
        base = BState(state.phase, replace(state.obligations, index, next_closed), state.reviews, "active", passed)
        edges.append((prefix + "dismissed_" + profile_name(profile), b_dismissed_from_attempt(base, index, stage, reviews, profile, "fix_induced", parent_id)))
    if len(state.findings) < FINDING_CAP:
        for severity in SEVERITIES:
            edges.append(b_unowned_edge(state, reviews, severity, prefix))
        for severity in SEVERITIES:
            edges.append((prefix + "scope_expanded_" + severity, b_scope_from_verification(state, index, generation, reviews, passed, severity)))
    return edges


def b_dismissal_recheck_edges(state):
    upheld = update_findings(state.findings, is_pending_recheck, "dismissed")
    overturned = update_findings(state.findings, is_pending_recheck, "open")
    upheld_obligations = list(state.obligations)
    overturned_obligations = list(state.obligations)
    overturned_terminal = any(f.owner == "unowned" and is_pending_recheck(f) for f in state.findings)
    for index, stage in enumerate(state.obligations):
        if stage == "recheck_initial":
            upheld_obligations[index] = "closed0"
            overturned_obligations[index] = "open0"
        elif stage == "recheck_reopen":
            upheld_obligations[index] = "closed1"
            overturned_obligations[index] = "open1"
        elif stage == "deferred_recheck1":
            upheld_obligations[index] = "closed0"
            overturned_obligations[index] = "deferred1"
        elif stage == "recheck_incidental_initial":
            upheld_obligations[index] = "untested"
            overturned_obligations[index] = "open0"
        elif stage == "recheck_incidental_reopen":
            upheld_obligations[index] = "closed0"
            overturned_obligations[index] = "deferred1" if "untested" in state.obligations else "open1"
        elif stage.startswith("recheck_verify"):
            generation = stage[-1]
            upheld_obligations[index] = "closed" + generation
            overturned_obligations[index] = "open" + generation
            overturned_terminal = True
        elif stage == "recheck_exhausted":
            upheld_obligations[index] = "closed1"
            overturned_obligations[index] = "open_exhausted"
            overturned_terminal = True
    upheld_candidate = BState(state.phase, tuple(upheld_obligations), state.reviews, "active", upheld)
    overturned_candidate = BState(state.phase, tuple(overturned_obligations), state.reviews, "active", overturned)
    if state.control == "recheck_blind":
        upheld_target = BState(state.phase, tuple(upheld_obligations), state.reviews, "complete", upheld)
        overturned_target = b_terminal(overturned_candidate)
    else:
        upheld_target = b_terminal(upheld_candidate) if state.control in ("terminal", "serious_blocked") else upheld_candidate
        overturned_target = b_terminal(overturned_candidate) if overturned_terminal or state.control in ("terminal", "serious_blocked") else overturned_candidate
    return [("dismissal_recheck_upheld", upheld_target), ("dismissal_recheck_overturned", overturned_target)]


def b_scope_recheck_edges(state):
    referral = next(f for f in state.findings if is_pending_scope_recheck(f))
    owner_index = b_owner_index(referral.owner) if referral.owner.startswith("o") else -1
    stage = state.obligations[owner_index] if owner_index >= 0 else "scope_recheck_blind"
    if referral.severity == "high":
        upheld = update_findings(state.findings, is_pending_scope_recheck, "scope_terminal")
        upheld_target = BState(state.phase, state.obligations, state.reviews, "terminal_scope_decision", upheld)
        overturned = update_findings(state.findings, is_pending_scope_recheck, "open")
        overturned = update_scope(overturned, lambda f: f.finding_id == referral.finding_id, IN_SCOPE)
        obligations = list(state.obligations)
        terminal = False
        if stage == "scope_recheck_initial":
            obligations[owner_index] = "open0"
        elif stage == "scope_recheck_reopen":
            obligations[owner_index] = "open1"
        elif stage.startswith("scope_recheck_verify"):
            obligations[owner_index] = "open" + stage[-1]
            terminal = True
        else:
            terminal = True
        candidate = BState(state.phase, tuple(obligations), state.reviews, "active", overturned)
        overturned_target = b_terminal(candidate) if terminal else candidate
    else:
        upheld = update_findings(state.findings, is_pending_scope_recheck, "open")
        overturned = update_findings(state.findings, is_pending_scope_recheck, "open")
        overturned = update_scope(overturned, lambda f: f.finding_id == referral.finding_id, IN_SCOPE)
        obligations = list(state.obligations)
        if owner_index >= 0:
            generation = "1" if "reopen" in stage or stage.endswith("1") else "0"
            obligations[owner_index] = "open" + generation
        upheld_target = BState(state.phase, tuple(obligations), state.reviews, "serious_blocked", upheld)
        overturned_target = BState(state.phase, tuple(obligations), state.reviews, "serious_blocked", overturned)
    return [("scope_recheck_upheld", upheld_target), ("scope_recheck_overturned", overturned_target)]


def b_blind_edges(state):
    edges = []
    reviews = state.reviews + 1
    edges.append(("blind_closure_clean", BState(state.phase, state.obligations, reviews, "complete", state.findings)))
    for batch in b_valid_batches(state, -1):
        observed = b_reduce_review_batch(BState(state.phase, state.obligations, reviews, "active", state.findings), batch, 0, reviews, False)
        edges.append(("blind_closure_batch_" + b_batch_name(batch), b_terminal(observed)))
    for batch in b_mixed_batches(state, -1):
        observed = b_reduce_review_batch(BState(state.phase, state.obligations, reviews, "active", state.findings), batch, 0, reviews, False)
        edges.append(("blind_closure_mixed_batch_" + b_batch_name(batch), b_terminal(observed)))
    for profile in dismissal_profiles(state.findings):
        findings = mint_profile(state.findings, profile, "blind", "pre_existing", "awaiting_recheck")
        edges.append(("blind_closure_dismissed_" + profile_name(profile), BState(state.phase, state.obligations, reviews, "recheck_blind", findings)))
    if len(state.findings) < FINDING_CAP:
        for severity in SEVERITIES:
            if severity == "low":
                findings = mint_scope_expansion(state.findings, severity, "blind", "pre_existing", "backlogged")
                target = BState(state.phase, state.obligations, reviews, "complete", findings)
            elif severity == "medium":
                findings = mint_scope_expansion(state.findings, severity, "blind", "pre_existing", "scope_terminal")
                target = BState(state.phase, state.obligations, reviews, "terminal_scope_decision", findings)
            else:
                findings = mint_scope_expansion(state.findings, severity, "blind", "pre_existing", "awaiting_scope_recheck")
                target = BState(state.phase, state.obligations, reviews, "scope_recheck_blind", findings)
            edges.append(("blind_scope_expanded_" + severity, target))
    return edges


def b_has_generation_one_work_before_initial(state):
    if state.control != "active" or "untested" not in state.obligations:
        return False
    return any(stage in ("open1", "pending1", "closed1", "recheck_reopen", "recheck_verify1", "scope_recheck_reopen", "scope_recheck_verify1") for stage in state.obligations)


def b_edges(state):
    if has_pending_scope_recheck(state.findings):
        return b_scope_recheck_edges(state)
    if has_pending_recheck(state.findings):
        return b_dismissal_recheck_edges(state)
    edges = []
    if state.control == "active":
        limit = 4 * len(state.obligations) + 1
        special = [index for index, value in enumerate(state.obligations) if value.startswith(("open", "pending")) and value != "open_exhausted"]
        if special:
            index = special[0]
            stage = state.obligations[index]
            if stage.startswith("open"):
                edges.extend(b_repair_edges(state, index, int(stage[-1])))
            else:
                if state.reviews < limit:
                    edges.extend(b_verify_edges(state, index, int(stage[-1])))
                else:
                    edges.append((b_owner(index) + "_authority_exhausted", b_terminal(state)))
        else:
            untested = [index for index, value in enumerate(state.obligations) if value == "untested"]
            deferred = [index for index, value in enumerate(state.obligations) if value == "deferred1"]
            if untested and state.reviews < limit:
                edges.extend(b_attempt_edges(state, untested[0], 0))
            elif untested:
                edges.append(("authority_exhausted_with_untested", b_terminal(state)))
            elif deferred:
                index = deferred[0]
                edges.append((b_owner(index) + "_activate_deferred_reopen", BState(state.phase, replace(state.obligations, index, "open1"), state.reviews, "active", state.findings)))
            elif state.reviews < limit and b_all_closed(state.obligations):
                closed0 = [index for index, value in enumerate(state.obligations) if value == "closed0"]
                if closed0:
                    edges.extend(b_attempt_edges(state, closed0[0], 1))
                edges.extend(b_blind_edges(state))
            else:
                edges.append(("authority_exhausted", b_terminal(state)))
        carried = b_dispose(state.findings, "scope_digest_changed")
        edges.append(("scope_digest_changed", BState(state.phase, state.obligations, state.reviews, "replanned", carried)))
    elif state.control in ("terminal", "serious_blocked"):
        no_untested = all(value != "untested" for value in state.obligations)
        if state.control == "terminal" and no_untested and not outstanding_at_floor(state.findings) and not has_pending_recheck(state.findings) and not has_pending_scope_recheck(state.findings):
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


def scope_digest(obligations, exclusions):
    canonical = "obligations=" + "\x1f".join(sorted(obligations)) + "\x1eexclusions=" + "\x1f".join(sorted(exclusions))
    return sha256(canonical.encode("ascii")).hexdigest()


@dataclass(frozen=True)
class Predecessor:
    family_id: str
    ancestor_ids: tuple
    obligations: tuple
    exclusions: tuple
    scope_digest: str
    terminal: bool
    review_spend: int
    carried_findings: tuple


@dataclass(frozen=True)
class Successor:
    family_id: str
    predecessor_id: str
    ancestor_ids: tuple
    obligations: tuple
    exclusions: tuple
    scope_digest: str
    predecessor_spend: int
    carried_findings: tuple
    authority_origin: str


@dataclass(frozen=True)
class SuccessorReceipt:
    predecessor_id: str
    successor_id: str
    predecessor_ancestor_ids: tuple
    successor_ancestor_ids: tuple
    predecessor_scope_digest: str
    successor_scope_digest: str
    presented_options: tuple
    chosen_successor: str
    predecessor_spend: int
    carried_findings: tuple
    materially_different: bool


def successor_authorised(predecessor, successor, receipt):
    if receipt is None:
        return False
    structured_delta = predecessor.scope_digest != successor.scope_digest
    exact_successor_digest = successor.scope_digest == scope_digest(successor.obligations, successor.exclusions)
    exact_predecessor_digest = predecessor.scope_digest == scope_digest(predecessor.obligations, predecessor.exclusions)
    predecessor_registry = predecessor.ancestor_ids + (predecessor.family_id,)
    predecessor_ancestry_valid = len(set(predecessor_registry)) == len(predecessor_registry)
    fresh_successor_id = successor.family_id not in predecessor_registry
    exact_successor_ancestry = successor.ancestor_ids == predecessor_registry
    return all((
        predecessor.terminal,
        structured_delta,
        exact_predecessor_digest,
        exact_successor_digest,
        predecessor_ancestry_valid,
        fresh_successor_id,
        exact_successor_ancestry,
        successor.predecessor_id == predecessor.family_id,
        successor.predecessor_spend == predecessor.review_spend,
        successor.carried_findings == predecessor.carried_findings,
        successor.authority_origin == "new_human_receipt",
        receipt.predecessor_id == predecessor.family_id,
        receipt.successor_id == successor.family_id,
        receipt.predecessor_ancestor_ids == predecessor.ancestor_ids,
        receipt.successor_ancestor_ids == successor.ancestor_ids,
        receipt.predecessor_scope_digest == predecessor.scope_digest,
        receipt.successor_scope_digest == successor.scope_digest,
        bool(receipt.presented_options),
        receipt.chosen_successor in receipt.presented_options,
        receipt.chosen_successor == successor.family_id,
        receipt.predecessor_spend == predecessor.review_spend,
        receipt.carried_findings == predecessor.carried_findings,
        receipt.materially_different,
    ))


def findings_of(state):
    return getattr(state, "findings", ())


def critical_map(state):
    return {f.finding_id: f for f in findings_of(state) if f.severity == "critical" and is_outstanding(f)}


def legal_critical_clear(source_finding, target_finding, action):
    if target_finding is None:
        return False
    if source_finding.disposition == "pending_verification" and target_finding.disposition == "resolved" and "verify" in action and ("pass" in action or "dismissed" in action or "scope_expanded" in action):
        return True
    if source_finding.disposition == "awaiting_recheck" and target_finding.disposition == "dismissed" and "recheck_upheld" in action:
        return True
    if target_finding.disposition in ("removed", "reverted", "carried", "abandoned") and (action in NON_DELIVERY or action == "scope_digest_changed"):
        return True
    return False


def b_owner_state_matches(state):
    if state.control not in ("active", "terminal", "serious_blocked", "recheck_blind", "scope_recheck_blind"):
        return True
    for finding in state.findings:
        if not is_outstanding(finding) or not finding.owner.startswith("o"):
            continue
        stage = state.obligations[b_owner_index(finding.owner)]
        if finding.disposition == "open" and not (stage.startswith("open") or stage == "deferred1"):
            return False
        if finding.disposition == "pending_verification" and not stage.startswith("pending"):
            return False
        if finding.disposition == "awaiting_recheck":
            same_owner_open = any(other.owner == finding.owner and other.disposition == "open" for other in state.findings)
            if not (stage.startswith("recheck") or stage == "deferred_recheck1" or same_owner_open and (stage.startswith("open") or stage == "deferred1")):
                return False
        if finding.disposition == "awaiting_scope_recheck" and not stage.startswith("scope_recheck"):
            return False
    if state.control in ("active", "terminal", "serious_blocked"):
        for index, stage in enumerate(state.obligations):
            owner_findings = tuple(f for f in state.findings if f.owner == b_owner(index) and is_outstanding(f))
            if (stage.startswith("open") or stage == "deferred1") and not any(f.disposition == "open" for f in owner_findings):
                return False
            if stage.startswith("pending") and not any(f.disposition == "pending_verification" for f in owner_findings):
                return False
            if (stage.startswith("recheck") or stage == "deferred_recheck1") and not any(f.disposition == "awaiting_recheck" for f in owner_findings):
                return False
            if stage.startswith("scope_recheck") and not any(f.disposition == "awaiting_scope_recheck" for f in owner_findings):
                return False
    return True


def b_atomic_cross_owner_low_critical(source, action, target):
    if "batch_" not in action:
        return False
    source_ids = {finding.finding_id for finding in source.findings}
    added = tuple(finding for finding in target.findings if finding.finding_id not in source_ids and finding.owner.startswith("o"))
    return {finding.severity for finding in added} >= {"low", "critical"} and len({finding.owner for finding in added}) >= 2


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
                if critical_map(target) or has_pending_recheck(findings_of(target)) or has_pending_scope_recheck(findings_of(target)):
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


def mixed_disposition_metrics(result, is_exhausted):
    mixed_states = tuple(state for state in result["seen"] if any(f.disposition == "open" for f in findings_of(state)) and any(f.disposition == "awaiting_recheck" for f in findings_of(state)))
    upheld = 0
    overturned = 0
    bad_preservation = 0
    for source, action, target in result["edges_data"]:
        if source not in mixed_states:
            continue
        open_ids = {f.finding_id: f.evidence_id for f in findings_of(source) if f.disposition == "open"}
        recheck_ids = {f.finding_id: f.evidence_id for f in findings_of(source) if f.disposition == "awaiting_recheck"}
        target_by_id = {f.finding_id: f for f in findings_of(target)}
        if recheck_ids and all(target_by_id.get(finding_id) and target_by_id[finding_id].disposition == "dismissed" and target_by_id[finding_id].evidence_id == evidence_id for finding_id, evidence_id in recheck_ids.items()):
            upheld += 1
            if not all(target_by_id.get(finding_id) and target_by_id[finding_id].disposition == "open" and target_by_id[finding_id].evidence_id == evidence_id for finding_id, evidence_id in open_ids.items()):
                bad_preservation += 1
        if recheck_ids and all(target_by_id.get(finding_id) and target_by_id[finding_id].disposition == "open" and target_by_id[finding_id].evidence_id == evidence_id for finding_id, evidence_id in recheck_ids.items()):
            overturned += 1
            if not all(target_by_id.get(finding_id) and target_by_id[finding_id].disposition == "open" and target_by_id[finding_id].evidence_id == evidence_id for finding_id, evidence_id in open_ids.items()):
                bad_preservation += 1
    exhausted = sum(1 for state in mixed_states if is_exhausted(state))
    return len(mixed_states), upheld, overturned, exhausted, bad_preservation


def mixed_exhaustion_control(starts, edge_function):
    cases = 0
    bad = 0
    for start in starts:
        for action, mixed in edge_function(start):
            open_ids = {f.finding_id: f.evidence_id for f in findings_of(mixed) if f.disposition == "open"}
            recheck_ids = {f.finding_id: f.evidence_id for f in findings_of(mixed) if f.disposition == "awaiting_recheck"}
            if not open_ids or not recheck_ids:
                continue
            cases += 1
            continuations = edge_function(mixed)
            upheld = tuple(target for next_action, target in continuations if all(any(f.finding_id == finding_id and f.disposition == "dismissed" and f.evidence_id == evidence_id for f in findings_of(target)) for finding_id, evidence_id in recheck_ids.items()))
            overturned = tuple(target for next_action, target in continuations if all(any(f.finding_id == finding_id and f.disposition == "open" and f.evidence_id == evidence_id for f in findings_of(target)) for finding_id, evidence_id in recheck_ids.items()))
            if not upheld or not overturned:
                bad += 1
                continue
            for target in upheld + overturned:
                target_by_id = {f.finding_id: f for f in findings_of(target)}
                if target.reviews != mixed.reviews or not all(target_by_id.get(finding_id) and target_by_id[finding_id].disposition == "open" and target_by_id[finding_id].evidence_id == evidence_id for finding_id, evidence_id in open_ids.items()):
                    bad += 1
    return cases, bad


def scope_control_metrics(result):
    states = result["seen"]
    routes = (
        any(f.scope_relation.kind == "scope_expanded" and f.severity == "low" and f.disposition == "backlogged" for state in states for f in findings_of(state)),
        any(state.control == "terminal_scope_decision" and any(f.scope_relation.kind == "scope_expanded" and f.severity == "medium" for f in findings_of(state)) for state in states),
        any(f.scope_relation.kind == "scope_expanded" and f.severity == "high" and f.disposition == "awaiting_scope_recheck" for state in states for f in findings_of(state)),
        any(state.control == "terminal_scope_decision" and any(f.scope_relation.kind == "scope_expanded" and f.severity == "high" and f.disposition == "scope_terminal" for f in findings_of(state)) for state in states),
        any(f.scope_relation.kind == "in_scope" and f.severity == "high" and f.disposition == "open" for state in states for f in findings_of(state)),
        any(f.scope_relation.kind == "scope_expanded" and f.severity == "critical" and f.disposition == "awaiting_scope_recheck" for state in states for f in findings_of(state)),
        any(state.control == "serious_blocked" and any(f.scope_relation.kind == "scope_expanded" and f.severity == "critical" for f in findings_of(state)) for state in states),
        any(state.control == "serious_blocked" and any(f.scope_relation.kind == "in_scope" and f.severity == "critical" for f in findings_of(state)) for state in states),
    )
    bad_spend = 0
    bad_identity = 0
    for source, action, target in result["edges_data"]:
        pending = {f.finding_id: f.evidence_id for f in findings_of(source) if f.disposition == "awaiting_scope_recheck"}
        if not pending:
            continue
        if source.reviews != target.reviews:
            bad_spend += 1
        target_evidence = {f.finding_id: f.evidence_id for f in findings_of(target)}
        if any(target_evidence.get(finding_id) != evidence_id for finding_id, evidence_id in pending.items()):
            bad_identity += 1
    bad_delivery = sum(1 for state in states if state.control in ("complete", "delivered_residual") and any(f.disposition == "awaiting_scope_recheck" or f.scope_relation.kind == "scope_expanded" and f.severity in ("medium", "high", "critical") and is_outstanding(f) for f in findings_of(state)))
    return sum(routes), bad_spend, bad_identity, bad_delivery


def a_upheld_streak_trace(need):
    if need != 2:
        return 0
    state = AState("active", 0, 0, False, ())
    actions = (
        "review_settled",
        "review_findings_low",
        "repair_joint",
        "verify_fail_joint",
        "repair_joint",
        "verify_pass_joint",
        "review_dismissed_high",
        "dismissal_recheck_upheld",
    )
    for wanted in actions:
        state = next(target for action, target in a_edges(state, need, 5, 2) if action == wanted)
    return int(state.control == "complete" and state.reviews == 5 and state.streak == 2)


def check_a(phase, risk):
    need = 1 if phase == "acceptance" or risk == "low_risk" else 2
    start = AState("active", 0, 0, False, ())
    result = walk(start, lambda state: a_edges(state, need, 5, 2), ("complete", "delivered_residual"), 7)
    assert_common(result)
    bad_upheld_unlock = sum(1 for source, action, target in result["edges_data"] if action == "dismissal_recheck_upheld" and not source.serious_seen and target.serious_seen)
    bad_foreclosure_state = sum(1 for state in result["seen"] if state.control in ("active", "repair", "verify") and not has_pending_recheck(state.findings) and not has_pending_scope_recheck(state.findings) and a_cannot_complete(state, need, 5, 2))
    dismissal_only_upheld = tuple((source, target) for source, action, target in result["edges_data"] if action == "dismissal_recheck_upheld" and not any(f.disposition == "open" for f in source.findings))
    bad_upheld_streak = sum(1 for source, target in dismissal_only_upheld if target.streak != source.streak + 1)
    upheld_prior_streak_complete = sum(1 for source, target in dismissal_only_upheld if source.streak == 1 and target.control == "complete" and target.streak == 2)
    upheld_batch5_complete = a_upheld_streak_trace(need)
    mixed_disposition, mixed_upheld, mixed_overturned, mixed_exhausted, bad_mixed_preservation = mixed_disposition_metrics(result, lambda state: state.reviews == a_limit(state, 5, 2))
    scope_routes, bad_scope_spend, bad_scope_identity, bad_scope_delivery = scope_control_metrics(result)
    assert bad_upheld_unlock == 0
    assert bad_foreclosure_state == 0
    assert bad_upheld_streak == 0
    if need == 2:
        assert upheld_prior_streak_complete > 0
        assert upheld_batch5_complete == 1
    exhaustion_starts = (AState("active", 4, need - 1, False, ()), AState("active", 6, need - 1, True, ()))
    mixed_exhaustion_cases, bad_mixed_exhaustion = mixed_exhaustion_control(exhaustion_starts, lambda state: a_edges(state, need, 5, 2))
    assert mixed_disposition > 0
    assert mixed_upheld > 0
    assert mixed_overturned > 0
    assert mixed_exhaustion_cases > 0
    assert bad_mixed_exhaustion == 0
    assert bad_mixed_preservation == 0
    assert scope_routes == 8
    assert bad_scope_spend == 0
    assert bad_scope_identity == 0
    assert bad_scope_delivery == 0
    print("A phase=%s risk=%s floor=%s finding_cap=%d normal=5 reserve=2 required=%d states=%d edges=%d terminal=%d acyclic=%s min_reviews=%d max_reviews=%d mixed_low_critical=%d parent_child=%d mixed_disposition=%d mixed_upheld=%d mixed_overturned=%d mixed_exhausted=%d mixed_exhaustion_cases=%d scope_routes=%d bad_delivery=%d bad_unverified_delivery=%d bad_critical_clear=%d bad_bound=%d bad_upheld_unlock=%d bad_upheld_streak=%d upheld_prior_streak_complete=%d upheld_batch5_complete=%d bad_mixed_preservation=%d bad_mixed_exhaustion=%d bad_scope_spend=%d bad_scope_identity=%d bad_scope_delivery=%d bad_foreclosure_state=%d" % (
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
        mixed_disposition,
        mixed_upheld,
        mixed_overturned,
        mixed_exhausted,
        mixed_exhaustion_cases,
        scope_routes,
        result["bad_delivery"],
        result["bad_unverified_delivery"],
        result["bad_clear"],
        result["bad_bound"],
        bad_upheld_unlock,
        bad_upheld_streak,
        upheld_prior_streak_complete,
        upheld_batch5_complete,
        bad_mixed_preservation,
        bad_mixed_exhaustion,
        bad_scope_spend,
        bad_scope_identity,
        bad_scope_delivery,
        bad_foreclosure_state,
    ))


def check_c(phase, risk):
    start = CState(phase, "discovery", 0, (), "none", False)
    result = walk(start, lambda state: c_edges(state, risk), ("complete", "delivered_residual"), 4)
    assert_common(result)
    bad_acceptance_blind_bypass = sum(1 for state in result["seen"] if phase == "acceptance" and state.control == "complete" and not state.blind_visited)
    mixed_disposition, mixed_upheld, mixed_overturned, mixed_exhausted, bad_mixed_preservation = mixed_disposition_metrics(result, lambda state: state.control in ("verify2", "blind_closure"))
    scope_routes, bad_scope_spend, bad_scope_identity, bad_scope_delivery = scope_control_metrics(result)
    exhaustion_starts = (CState(phase, "blind_closure", 3, (), "none", False),)
    mixed_exhaustion_cases, bad_mixed_exhaustion = mixed_exhaustion_control(exhaustion_starts, lambda state: c_edges(state, risk))
    assert bad_acceptance_blind_bypass == 0
    assert mixed_disposition > 0
    assert mixed_upheld > 0
    assert mixed_overturned > 0
    assert mixed_exhaustion_cases > 0
    assert bad_mixed_exhaustion == 0
    assert bad_mixed_preservation == 0
    assert scope_routes == 8
    assert bad_scope_spend == 0
    assert bad_scope_identity == 0
    assert bad_scope_delivery == 0
    print("C phase=%s risk=%s floor=%s finding_cap=%d stages=4 repairs=2 states=%d edges=%d terminal=%d acyclic=%s min_reviews=%d max_reviews=%d mixed_low_critical=%d parent_child=%d mixed_disposition=%d mixed_upheld=%d mixed_overturned=%d mixed_exhausted=%d mixed_exhaustion_cases=%d scope_routes=%d bad_delivery=%d bad_unverified_delivery=%d bad_critical_clear=%d bad_bound=%d bad_mixed_preservation=%d bad_mixed_exhaustion=%d bad_scope_spend=%d bad_scope_identity=%d bad_scope_delivery=%d bad_acceptance_blind_bypass=%d" % (
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
        mixed_disposition,
        mixed_upheld,
        mixed_overturned,
        mixed_exhausted,
        mixed_exhaustion_cases,
        scope_routes,
        result["bad_delivery"],
        result["bad_unverified_delivery"],
        result["bad_clear"],
        result["bad_bound"],
        bad_mixed_preservation,
        bad_mixed_exhaustion,
        bad_scope_spend,
        bad_scope_identity,
        bad_scope_delivery,
        bad_acceptance_blind_bypass,
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
    carried = (
        Finding(1, "o1", "low", "carried", "pre_existing", 0),
        Finding(2, "o2", "critical", "carried", "fix_induced", 1),
    )
    predecessor_obligations = ("O1", "O2")
    predecessor = Predecessor("F2", ("F0", "F1"), predecessor_obligations, (), scope_digest(predecessor_obligations, ()), True, 7, carried)
    predecessor_snapshot = Predecessor("F2", ("F0", "F1"), predecessor_obligations, (), scope_digest(predecessor_obligations, ()), True, 7, carried)
    successor_obligations = ("O1", "O2", "O3")
    successor = Successor("F3", "F2", ("F0", "F1", "F2"), successor_obligations, (), scope_digest(successor_obligations, ()), 7, carried, "new_human_receipt")
    receipt = SuccessorReceipt("F2", "F3", predecessor.ancestor_ids, successor.ancestor_ids, predecessor.scope_digest, successor.scope_digest, ("F3", "abandon"), "F3", 7, carried, True)
    accepted_different = successor_authorised(predecessor, successor, receipt)
    same_scope = dc_replace(successor, obligations=predecessor.obligations, scope_digest=predecessor.scope_digest)
    reordered_scope = dc_replace(successor, obligations=("O2", "O1"), scope_digest=predecessor.scope_digest)
    missing_options = dc_replace(receipt, presented_options=())
    wrong_family = dc_replace(receipt, predecessor_id="F9")
    wrong_predecessor_digest = dc_replace(receipt, predecessor_scope_digest="wrong")
    wrong_successor_digest = dc_replace(receipt, successor_scope_digest="wrong")
    missing_carry = dc_replace(receipt, carried_findings=carried[:1])
    fresh_authority = dc_replace(successor, predecessor_spend=0, authority_origin="predecessor_unspent")
    same_family = dc_replace(successor, family_id="F2")
    same_family_receipt = dc_replace(receipt, successor_id="F2", presented_options=("F2", "abandon"), chosen_successor="F2")
    ancestor_reuse = dc_replace(successor, family_id="F1")
    ancestor_receipt = dc_replace(receipt, successor_id="F1", presented_options=("F1", "abandon"), chosen_successor="F1")
    wrong_ancestry = dc_replace(successor, ancestor_ids=("F0", "F2"))
    wrong_ancestry_receipt = dc_replace(receipt, successor_ancestor_ids=wrong_ancestry.ancestor_ids)
    wrong_receipt_ancestry = dc_replace(receipt, predecessor_ancestor_ids=("F9",))
    rejected = (
        successor_authorised(predecessor, same_scope, dc_replace(receipt, successor_scope_digest=same_scope.scope_digest)),
        successor_authorised(predecessor, reordered_scope, dc_replace(receipt, successor_scope_digest=reordered_scope.scope_digest)),
        successor_authorised(predecessor, successor, None),
        successor_authorised(predecessor, successor, missing_options),
        successor_authorised(predecessor, successor, wrong_family),
        successor_authorised(predecessor, successor, wrong_predecessor_digest),
        successor_authorised(predecessor, successor, wrong_successor_digest),
        successor_authorised(predecessor, successor, missing_carry),
        successor_authorised(predecessor, fresh_authority, receipt),
        successor_authorised(predecessor, same_family, same_family_receipt),
        successor_authorised(predecessor, ancestor_reuse, ancestor_receipt),
        successor_authorised(predecessor, wrong_ancestry, wrong_ancestry_receipt),
        successor_authorised(predecessor, successor, wrong_receipt_ancestry),
    )
    predecessor_immutable = predecessor == predecessor_snapshot
    assert accepted_different
    assert not any(rejected)
    assert predecessor_immutable
    print("B successor structured_cases=14 accepted_different=%s bad_same_scope=%d bad_reordered_scope=%d bad_missing_receipt=%d bad_missing_options=%d bad_wrong_family=%d bad_wrong_predecessor_digest=%d bad_wrong_successor_digest=%d bad_missing_carry=%d bad_fresh_authority=%d bad_same_family=%d bad_ancestor_reuse=%d bad_ancestry_binding=%d bad_receipt_ancestry=%d bad_predecessor_mutation=%d" % (str(accepted_different).lower(), *(int(value) for value in rejected), int(not predecessor_immutable)))


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
    bad_reopen_before_initial = sum(1 for state in result["seen"] if b_has_generation_one_work_before_initial(state))
    deferred_early_findings = sum(1 for state in result["seen"] if "untested" in state.obligations and "deferred1" in state.obligations)
    bad_deferred_identity = sum(1 for state in result["seen"] for index, stage in enumerate(state.obligations) if state.control == "active" and stage == "deferred1" and not any(f.owner == b_owner(index) and f.disposition == "open" for f in state.findings))
    unowned_critical_states = sum(1 for state in result["seen"] if any(f.owner == "unowned" and f.severity == "critical" and is_outstanding(f) for f in state.findings))
    unowned_critical_delivery = sum(1 for state in result["seen"] if state.control in ("complete", "delivered_residual") and any(f.owner == "unowned" and f.severity == "critical" and is_outstanding(f) for f in state.findings))
    cross_owner_low_critical = sum(1 for state in result["seen"] if any(is_outstanding(low) and low.severity == "low" and low.owner.startswith("o") and any(is_outstanding(critical) and critical.severity == "critical" and critical.owner.startswith("o") and critical.owner != low.owner for critical in state.findings) for low in state.findings))
    atomic_cross_owner_low_critical = sum(1 for source, action, target in result["edges_data"] if b_atomic_cross_owner_low_critical(source, action, target))
    multi_initial_batch = sum(1 for source, action, target in result["edges_data"] if "initial_batch" in action and sum(1 for before, after in zip(source.obligations, target.obligations) if before == "untested" and after != "untested") > 1)
    bad_owner_state = sum(1 for state in result["seen"] if not b_owner_state_matches(state))
    mixed_disposition, mixed_upheld, mixed_overturned, mixed_exhausted, bad_mixed_preservation = mixed_disposition_metrics(result, lambda state: state.reviews == bound)
    mixed_same_owner = sum(1 for state in result["seen"] if any(valid.owner.startswith("o") and valid.disposition == "open" and any(dismissed.owner == valid.owner and dismissed.disposition == "awaiting_recheck" for dismissed in state.findings) for valid in state.findings))
    mixed_cross_owner = sum(1 for state in result["seen"] if any(valid.owner.startswith("o") and valid.disposition == "open" and any(dismissed.owner.startswith("o") and dismissed.owner != valid.owner and dismissed.disposition == "awaiting_recheck" for dismissed in state.findings) for valid in state.findings))
    mixed_owned_unowned = sum(1 for state in result["seen"] if any(f.owner.startswith("o") and f.disposition == "open" for f in state.findings) and any(f.owner == "unowned" and f.disposition == "awaiting_recheck" for f in state.findings) or any(f.owner == "unowned" and f.disposition == "open" for f in state.findings) and any(f.owner.startswith("o") and f.disposition == "awaiting_recheck" for f in state.findings))
    mixed_blind_closure = sum(1 for source, action, target in result["edges_data"] if action.startswith("blind_closure_mixed_batch_") and any(f.disposition == "open" for f in target.findings) and any(f.disposition == "awaiting_recheck" for f in target.findings))
    scope_routes, bad_scope_spend, bad_scope_identity, bad_scope_delivery = scope_control_metrics(result)
    assert bad_reopen_before_initial == 0
    assert bad_deferred_identity == 0
    exhaustion_start = BState(phase, tuple("closed0" for _ in range(obligations)), bound - 1, "active", ())
    mixed_exhaustion_cases, bad_mixed_exhaustion = mixed_exhaustion_control((exhaustion_start,), b_edges)
    assert bad_owner_state == 0
    assert mixed_disposition > 0
    assert mixed_upheld > 0
    assert mixed_overturned > 0
    assert mixed_blind_closure > 0
    if obligations > 0:
        assert mixed_same_owner > 0
        assert mixed_owned_unowned > 0
    if obligations > 1:
        assert mixed_cross_owner > 0
    assert mixed_exhaustion_cases > 0
    assert bad_mixed_exhaustion == 0
    assert bad_mixed_preservation == 0
    assert scope_routes == 8
    assert bad_scope_spend == 0
    assert bad_scope_identity == 0
    assert bad_scope_delivery == 0
    if obligations > 0:
        assert unowned_critical_states > 0
    if obligations > 1:
        assert cross_owner_low_critical > 0
        assert atomic_cross_owner_low_critical > 0
        assert multi_initial_batch > 0
    if obligations > 2:
        assert deferred_early_findings > 0
    assert unowned_critical_delivery == 0
    print("B phase=%s obligations=%d floor=%s finding_cap=%d bound=%d states=%d edges=%d terminal=%d acyclic=%s min_reviews=%d max_reviews=%d mixed_low_critical=%d parent_child=%d cross_owner_low_critical=%d atomic_cross_owner_low_critical=%d multi_initial_batch=%d mixed_disposition=%d mixed_same_owner=%d mixed_cross_owner=%d mixed_owned_unowned=%d mixed_blind_closure=%d mixed_upheld=%d mixed_overturned=%d mixed_exhausted=%d mixed_exhaustion_cases=%d deferred_early_findings=%d scope_routes=%d unowned_critical=%d bad_owner_state=%d bad_unowned_critical_delivery=%d bad_reopen_before_initial=%d bad_deferred_identity=%d bad_mixed_preservation=%d bad_mixed_exhaustion=%d bad_scope_spend=%d bad_scope_identity=%d bad_scope_delivery=%d bad_delivery=%d bad_unverified_delivery=%d bad_critical_clear=%d bad_bound=%d" % (
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
        cross_owner_low_critical,
        atomic_cross_owner_low_critical,
        multi_initial_batch,
        mixed_disposition,
        mixed_same_owner,
        mixed_cross_owner,
        mixed_owned_unowned,
        mixed_blind_closure,
        mixed_upheld,
        mixed_overturned,
        mixed_exhausted,
        mixed_exhaustion_cases,
        deferred_early_findings,
        scope_routes,
        unowned_critical_states,
        bad_owner_state,
        unowned_critical_delivery,
        bad_reopen_before_initial,
        bad_deferred_identity,
        bad_mixed_preservation,
        bad_mixed_exhaustion,
        bad_scope_spend,
        bad_scope_identity,
        bad_scope_delivery,
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
