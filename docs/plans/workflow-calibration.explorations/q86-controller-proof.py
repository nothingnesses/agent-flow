#!/usr/bin/env python3
from collections import deque
from dataclasses import dataclass, replace as dc_replace
from itertools import combinations_with_replacement
from hashlib import sha256
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


def a_edges(state, need, normal, reserve):
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
            edges.append(("review_dismissed_" + profile_name(profile), AState("recheck", reviews, 0, state.serious_seen, findings)))
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
        if parents and len(state.findings) < FINDING_CAP:
            for severity in SEVERITIES:
                with_child = mint_profile(failed, (severity,), "phase", "fix_induced", "open", parents[0].finding_id)
                serious_seen = state.serious_seen or severity in BACKSTOP
                edges.append(("verify_fail_with_child_" + severity, a_open(state, reviews, with_child, serious_seen, need, normal, reserve)))
        resolved = verification_pass_joint(state.findings)
        parent_id = parents[0].finding_id if parents else 0
        for profile in dismissal_profiles(resolved):
            findings = mint_profile(resolved, profile, "phase", "fix_induced", "awaiting_recheck", parent_id)
            edges.append(("verify_dismissed_" + profile_name(profile), AState("recheck", reviews, 0, state.serious_seen, findings)))
    elif state.control == "recheck":
        upheld = update_findings(state.findings, is_pending_recheck, "dismissed")
        edges.append(("recheck_upheld", a_settled(state, state.reviews, upheld, need, normal, reserve)))
        overturned = update_findings(state.findings, is_pending_recheck, "open")
        edges.append(("recheck_overturned", a_open(state, state.reviews, overturned, True, need, normal, reserve)))
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


def c_edges(state, risk):
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
            if parents and len(state.findings) < FINDING_CAP:
                for severity in SEVERITIES:
                    with_child = mint_profile(failed, (severity,), "phase", "fix_induced", "open", parents[0].finding_id)
                    edges.append(("verify_fail_with_child_" + severity, c_open(state, stage, reviews, with_child)))
            resolved = verification_pass_joint(state.findings)
            parent_id = parents[0].finding_id if parents else 0
            for profile in dismissal_profiles(resolved):
                findings = mint_profile(resolved, profile, "phase", "fix_induced", "awaiting_recheck", parent_id)
                edges.append(("verify_dismissed_" + profile_name(profile), CState(state.phase, "recheck", reviews, findings, stage, state.blind_visited)))
        else:
            edges.append(("review_settled", c_settled(state, stage, reviews, state.findings, risk)))
            for profile in severity_profiles(FINDING_CAP - len(state.findings)):
                findings = mint_profile(state.findings, profile, "phase", "pre_existing")
                edges.append(("review_findings_" + profile_name(profile), c_open(state, stage, reviews, findings)))
            for profile in dismissal_profiles(state.findings):
                findings = mint_profile(state.findings, profile, "phase", "pre_existing", "awaiting_recheck")
                edges.append(("review_dismissed_" + profile_name(profile), CState(state.phase, "recheck", reviews, findings, stage, state.blind_visited)))
    elif state.control in ("repair1", "repair2"):
        findings = repair_joint(state.findings)
        edges.append((state.control + "_joint", CState(state.phase, "verify" + state.control[-1], state.reviews, findings, "none", state.blind_visited)))
    elif state.control == "recheck":
        upheld = update_findings(state.findings, is_pending_recheck, "dismissed")
        edges.append(("recheck_upheld", c_settled(state, state.return_stage, state.reviews, upheld, risk)))
        overturned = update_findings(state.findings, is_pending_recheck, "open")
        edges.append(("recheck_overturned", c_open(state, state.return_stage, state.reviews, overturned)))
    elif state.control in ("terminal", "serious_blocked"):
        if state.control == "terminal" and not outstanding_at_floor(state.findings) and not has_pending_recheck(state.findings):
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
    owned: tuple
    unowned: tuple


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


