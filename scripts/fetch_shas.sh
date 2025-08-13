#!/usr/bin/env bash
set -euo pipefail
ORG="${ORG:-AI4Finance-Foundation}"
GITHUB_BASE="${GITHUB_BASE:-https://api.github.com}"
REPOS=(FinRL FinRL-Meta ElegantRL FinRL-Trading FinRL_Crypto FinRL_Podracer FinRAG FinGPT FinRobot)
OUT="repos.lock"
LOG="scripts/fetch_shas.log"
: > "$LOG"

api() {  # $1 = repo
  if [[ -n "${GITHUB_TOKEN:-}" ]]; then
    curl -fsSL -H "Authorization: Bearer $GITHUB_TOKEN" "$GITHUB_BASE/repos/$ORG/$1/commits/HEAD"
  else
    curl -fsSL "$GITHUB_BASE/repos/$ORG/$1/commits/HEAD"
  fi
}

echo "== $(date -Is) fetch_shas ==" | tee -a "$LOG"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

for r in "${REPOS[@]}"; do
  echo -n "$r: " | tee -a "$LOG"
  if resp=$(api "$r" 2>>"$LOG"); then
    sha=$(awk -F'"' '/"sha":/{print $4; exit}' <<<"$resp")
    echo "$sha" | tee -a "$LOG"
    echo "$r $sha" >> "$TMP"
  else
    echo "FAILED" | tee -a "$LOG"
    echo "[WARN] network/api error. Keeping previous $OUT if exists." | tee -a "$LOG"
  fi
done

if [[ -s "$TMP" ]]; then
  mv "$TMP" "$OUT"
  echo "[OK] wrote $OUT" | tee -a "$LOG"
else
  echo "[SKIP] no data; $OUT unchanged (if existed)." | tee -a "$LOG"
fi
