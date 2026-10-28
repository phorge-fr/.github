# Governance and project management

How Phorge plans, tracks and reports its work. These rules apply to every repository of the organization; a repository can add
stricter ones in its own `AGENTS.md`.

## Roles

- **Maintainer** ([@l-nmch](https://github.com/l-nmch)): sets priorities, assigns work, reviews and merges.
- **Contributor**: anyone who opens an issue or a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md).
- **Agent**: an AI assistant working for a maintainer or contributor. It follows the same rules as a person and is accountable to
  the human it works for.

Decisions are made in the open, in issues or in a short decision record (`docs/decisions/NNNN-title.md`) when they shape the
architecture. A decision that is revisited gets a new record that supersedes the old one.

## Issues

Every unit of work is an issue, in the repository it changes. An open issue carries:

| Property | Where | Values |
| --- | --- | --- |
| Type (the "tag", exactly one) | Issue type | Epic, Feature, Task, Bug, Chore, Security, Docs |
| Area (exactly one) | `area/*` label | `control`, `core`, `svc`, `platform`, `network`, `storage`, `compute`, `api`, `crossplane`, `observability`, `security`, `docs`, `ci`, `brand`, `legal` |
| Priority | Project field | P0 (now, blocks everything), P1 (this quarter), P2 (planned), P3 (nice to have) |
| Estimate | Project field `Estimate (h)` | Hours of focused work, rounded up |
| Time spent | Project field `Spent (h)` | Filled from `/time` comments |
| Assignee | Issue | One person |
| Milestone | Issue | `2026-Q4`, `2027-Q1`, `2027-Q2` or `Backlog` (closed past quarters, `2025-Q4` and `2026-Q3`, hold finished history) |
| Project | Issue | At least one of the organization projects |

Titles are in English. In **Hangar** they read `<cluster>/<subject>: Description` (`core/authentik: ...`, `all/security: ...` for
topics that span clusters). Elsewhere they are plain imperative sentences.

An **Epic** is an issue whose work is split into **sub-issues** (GitHub sub-issues). It lives in the repository that owns most of
the work, or in this repository when it spans several. Its estimate is the sum of its sub-issues'.

A finding made while working gets its own issue. An issue is closed only when its work is done; leftovers are moved to a new
issue and linked before closing. The closing comment lists the pull requests and what was verified.

### Statuses

`Backlog` -> `Ready` (has type, priority, estimate, milestone) -> `In progress` -> `In review` -> `Done`. Status is set by the
project's built-in workflows when a pull request is opened or merged and an issue is closed.

## Pull requests

- Branch off an up-to-date `main`, named `feat/`, `fix/`, `docs/`, `chore/` + short subject. Never commit to `main`.
- The pull request description is in English, references its issue (`Closes #N`; `Refs #N` for a partial step) and says what was
  tested. The issue and the pull request carry the same label, milestone and project.
- It has an assignee and a requested reviewer. Review ownership comes from `CODEOWNERS`. Since a single maintainer cannot
  approve their own pull request, "reviewed" means a reviewer was requested and checks are green; whoever merges states what was
  verified.
- Required checks must pass. The `pr-governance` check verifies the issue link, label, milestone and assignee.
- Exempt from the issue link: Renovate, Dependabot and release-please pull requests.
- Squash or merge as the repository prefers; keep commit messages in English, imperative, with a conventional prefix
  (`feat(scope):`, `fix(scope):`, `docs:`, `chore:`).

## Time tracking

GitHub has no native time tracking, so Phorge uses a comment convention.

```text
/time 1h30 debugged the Cilium policy for the exporter
/time 45m reviewed the compositions
/time 2h @2026-10-27 pairing on the API (for work done on another day)
```

- Write it on the issue or the pull request the time was spent on. One command per line; several per comment are fine.
- Units: `h` and `m`, combined (`1h30`, `1h 30m`, `90m`). Default date is the comment's.
- The `time-tracking` workflow runs hourly and sums the entries of each item into the `Spent (h)` field of its project items.
- Every Monday a report (per day, per author, per issue and per pull request) is posted as a comment on the issue `all/time: Time reports` in this repository. `scripts/time_tracking.py report phorge-fr` produces it on demand.
- Edit or delete a wrong comment; totals are recomputed.

## Milestones and roadmaps

Milestones are per repository, so every repository uses the same names and due dates. Quarterly milestones are the commitment;
`Backlog` is unscheduled. The public projects are:

- **Roadmap**: epics only, timeline by quarter. Start here.
- **Platform**: Hangar, Network, Ansible.
- **Cloud API & Providers**: phorge-api, providers, the console.
- **Security & Compliance**: audits, pentest, GDPR, licenses.
- **Community & Brand**: community files, READMEs, branding.

## Security and transparency

Everything is public by default, with two exceptions: secrets and unfixed weaknesses. Audit scope, method, status and the sanitized
outcome are public; raw findings go to a private [advisory](SECURITY.md) until they are fixed. See also `docs/gdpr.md` in Hangar for
personal-data handling.

## Licenses

Every repository of the organization is licensed under the Apache License 2.0 (a `LICENSE` file at its root), and lists third-party licenses in `THIRD_PARTY_NOTICES.md`. A new dependency
is checked for compatibility before it is added.

## Documentation

Every repository documents itself by the same standard: five page types (tutorial, how-to, reference, explanation, decision), a header on every page, and shared checks in CI. See [the documentation standard](docs/reference/documentation-standard.md) and [how to write and check a page](docs/how-to/write-and-check-a-page.md).