def b_valid_batches(state, index, owner_indices=None):
    remaining = FINDING_CAP - len(state.findings)
    owner_indices = range(len(state.obligations)) if owner_indices is None else owner_indices
    tokens = tuple((b_owner(owner_index), severity) for owner_index in owner_indices for severity in SEVERITIES)
    tokens += tuple(("unowned", severity) for severity in SEVERITIES)
    batches = []
    for size in range(1, remaining + 1):
        for selected in combinations_with_replacement(tokens, size):
            by_owner = {}
            unowned = []
            for owner, severity in selected:
                if owner == "unowned":
                    unowned.append(severity)
                else:
                    by_owner.setdefault(owner, []).append(severity)
            owned = tuple((owner, tuple(severities)) for owner, severities in sorted(by_owner.items()))
            batches.append(ReviewBatch(index, owned, tuple(unowned)))
    return tuple(batches)


def b_batch_name(batch):
    owned = "_".join(owner + "-" + profile_name(profile) for owner, profile in batch.owned) or "none"
    unowned = profile_name(batch.unowned) if batch.unowned else "none"
    return "owned_" + owned + "_unowned_" + unowned


def b_reduce_valid_batch(state, batch, generation, reviews, settle_primary=True):
    obligations = list(state.obligations)
    findings = state.findings
    owned = dict(batch.owned)
    if settle_primary:
        primary_owner = b_owner(batch.primary_index)
        if primary_owner not in owned:
            expected = "untested" if generation == 0 else "closed0"
            assert obligations[batch.primary_index] == expected
            obligations[batch.primary_index] = "closed" + str(generation)
    terminal_owner = False
    for owner, profile in batch.owned:
        index = b_owner_index(owner)
        stage = obligations[index]
        if stage == "untested":
            obligations[index] = "open0"
            origin = "pre_existing"
        elif stage == "closed0":
            obligations[index] = "open1"
            origin = "reopened"
        elif stage == "closed1":
            obligations[index] = "open_exhausted"
            origin = "reopened"
            terminal_owner = True
        else:
            raise AssertionError("finding batch targeted an obligation with unresolved work")
        findings = mint_profile(findings, profile, owner, origin)
    if batch.unowned:
        findings = mint_profile(findings, batch.unowned, "unowned", "origin_indeterminate")
    candidate = BState(state.phase, tuple(obligations), reviews, "active", findings)
    if terminal_owner or batch.unowned or reviews >= 4 * len(state.obligations) + 1:
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
        for batch in b_valid_batches(state, index):
            edges.append((prefix + "initial_batch_" + b_batch_name(batch), b_reduce_valid_batch(state, batch, generation, reviews)))
        for profile in dismissal_profiles(state.findings):
            edges.append((prefix + "initial_dismissed_" + profile_name(profile), b_dismissed_from_attempt(state, index, "recheck_initial", reviews, profile, "pre_existing")))
    else:
        edges.append((prefix + "reopen_clean", BState(state.phase, replace(state.obligations, index, "closed1"), reviews, "active", state.findings)))
        settled_owner = tuple(f for f in state.findings if f.owner == owner and f.disposition in ("resolved", "dismissed"))
        if settled_owner:
            findings = update_findings(state.findings, lambda f: f.owner == owner and f.disposition in ("resolved", "dismissed"), "open")
            edges.append((prefix + "material_new_evidence_existing", BState(state.phase, replace(state.obligations, index, "open1"), reviews, "active", findings)))
        for batch in b_valid_batches(state, index):
            edges.append((prefix + "reopen_batch_" + b_batch_name(batch), b_reduce_valid_batch(state, batch, generation, reviews)))
        for profile in dismissal_profiles(state.findings):
            edges.append((prefix + "material_new_evidence_dismissed_" + profile_name(profile), b_dismissed_from_attempt(state, index, "recheck_reopen", reviews, profile, "reopened")))
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
    passed_state = BState(state.phase, replace(state.obligations, index, next_closed), reviews, "active", passed)
    edges.append((prefix + "pass_joint", passed_state))
    other_owners = tuple(owner_index for owner_index, stage in enumerate(state.obligations) if owner_index != index and stage in ("untested", "closed0", "closed1"))
    for batch in b_valid_batches(state, index, other_owners):
        observed = b_reduce_valid_batch(passed_state, batch, generation, reviews, False)
        edges.append((prefix + "pass_with_batch_" + b_batch_name(batch), observed))
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
    for batch in b_valid_batches(state, -1):
        observed = b_reduce_valid_batch(BState(state.phase, state.obligations, reviews, "active", state.findings), batch, 0, reviews, False)
        edges.append(("blind_closure_batch_" + b_batch_name(batch), b_terminal(observed)))
    for profile in dismissal_profiles(state.findings):
        findings = mint_profile(state.findings, profile, "blind", "pre_existing", "awaiting_recheck")
        edges.append(("blind_closure_dismissed_" + profile_name(profile), BState(state.phase, state.obligations, reviews, "recheck_blind", findings)))
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


