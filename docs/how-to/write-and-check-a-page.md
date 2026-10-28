---
type: how-to
audience: contributor adding or changing documentation
verified: 2026-10-28
---

# Write and check a page

## Before you start

You need a clone of the repository and Python 3. The prose and link checks need [Vale](https://vale.sh) and [lychee](https://lychee.cli.rs); the Markdown check needs Node.js.

## Write the page

1. Decide the type with [the standard](../reference/documentation-standard.md#the-five-page-types). If the page would need two types, write two pages.
2. Copy the template of that type (`templates/docs/<type>.md` in this repository, for example [how-to](../../templates/docs/how-to.md)) into the matching folder of the repository's `docs/`.
3. Fill the header: `type`, `audience`, and `verified` (the date you ran the steps).
4. Add one line for the page to `docs/README.md`.

## Check it

From the root of the repository that holds the page, with a clone of this repository next to it at `../.github`:

1. Check the header and layout:

   ```bash
   python3 ../.github/scripts/check_docs.py .
   ```

2. Check the Markdown:

   ```bash
   npx --yes markdownlint-cli2@0.23.3 --config ../.github/docs-lint/markdownlint.yaml "docs/**/*.md" "README.md"
   ```

3. Check the links on disk:

   ```bash
   lychee --offline --include-fragments --config ../.github/docs-lint/lychee.toml docs README.md
   ```

4. Check the prose:

   ```bash
   vale --config ../.github/docs-lint/vale.ini sync
   vale --config ../.github/docs-lint/vale.ini docs
   ```

Every command prints nothing or an error you can act on. Fix the errors, then open the pull request; the same checks run there.
