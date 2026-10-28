---
type: reference
audience: anyone who writes or reviews documentation in a phorge-fr repository
verified: 2026-10-28
---

# Documentation standard

Every repository of the organization documents itself the same way, so that a person or an agent knows where to look and what a page promises. The structure follows [Diátaxis](https://diataxis.fr); decisions follow [MADR 4.0](https://adr.github.io/madr/); the prose follows the [Google developer documentation style guide](https://developers.google.com/style).

## The five page types

A page has exactly one type. If a page needs two, split it.

| Type | Folder | The reader wants to | Written as |
| --- | --- | --- | --- |
| Tutorial | `docs/tutorials/` | Learn by doing something small that always works | A guided path with a visible result at each step. No options, no theory |
| How-to | `docs/how-to/` | Get a specific task done | Numbered steps for a reader who already knows the basics. States prerequisites, how to verify, how to undo |
| Reference | `docs/reference/` | Look up a fact | Dry, complete, structured like the thing it describes. No opinions, no steps |
| Explanation | `docs/explanation/` | Understand why | Prose that gives context, trade-offs and the shape of the system. No steps |
| Decision | `docs/decisions/` | Know why a choice was made | One [MADR](https://adr.github.io/madr/) record per decision, numbered |

A runbook is a how-to. An architecture overview is an explanation, and the table of VLANs it mentions is reference. Mixing the types is the usual way a page goes bad.

Generated reference (an OpenAPI file, a command-line help text) is linked, not copied.

## Layout

```text
docs/
  README.md          index, one line per page grouped by type
  tutorials/
  how-to/
  reference/
  explanation/
  decisions/
    0001-short-title.md
```

A folder exists only if it holds a page. `README.md` at the root of the repository says what the repository is and links to `docs/`. `AGENTS.md` holds the instructions for a person or an agent working in the repository; it links to the documentation and does not repeat it.

## Page header

Every page except an index (`README.md`) starts with a front matter block:

```yaml
---
type: how-to
audience: operator who restarts a cluster
verified: 2026-10-28
---
```

| Key | Meaning | Required |
| --- | --- | --- |
| `type` | One of `tutorial`, `how-to`, `reference`, `explanation`. Must match the folder | Always |
| `audience` | Who reads this, in a few words | Always |
| `verified` | The date someone last ran the steps or checked the facts, `YYYY-MM-DD` | Tutorials and how-tos; recommended for reference |

The title is the single `#` heading, written in sentence case.

Decision records use the MADR header instead: `status`, `date`, `decision-makers` (and optionally `consulted`, `informed`). The filename is `NNNN-short-title.md`. Start from [the template](../../templates/docs/decision.md). A decision is never rewritten: a new record supersedes it and the old one is marked `superseded by ...`.

## Rules against empty documentation

1. A page has a reader and a purpose, written in its header. No reader, no page.
2. A procedure is true: its commands were run, and `verified` says when. Past 180 days a warning is raised; update the date only after checking.
3. One fact lives in one place. Everything else links to it.
4. Prefer generating to writing, and linking to copying.
5. No placeholder pages. A page exists the day it has content that helps.
6. Nothing sensitive: no credentials, key locations, private addresses, or exploitable weaknesses. See `SECURITY.md`.
7. Delete or fix a page that is wrong; do not leave it with a disclaimer.

## Writing

English, plain, and direct. Write in the present tense and the active voice, address the reader as "you" in tutorials and how-tos, and keep one idea per sentence. Name things as the tool names them. Prefer a short example over an adjective. Link the first mention of a term that needs explaining.

## Checks

A pull request that touches documentation must pass the shared `docs-lint` workflow:

| Check | Tool | Fails the pull request on |
| --- | --- | --- |
| Header and layout | `scripts/check_docs.py` | Missing or invalid header, a page outside the five folders, no single title |
| Markdown | markdownlint | Rule violations of `docs-lint/markdownlint.yaml` |
| Links | lychee | A broken internal link or anchor. External links are checked on a schedule |
| Prose | Vale with the Google style | Errors. Warnings are shown but do not block |

Run them locally with [Write and check a page](../how-to/write-and-check-a-page.md).