def scope_digest(obligations, exclusions):
    canonical = "obligations=" + "\x1f".join(sorted(obligations)) + "\x1eexclusions=" + "\x1f".join(sorted(exclusions))
    return sha256(canonical.encode("ascii")).hexdigest()


@dataclass(frozen=True)
class Predecessor:
    family_id: str
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
    return all((
        predecessor.terminal,
        structured_delta,
        exact_predecessor_digest,
        exact_successor_digest,
        successor.predecessor_id == predecessor.family_id,
        successor.predecessor_spend == predecessor.review_spend,
        successor.carried_findings == predecessor.carried_findings,
        successor.authority_origin == "new_human_receipt",
        receipt.predecessor_id == predecessor.family_id,
        receipt.successor_id == successor.family_id,
        receipt.predecessor_scope_digest == predecessor.scope_digest,
        receipt.successor_scope_digest == successor.scope_digest,
        bool(receipt.presented_options),
        receipt.chosen_successor in receipt.presented_options,
        receipt.chosen_successor == successor.family_id,
        receipt.predecessor_spend == predecessor.review_spend,
        receipt.carried_findings == predecessor.carried_findings,
        receipt.materially_different,
    ))


def scope_expanded_route(severity, recheck=None):
    if severity == "low":
        return "backlogged"
    if severity == "medium":
        return "terminal_scope_decision"
    if recheck is None:
        return "awaiting_scope_recheck"
    if severity == "high":
        return "terminal_scope_decision" if recheck == "upheld" else "in_scope"
    return "serious_blocked"


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


def b_owner_state_matches(state):
    for finding in state.findings:
        if not is_outstanding(finding) or not finding.owner.startswith("o"):
            continue
        stage = state.obligations[b_owner_index(finding.owner)]
        if finding.disposition == "open" and not stage.startswith("open"):
            return False
        if finding.disposition == "pending_verification" and not stage.startswith("pending"):
            return False
        if finding.disposition == "awaiting_recheck" and not stage.startswith("recheck"):
            return False
    if state.control in ("active", "terminal", "serious_blocked"):
        for index, stage in enumerate(state.obligations):
            owner_findings = tuple(f for f in state.findings if f.owner == b_owner(index) and is_outstanding(f))
            if stage.startswith("open") and not any(f.disposition == "open" for f in owner_findings):
                return False
            if stage.startswith("pending") and not any(f.disposition == "pending_verification" for f in owner_findings):
                return False
            if stage.startswith("recheck") and not any(f.disposition == "awaiting_recheck" for f in owner_findings):
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
    bad_foreclosure_state = sum(1 for state in result["seen"] if state.control in ("active", "repair", "verify") and a_cannot_complete(state, need, 5, 2))
    assert bad_upheld_unlock == 0
    assert bad_foreclosure_state == 0
    print("A phase=%s risk=%s floor=%s finding_cap=%d normal=5 reserve=2 required=%d states=%d edges=%d terminal=%d acyclic=%s min_reviews=%d max_reviews=%d mixed_low_critical=%d parent_child=%d bad_delivery=%d bad_unverified_delivery=%d bad_critical_clear=%d bad_bound=%d bad_upheld_unlock=%d bad_foreclosure_state=%d" % (
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
        bad_foreclosure_state,
    ))


