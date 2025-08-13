#!/usr/bin/env bash
set -euo pipefail
ROOT="$(pwd)"
LOCK="${1:-$ROOT/repos.lock}"
DEST="$ROOT/vendor"; LOG="$ROOT/scripts/clone_and_pin.log"
mkdir -p "$DEST"; : > "$LOG"

retry() { # retry <attempts> <sleep> -- cmd...
  local n=$1 s=$2; shift 2
  for ((i=1;i<=n;i++)); do
    if "$@"; then return 0; fi
    sleep "$s"; s=$((s*2))
  done
  return 1
}

while read -r name sha; do
  [[ -z "$name" || -z "$sha" ]] && continue
  echo "== $name @ $sha ==" | tee -a "$LOG"
  dir="$DEST/$name"; rm -rf "$dir"

  # Offline mirror first
  if [[ -f "mirror/${name}.tar.gz" ]]; then
    echo "[mirror] using mirror/${name}.tar.gz" | tee -a "$LOG"
    mkdir -p "$dir"; tar -xzf "mirror/${name}.tar.gz" -C "$dir" --strip-components=1
  else
    url="https://github.com/AI4Finance-Foundation/${name}.git"
    echo "[git] cloning shallow…" | tee -a "$LOG"
    retry 3 1 git clone --depth 1 --filter=blob:none "$url" "$dir" 2>>"$LOG" || {
      echo "[FAIL] clone $name. If proxy blocks, drop a tarball to mirror/${name}.tar.gz" | tee -a "$LOG"; continue; }
    (
      cd "$dir"
      git fetch origin "$sha" --depth 1 2>>"$LOG" || true
      git checkout -q "$sha" || {
        echo "[WARN] SHA not in shallow, fetching full…" | tee -a "$LOG"
        git fetch --all --tags 2>>"$LOG"
        git checkout -q "$sha"
      }
    )
  fi

  # Verify
  got=$(git -C "$dir" rev-parse HEAD 2>/dev/null || echo "no-git")
  echo "[OK] $name → $got" | tee -a "$LOG"
done < "$LOCK"
