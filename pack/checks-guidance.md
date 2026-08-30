## Optional deterministic checks

This project enabled the `checks` module. `.agents/checks.toml`, `.agents/checks/`, and `.agents/hooks/` are product-development tooling, not task state and not proof of independent review.

Run `agent-flow checks` for the working tree or `agent-flow checks --staged` for staged content. The tool executes the configured lint and format-check commands in temporary isolation. The optional `.agents/prompts/checks-reviewer.md` can report these results during product review, but it does not replace the independent reviewer.

The scaffolded `.agents/hooks/pre-commit` is inert until activated. `--with-precommit-hook` installs a create-if-absent delegate only when `--module checks` is selected; it never overwrites an existing hook. You may instead link it from the repository root after checking that no hook exists: `ln -s ../../.agents/hooks/pre-commit .git/hooks/pre-commit`.