def check_c(phase, risk):
    start = CState(phase, "discovery", 0, (), "none", False)
    result = walk(start, lambda state: c_edges(state, risk), ("complete", "delivered_residual"), 4)
    assert_common(result)
    bad_acceptance_blind_bypass = sum(1 for state in result["seen"] if phase == "acceptance" and state.control == "complete" and not state.blind_visited)
    assert bad_acceptance_blind_bypass == 0
    print("C phase=%s risk=%s floor=%s finding_cap=%d stages=4 repairs=2 states=%d edges=%d terminal=%d acyclic=%s min_reviews=%d max_reviews=%d mixed_low_critical=%d parent_child=%d bad_delivery=%d bad_unverified_delivery=%d bad_critical_clear=%d bad_bound=%d bad_acceptance_blind_bypass=%d" % (
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
    predecessor = Predecessor("F1", predecessor_obligations, (), scope_digest(predecessor_obligations, ()), True, 7, carried)
    unchanged = predecessor
    successor_obligations = ("O1", "O2", "O3")
    successor = Successor("F2", "F1", successor_obligations, (), scope_digest(successor_obligations, ()), 7, carried, "new_human_receipt")
    receipt = SuccessorReceipt("F1", "F2", predecessor.scope_digest, successor.scope_digest, ("F2", "abandon"), "F2", 7, carried, True)
    accepted_different = successor_authorised(predecessor, successor, receipt)
    same_scope = dc_replace(successor, obligations=predecessor.obligations, scope_digest=predecessor.scope_digest)
    reordered_scope = dc_replace(successor, obligations=("O2", "O1"), scope_digest=predecessor.scope_digest)
    missing_receipt = None
    missing_options = dc_replace(receipt, presented_options=())
    wrong_family = dc_replace(receipt, predecessor_id="F9")
    wrong_predecessor_digest = dc_replace(receipt, predecessor_scope_digest="wrong")
    wrong_successor_digest = dc_replace(receipt, successor_scope_digest="wrong")
    missing_carry = dc_replace(receipt, carried_findings=carried[:1])
    fresh_authority = dc_replace(successor, predecessor_spend=0, authority_origin="predecessor_unspent")
    accepted_same = successor_authorised(predecessor, same_scope, dc_replace(receipt, successor_scope_digest=same_scope.scope_digest))
    accepted_reordered = successor_authorised(predecessor, reordered_scope, dc_replace(receipt, successor_scope_digest=reordered_scope.scope_digest))
    accepted_missing_receipt = successor_authorised(predecessor, successor, missing_receipt)
    accepted_missing_options = successor_authorised(predecessor, successor, missing_options)
    accepted_wrong_family = successor_authorised(predecessor, successor, wrong_family)
    accepted_wrong_predecessor_digest = successor_authorised(predecessor, successor, wrong_predecessor_digest)
    accepted_wrong_successor_digest = successor_authorised(predecessor, successor, wrong_successor_digest)
    accepted_missing_carry = successor_authorised(predecessor, successor, missing_carry)
    accepted_fresh_authority = successor_authorised(predecessor, fresh_authority, receipt)
    predecessor_immutable = predecessor == unchanged
    assert accepted_different
    assert not any((accepted_same, accepted_reordered, accepted_missing_receipt, accepted_missing_options, accepted_wrong_family, accepted_wrong_predecessor_digest, accepted_wrong_successor_digest, accepted_missing_carry, accepted_fresh_authority))
    assert predecessor_immutable
    print("B successor structured_cases=10 accepted_different=%s bad_same_scope=%d bad_reordered_scope=%d bad_missing_receipt=%d bad_missing_options=%d bad_wrong_family=%d bad_wrong_predecessor_digest=%d bad_wrong_successor_digest=%d bad_missing_carry=%d bad_fresh_authority=%d bad_predecessor_mutation=%d" % (str(accepted_different).lower(), int(accepted_same), int(accepted_reordered), int(accepted_missing_receipt), int(accepted_missing_options), int(accepted_wrong_family), int(accepted_wrong_predecessor_digest), int(accepted_wrong_successor_digest), int(accepted_missing_carry), int(accepted_fresh_authority), int(not predecessor_immutable)))


def check_scope_controls():
    low = scope_expanded_route("low")
    medium = scope_expanded_route("medium")
    high_referral = scope_expanded_route("high")
    high_upheld = scope_expanded_route("high", "upheld")
    high_overturned = scope_expanded_route("high", "overturned")
    critical_referral = scope_expanded_route("critical")
    critical_upheld = scope_expanded_route("critical", "upheld")
    critical_overturned = scope_expanded_route("critical", "overturned")
    expected = ("backlogged", "terminal_scope_decision", "awaiting_scope_recheck", "terminal_scope_decision", "in_scope", "awaiting_scope_recheck", "serious_blocked", "serious_blocked")
    actual = (low, medium, high_referral, high_upheld, high_overturned, critical_referral, critical_upheld, critical_overturned)
    bad_scope_route = int(actual != expected)
    assert bad_scope_route == 0
    print("Scope controls low=%s medium=%s high_referral=%s high_upheld=%s high_overturned=%s critical_referral=%s critical_upheld=%s critical_overturned=%s bad_scope_route=%d" % (low, medium, high_referral, high_upheld, high_overturned, critical_referral, critical_upheld, critical_overturned, bad_scope_route))


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
    bad_reopen_before_initial = sum(1 for source, action, target in result["edges_data"] if ("material_new_evidence" in action or "reopen_clean" in action or "reopen_batch" in action) and "untested" in source.obligations)
    unowned_critical_states = sum(1 for state in result["seen"] if any(f.owner == "unowned" and f.severity == "critical" and is_outstanding(f) for f in state.findings))
    unowned_critical_delivery = sum(1 for state in result["seen"] if state.control in ("complete", "delivered_residual") and any(f.owner == "unowned" and f.severity == "critical" for f in state.findings))
    cross_owner_low_critical = sum(1 for state in result["seen"] if any(is_outstanding(low) and low.severity == "low" and low.owner.startswith("o") and any(is_outstanding(critical) and critical.severity == "critical" and critical.owner.startswith("o") and critical.owner != low.owner for critical in state.findings) for low in state.findings))
    atomic_cross_owner_low_critical = sum(1 for source, action, target in result["edges_data"] if b_atomic_cross_owner_low_critical(source, action, target))
    multi_initial_batch = sum(1 for source, action, target in result["edges_data"] if "initial_batch" in action and sum(1 for before, after in zip(source.obligations, target.obligations) if before == "untested" and after != "untested") > 1)
    bad_owner_state = sum(1 for state in result["seen"] if not b_owner_state_matches(state))
    assert bad_reopen_before_initial == 0
    assert bad_owner_state == 0
    if obligations > 0:
        assert unowned_critical_states > 0
    if obligations > 1:
        assert cross_owner_low_critical > 0
        assert atomic_cross_owner_low_critical > 0
        assert multi_initial_batch > 0
    assert unowned_critical_delivery == 0
    print("B phase=%s obligations=%d floor=%s finding_cap=%d bound=%d states=%d edges=%d terminal=%d acyclic=%s min_reviews=%d max_reviews=%d mixed_low_critical=%d parent_child=%d cross_owner_low_critical=%d atomic_cross_owner_low_critical=%d multi_initial_batch=%d unowned_critical=%d bad_owner_state=%d bad_unowned_critical_delivery=%d bad_reopen_before_initial=%d bad_delivery=%d bad_unverified_delivery=%d bad_critical_clear=%d bad_bound=%d" % (
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
        unowned_critical_states,
        bad_owner_state,
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
        check_scope_controls()
    if args.mode in ("C", "all"):
        check_c(args.phase, args.risk)


if __name__ == "__main__":
    main()
