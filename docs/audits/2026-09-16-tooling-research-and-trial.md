# Tooling research and Rust library trial

Date: 2026-09-16.

## Authority and evidence

The [historical decision revalidation](2026-09-09-historical-decision-revalidation.md) remains the decision authority. It selects a deterministic Mealy-machine core inside agent-flow with provider-neutral backends. The reset did not abandon that direction. Historical direction does not approve implementation.

This report synthesises the checked alternatives study, library trial outcomes, later human acceptance and a separate OpenShell assessment. It preserves conclusions rather than raw sessions or private execution records. It creates no task, adoption, prototype, issue or execution authority.

The researcher's provisional recommendation to pause custom development concerned demonstrated value and maintenance cost. It did not supersede the retained architecture. Current agent-flow supplies contracts and state projections, not the proposed automated controller.

## Alternatives study, 2026-09-11

The original study covered twelve supplied sources. OpenShell and VeriGuard were assessed later and were not part of that study. The checker supported selective methodological reuse with specific qualifications.

OpenSpec offered specification exploration and scenario conventions. Stately Agent was the closest state-machine fit. LangGraph offered persistent, parallel and interruptible orchestration. None established a complete externally authorised dispatch contract with cumulative accounting, independent evidence and role-specific isolation.

The checker materially qualified the comparison:

- Stately documents cumulative budgets in machine context across snapshot resume. Its per-run counter alone is an incomplete account. Executor reporting and dropped events limit accounting completeness.
- Only LangGraph's Python implementation was inspected. Its JS/TS implementation was not evaluated, including its guarantees and adoption costs.
- OpenSpec artefact completion and structural validation do not establish specification adequacy or delivered behaviour.
- Swamp's matching source revisions establish provenance and source licensing. They do not settle separate website or registry terms, or credential assurances.

The remaining sources supplied ideas about counterexamples, explicit memory, provenance and review. Their benchmarks did not establish effectiveness for software delivery here. Authorisation gates complement containment. Different model identities do not themselves establish independent evidence.

No candidate code was installed, built, tested or executed. No framework was adopted. Publisher benchmark claims were not reproduced results.

## Rust library trial and follow-ups

The trial explicitly used [agent-flow prompt assets][prompts] at `a64d6c27a2171b5fe311f7ab05f1d8cbe8aeff2d`. Manual Pi/Podman execution supplied isolation and coordination. This evaluated prompts and operating procedures, not an automated controller.

Independent review and triage established nine valid defect groups. Two important defects passed the existing gates: marked multi-shot constructors admitted `BoxBrand`, and shared continuation queues copied quadratically. Corrections restricted marked constructors to `RcBrand` and introduced persistent shared Rc and Arc queues.

Other groups covered:

- Qualified-path generic detection.
- Generated-name collisions.
- Generated API documentation validation.
- Defaulted generics.
- Malformed multi-shot markers.
- Tagged-handler diagnostics.
- Stale public documentation.

The initial verifier returned PASS for all nine groups. Required library checks were `just verify` and `just effects-feature-off`. Both passed on the corrected candidate and during independent verification.

Public-documentation defects later escaped that initial review. A separately authorised documentation correction ended with FAIL because related Shift documentation remained stale outside its edit boundary. Nonzero verification commands also contributed under that execution's rules. Passing library gates did not resolve the inaccurate public claim.

A second documentation execution corrected the Shift facts. Its verifier returned FAIL for one prohibited semicolon, despite passing factual checks and both required gates. The human then prescribed a literal punctuation replacement and accepted deterministic checks plus the prior independent evidence. Both library gates passed again. This acceptance was not a new independent PASS.

Complete accounting excludes coordinator work:

- The first trial used seven authorised dispatches, including a timed-out specialist and its replacement.
- Two documentation executions used two authorised roles each.
- An intended shell preflight accidentally invoked the image's agent entrypoint, adding one unintended model-backed execution.
- The final human-directed correction and adoption added no worker.

