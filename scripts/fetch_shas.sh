#!/usr/bin/env bash
set -euo pipefail

ORG="AI4Finance-Foundation"
REPOS=(
  FinRL
  FinRL-Meta
  ElegantRL
  FinRL-Trading
  FinRL_Crypto
  FinRL_Podracer
  FinRAG
  FinGPT
  FinRobot
)
LOCKFILE="repos.lock"
LOG="fetch_shas.log"

# truncate log and lockfile
: > "$LOG"
: > "$LOCKFILE"

for repo in "${REPOS[@]}"; do
  echo "[$(date -Is)] fetching $repo" | tee -a "$LOG"
  if sha=$(git ls-remote "https://github.com/$ORG/$repo.git" HEAD 2>>"$LOG" | awk '{print $1}'); then
    if [ -n "$sha" ]; then
      echo "$repo $sha" | tee -a "$LOCKFILE"
    else
      echo "Failed to parse SHA for $repo" | tee -a "$LOG"
    fi
  else
    echo "Failed to fetch $repo" | tee -a "$LOG"
  fi
  sleep 1
done

echo "[OK] wrote $LOCKFILE" | tee -a "$LOG"
