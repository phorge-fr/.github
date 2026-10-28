#!/usr/bin/env bash
# Apply labels.json and milestones.json to the organization's repositories.
# Usage: scripts/sync-repos.sh [--apply] [owner/repo ...]   (dry-run by default)
set -euo pipefail

here=$(cd "$(dirname "$0")/.." && pwd)
apply=0
if [[ ${1:-} == --apply ]]; then apply=1; shift; fi
repos=("$@")
if ((${#repos[@]} == 0)); then
  repos=(phorge-fr/Hangar phorge-fr/Network phorge-fr/Ansible phorge-fr/phorge-api phorge-fr/.github phorge-fr/gitea-phorge-theme)
fi

run() {
  if ((apply)); then "$@" >/dev/null; else echo "  DRY: $*"; fi
}

for repo in "${repos[@]}"; do
  echo "== $repo"
  existing=$(gh api "repos/$repo/labels" --paginate --jq '.[].name')
  jq -c '.[]' "$here/labels.json" | while read -r l; do
    name=$(jq -r .name <<<"$l"); color=$(jq -r .color <<<"$l"); desc=$(jq -r .description <<<"$l")
    if grep -Fxq -- "$name" <<<"$existing"; then
      run gh api -X PATCH "repos/$repo/labels/$(jq -rn --arg n "$name" '$n|@uri')" -f color="$color" -f description="$desc"
    else
      run gh api -X POST "repos/$repo/labels" -f name="$name" -f color="$color" -f description="$desc"
    fi
  done
  titles=$(gh api "repos/$repo/milestones?state=all" --paginate --jq '.[].title')
  jq -c '.[]' "$here/milestones.json" | while read -r m; do
    title=$(jq -r .title <<<"$m")
    if grep -Fxq -- "$title" <<<"$titles"; then continue; fi
    args=(-f title="$title" -f description="$(jq -r .description <<<"$m")" -f state="$(jq -r '.state // "open"' <<<"$m")")
    due=$(jq -r '.due_on // empty' <<<"$m")
    if [[ -n $due ]]; then args+=(-f due_on="$due"); fi
    run gh api -X POST "repos/$repo/milestones" "${args[@]}"
  done
done
