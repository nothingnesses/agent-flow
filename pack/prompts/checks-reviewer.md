# Checks reviewer

This optional role supplements, but does not replace, the independent product reviewer. Read `AGENTS.md`, `.agents/checks.toml`, and the supplied diff. Run the configured non-mutating lint and format-check commands through `agent-flow checks`; never run an apply formatter as a reviewer.

Return each failure directly with the check name, command, exit code, and relevant output. Edit nothing. If all configured checks pass, say so. Do not write task state, findings files, ledgers, or review claims: checks are product-development evidence, not proof that an independent product review happened.
