#!/usr/bin/env bash
# Replays the fork's commits that upstream does not have yet onto upstream/main and opens
# (or updates) a pull request to the upstream repository.
#
# Fork-only files (deploy / release automation, changelog) are left out of the contribution.
# Commits upstream already has (same patch, even with a different SHA) are skipped.
#
# Env: UPSTREAM_REPO (owner/name), CONTRIB_BRANCH, GH_TOKEN (needed unless DRY_RUN=1),
#      FORK_REF (default origin/main), DRY_RUN=1 (build the branch locally, don't push/PR)
set -euo pipefail

UPSTREAM_REPO="${UPSTREAM_REPO:?}"
CONTRIB_BRANCH="${CONTRIB_BRANCH:-contrib/upstream}"
FORK_REF="${FORK_REF:-origin/main}"
FORK_OWNER="${FORK_OWNER:-$(git remote get-url origin | sed -E 's#.*[:/]([^/]+)/[^/]+(\.git)?$#\1#')}"

# Paths that belong to the fork only.
EXCLUDES=(
  ':(exclude).github'
  ':(exclude)CHANGELOG.md'
  ':(exclude).release-please-manifest.json'
  ':(exclude)release-please-config.json'
)

git remote get-url upstream >/dev/null 2>&1 \
  || git remote add upstream "https://github.com/${UPSTREAM_REPO}.git"
git fetch --quiet upstream main

commits=()
while IFS= read -r line; do commits+=("$line"); done < <(
  git rev-list --reverse --no-merges --cherry-pick --right-only "upstream/main...${FORK_REF}"
)
echo "Fork commits not yet upstream: ${#commits[@]}"

git checkout -q -B "$CONTRIB_BRANCH" upstream/main
applied=()
for c in "${commits[@]}"; do
  # release-please version bumps only make sense in the fork
  if git log -1 --format=%s "$c" | grep -qE '^chore\(main\): release'; then
    echo "skip   $(git log -1 --format='%h %s' "$c") (fork release)"
    continue
  fi
  patch="$(git diff-tree -p --binary --no-commit-id "$c" -- . "${EXCLUDES[@]}")"
  if [ -z "$patch" ]; then
    echo "skip   $(git log -1 --format='%h %s' "$c") (fork-only files)"
    continue
  fi
  if ! printf '%s\n' "$patch" | git apply --index --3way; then
    echo "::error::Could not apply $(git log -1 --format='%h %s' "$c") onto upstream/main" >&2
    exit 1
  fi
  GIT_AUTHOR_NAME="$(git log -1 --format=%an "$c")" \
  GIT_AUTHOR_EMAIL="$(git log -1 --format=%ae "$c")" \
  GIT_AUTHOR_DATE="$(git log -1 --format=%aI "$c")" \
    git commit -q -m "$(git log -1 --format=%B "$c")"
  summary="$(git log -1 --format='%h %s' "$c")"
  applied+=("$summary")
  echo "apply  $summary"
done

if [ "${#applied[@]}" -eq 0 ]; then
  echo "Nothing to contribute."
  exit 0
fi
if [ "${DRY_RUN:-0}" = "1" ]; then
  echo "DRY_RUN: branch $CONTRIB_BRANCH built locally with ${#applied[@]} commit(s); not pushing."
  git diff --stat upstream/main | tail -20
  exit 0
fi

git push --force origin "$CONTRIB_BRANCH"

existing="$(gh pr list --repo "$UPSTREAM_REPO" --head "${FORK_OWNER}:${CONTRIB_BRANCH}" --state open --json number --jq '.[0].number // empty')"
if [ -n "$existing" ]; then
  echo "Updated existing PR #$existing (branch force-pushed)."
  exit 0
fi

body="$(printf 'Automatisch aus dem Fork `%s/%s` erstellt. Enthält:\n\n' "$FORK_OWNER" "${UPSTREAM_REPO#*/}"
        printf -- '- %s\n' "${applied[@]}"
        printf '\nOhne Workflows, Deployment- und Release-Automatisierung des Forks.\n')"
gh pr create --repo "$UPSTREAM_REPO" --base main --head "${FORK_OWNER}:${CONTRIB_BRANCH}" \
  --title "Beiträge aus ${FORK_OWNER}" --body "$body"
