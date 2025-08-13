#!/usr/bin/env bash
set -euo pipefail

LOCKFILE=${1:-repos.lock}
ORG="AI4Finance-Foundation"
DEST="vendor"
LOG="clone_and_pin.log"

if [ ! -f "$LOCKFILE" ]; then
  echo "lockfile '$LOCKFILE' not found" >&2
  exit 1
fi

mkdir -p "$DEST"
: > "$LOG"

while read -r name sha; do
  [ -n "$name" ] || continue
  repo_url="https://github.com/$ORG/$name.git"
  target="$DEST/$name"
  echo "[$(date -Is)] cloning $name" | tee -a "$LOG"
  if [ -d "$target/.git" ]; then
    echo "repo exists, fetching updates" | tee -a "$LOG"
    git -C "$target" fetch origin >>"$LOG" 2>&1 || true
  else
    if ! git clone "$repo_url" "$target" >>"$LOG" 2>&1; then
      echo "clone failed for $name" | tee -a "$LOG"
      continue
    fi
  fi
  if git -C "$target" checkout "$sha" >>"$LOG" 2>&1; then
    echo "checked out $sha" | tee -a "$LOG"
  else
    echo "checkout failed for $name" | tee -a "$LOG"
  fi
done < "$LOCKFILE"

echo "[OK] clones pinned" | tee -a "$LOG"
