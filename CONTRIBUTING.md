# Contributing to Phorge

Thank you for your interest. Phorge is built in the open and welcomes issues, reviews, documentation and code.
By taking part you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Before you start

1. Read [AGENTS.md](AGENTS.md) for the map of the repositories and [GOVERNANCE.md](GOVERNANCE.md) for how work is tracked.
2. Look at the [Roadmap](https://github.com/orgs/phorge-fr/projects) and the open issues; someone may already be on it.
3. For a security problem, **do not open a public issue**: follow [SECURITY.md](SECURITY.md).

## Proposing a change

1. **Open or pick an issue** using one of the templates. For anything non-trivial, agree on the approach in the issue first.
   Issues that are good first steps carry the `good first issue` label.
2. **Fork or branch** from an up-to-date `main`: `feat/...`, `fix/...`, `docs/...`, `chore/...`. Maintainers never commit to `main` directly either.
3. **Make a focused change** that matches the surrounding code and docs. Run the repository's checks (see its README or `AGENTS.md`).
4. **Open a pull request** in English that says `Closes #N` (a pull request always closes an issue, and an issue is closed only by a pull request), explains what changed and how you tested it. Fill in the template.
5. **Respond to review.** A maintainer merges once checks are green and the change is understood.

## Standards

- Commits: English, imperative, conventional prefix (`feat(scope): ...`, `fix: ...`, `docs: ...`).
- No secrets, credentials, private keys, tokens or personal data in commits, issues or screenshots.
- New infrastructure workloads ship with their network policy and their monitoring in the same pull request.
- New dependencies must have a license compatible with the repository's; mention it in the pull request.
- Documentation is part of the change. Keep it short, accurate and in English.

## Documentation

A change that alters behavior updates its documentation in the same pull request. Pages follow [the documentation standard](docs/reference/documentation-standard.md) and pass the `docs-lint` check.

## Logging time

Maintainers and regular contributors log time with a comment, `/time 1h30 what was done`. See [GOVERNANCE.md](GOVERNANCE.md#time-tracking).
It is optional for one-off contributions.

## Using AI assistants

Allowed, under the same rules as any contribution: you are responsible for what you submit, you must understand it and have
tested it, and it must not contain secrets or third-party code you cannot relicense. Agents read [AGENTS.md](AGENTS.md).

## Questions

Open a discussion or an issue with the `question` template, or see [SUPPORT.md](SUPPORT.md).
