#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/AI4Finance-Foundation/FinRL.git"
DEST="vendor/FinRL"
TARBALL="https://codeload.github.com/AI4Finance-Foundation/FinRL/tar.gz/refs/heads/main"
LOG="clone_finrl.log"

mkdir -p vendor
echo "== $(date -Is) starting ==" | tee "$LOG"

ensure_git_lfs() {
  if ! git lfs version >/dev/null 2>&1; then
    echo "git lfs not found; attempting to install..." | tee -a "$LOG"
    if command -v apt-get >/dev/null 2>&1; then
      apt-get update >> "$LOG" 2>&1 && apt-get install -y git-lfs >> "$LOG" 2>&1
    else
      echo "apt-get not available; cannot install git-lfs." | tee -a "$LOG"
      return 1
    fi
  fi
}

fetch_lfs() {
  ensure_git_lfs || return 0
  git lfs install --local >> "$LOG" 2>&1 || return 0
  git lfs pull >> "$LOG" 2>&1 || true
}

try_https() {
  echo "[1] HTTPS clone..." | tee -a "$LOG"
  GIT_CURL_VERBOSE=1 git clone "$REPO_URL" "$DEST" 2>&1 | tee -a "$LOG"
  (cd "$DEST" && fetch_lfs)
}

try_https_shallow() {
  echo "[2] HTTPS shallow (--depth 1, --filter=blob:none)..." | tee -a "$LOG"
  git clone --depth 1 --filter=blob:none "$REPO_URL" "$DEST" 2>&1 | tee -a "$LOG"
  (cd "$DEST" && fetch_lfs)
}

try_ssh_443() {
  echo "[3] SSH over 443..." | tee -a "$LOG"
  mkdir -p ~/.ssh
  if ! grep -q "Host github.com" ~/.ssh/config 2>/dev/null; then
    cat >> ~/.ssh/config <<'CFG'
Host github.com
  HostName ssh.github.com
  Port 443
  User git
  StrictHostKeyChecking accept-new
CFG
  fi
  GIT_SSH_COMMAND="ssh -F ~/.ssh/config" git clone git@github.com:AI4Finance-Foundation/FinRL.git "$DEST" 2>&1 | tee -a "$LOG"
  (cd "$DEST" && fetch_lfs)
}

try_tarball() {
  echo "[4] Tarball fallback (no git auth required)..." | tee -a "$LOG"
  TMPDIR=$(mktemp -d)
  trap 'rm -rf "$TMPDIR"' RETURN
  curl -L "$TARBALL" -o "$TMPDIR/finrl.tgz" 2>&1 | tee -a "$LOG"
  tar -xzf "$TMPDIR/finrl.tgz" -C "$TMPDIR" 2>&1 | tee -a "$LOG"
  EXTRACTED=$(find "$TMPDIR" -maxdepth 1 -type d -name "FinRL-*")
  COMMIT_HASH=${EXTRACTED##*-}
  rm -rf "$DEST"
  mkdir -p "$DEST"
  (shopt -s dotglob; mv "$EXTRACTED"/* "$DEST"/)
  echo "Tarball extracted to $DEST" | tee -a "$LOG"
  (
    cd "$DEST"
    git init >/dev/null
    git remote add origin "$REPO_URL"
    git fetch origin "$COMMIT_HASH" >> "$LOG" 2>&1
    git reset --hard "$COMMIT_HASH" >> "$LOG" 2>&1
    fetch_lfs
  )
}

cleanup_failed_dest() { [ ! -d "$DEST" ] || rm -rf "$DEST"; }

cleanup_failed_dest; if try_https; then exit 0; fi
cleanup_failed_dest; if try_https_shallow; then exit 0; fi
cleanup_failed_dest; if try_ssh_443; then exit 0; fi
cleanup_failed_dest; try_tarball