The total was 11 authorised dispatches plus one unintended model-backed execution. The resulting handoff is [rust-fp-library PR #46][library-pr]. Earlier local outcomes describe unpublished intermediate stages. They do not describe the final handoff, and the supplied PR snapshot establishes no current PR status.

The prompts helped bound scope, require evidence and separate triage from correction. Manual overlays resolved current-tree review assumptions and absent workflow state. Read-only mounts required scratch copies for checks that wrote caches. Environment setup, credential handling, timeouts and dispatch accounting imposed considerable coordination cost.

The trial supplied useful defect evidence. It did not establish statistical prompt superiority or controller return on investment. The agreed real-project reassessment occurred. No automatic pilot enrolment follows.

## Additional OpenShell assessment, 2026-09-16

The [formal-methods article][article] and linked [adversarial study][adversarial] were read alongside pinned documentation and relevant source. The inspected [main prover][openshell-main] checks four permission-risk categories: `link_local_reach`, `l7_bypass_credentialed`, `credential_reach_expansion` and `capability_expansion`.

These concern metadata reach, credentialed protocol bypass, newly credentialed endpoints and additional HTTP methods. Findings inform change review and control optional auto-approval. They do not determine semantic intent. Results depend on policy encoding, credential inputs and binary capability descriptions. The main model is per-sandbox and does not observe actual proxy decisions.

The separate [maximum-policy spike][spike] asks whether a candidate permits any modelled action outside an approved maximum. Its symbolic network model covers L4, REST and WebSocket actions. L4 authority can exceed inspected method and path restrictions.

Unsupported surfaces and solver `unknown` results refuse approval through `Unsupported`. Unsupported surfaces include deny rules, query constraints, GraphQL, MCP and CIDR controls. The narrowness scores are coarse heuristics, not calibrated security measures. Neither this spike nor the main prover proves every runtime or cross-sandbox property.

The adversarial study reports no observed protected repository mutations. One malformed approval was blocked by schema validation before activation. That outcome does not isolate the prover's contribution. No comparison removes only the prover while holding other controls constant.

The study attributes 416 decisions inconsistently between its combined-session summary and its ten-session table. The [research harness][harness] acknowledges polling limits. A mutation created and removed between checks can escape observation. These limits preclude an absolute security conclusion.

The human retained OpenShell for a later backend comparison without adoption, a prototype or issue creation. Formal methods for deterministic checks remain a preference independently of OpenShell. Any proof claim needs explicit assumptions and model-to-enforcement correspondence. Solver success alone does not prove the whole system.

## Related VeriGuard assessment

[VeriGuard v1][veriguard] was submitted on 2025-10-03. Sections 3.2, 3.3 and 5.3 distinguish specification generation, verification and runtime integration.

LLMs generate policy code and contracts. Nagini verifies policy code against those contracts, not against unformalised human intent. Human validation remains necessary to establish that the specification expresses the intended constraints. The paper acknowledges limitations in generated specifications and the verifier's supported language.

Runtime policy arguments are extracted by an LLM from agent data. That interpretation remains distinct from verified policy code. Enforcement also depends on integration that intercepts actions and applies the resulting decision. A proof of the policy function does not prove extraction accuracy or complete interception.

Figure 2 reaches zero measured attack success at validation, before formal verification. The study does not show that the proof step caused that reduction. No implementation or result was reproduced here. This assessment selects no Python, Nagini or other dependency.

## Unresolved configuration context

The later proposal favours one project configuration entry point referencing shared assets inside or outside the project. Project-owned `AGENTS.md`, specifications and tests remain. State placement, pack identity and updates, and actual harness discovery remain undecided. No illustrative filename or digest schema is selected. This remains design context, not a task list.

## Source references

The twelve-source study is discoverable through these pinned repository references and its two website sources. Swamp's two inspected origins shared one revision.

- [Kepler][kepler], [CCARC][ccarc], [Tycho][tycho] and [Retrodict][retrodict].
- [LangGraph][langgraph], [Lemmalog][lemmalog], [Stately Agent][stately] and [OpenSpec][openspec].
- [Swamp source][swamp], [Swamp website][swamp-web], [Open Code Review][review], [ATLAS][atlas] and [Fences, not Sandboxes][fences].

The [Stately budget documentation][budgets] preserves the cumulative-resume qualification. Website references identify the study's sources, not immutable snapshots.

[kepler]: https://github.com/Cveinnt/kepler/tree/f732c84d30685e70f892d3c4cbed093acaef54c2
[ccarc]: https://github.com/dastin359/CCARC/tree/ca9b96e7518c75fdad3d23820c9569a10181b654
[tycho]: https://github.com/NIMI-research/Tycho/tree/f68912a764372ead0a610db2e1c011d41ce5197e
[retrodict]: https://github.com/ryanbbrown/Retrodict/tree/71672e8e5adb008360f52a61ef9e2adf91a62d89
[langgraph]: https://github.com/langchain-ai/langgraph/tree/e539ac122f4126f6dd850581c1494948cf620e31
[lemmalog]: https://github.com/JordyZomer/lemmalog/tree/74d428a2497066795f6328946457f22d713fcbd5
[stately]: https://github.com/statelyai/agent/tree/ecd27f1327fea6ea1c8f9af736a4226047eac23e
[budgets]: https://github.com/statelyai/agent/blob/ecd27f1327fea6ea1c8f9af736a4226047eac23e/docs/usage-and-budgets.md#L193-L200
[openspec]: https://github.com/Fission-AI/OpenSpec/tree/9d4e5974e5c0d9a09b9c6c1e1eb0975e80ec4461
[swamp]: https://github.com/systeminit/swamp/tree/ae1ed1492de7943eaff247deac709de0b748cb39
[swamp-web]: https://swamp-club.com/
[review]: https://github.com/alibaba/open-code-review/tree/7f8f254d8407b26edff06f2e3a5940906f1f28ae
[atlas]: https://github.com/itigges22/ATLAS/tree/ef616c5d2797f3e54dbe2aa33f8159049e144965
[fences]: https://yegge.ai/essays/fences-not-sandboxes/
[prompts]: https://github.com/nothingnesses/agent-flow/tree/a64d6c27a2171b5fe311f7ab05f1d8cbe8aeff2d/.agents/prompts
[library-pr]: https://github.com/nothingnesses/rust-fp-library/pull/46
[article]: https://nvidia.github.io/OpenShell-Research/dev-notes/posts/2026-09-10-learning-formal-methods-agent-policy-prover/
[adversarial]: https://nvidia.github.io/OpenShell-Research/dev-notes/posts/2026-08-27-adversarial-policy-review-long-horizon-agents/
[openshell-main]: https://github.com/NVIDIA/OpenShell/tree/9b52b43b39bbcc3b195e073317f40f7ecf6fa363/crates/openshell-prover
[spike]: https://github.com/NVIDIA/OpenShell/blob/df0ee1aaaf6af7ee6193b785fd189449a3848fe0/crates/openshell-prover/MAXIMUM_POLICY_ENVELOPE_SPIKE.md
[harness]: https://github.com/NVIDIA/OpenShell-Research/tree/268361f147fec7f265e428930d6bf5e58f0fda32/projects/long-horizon-agent-evals
[veriguard]: https://arxiv.org/html/2510.05156v1
