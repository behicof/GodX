#!/usr/bin/env python3
"""Verify that vendor repositories match the commits in repos.lock."""
import subprocess
import sys
from pathlib import Path


def verify(lockfile: Path, vendor_dir: Path) -> None:
    ok = True
    for line in lockfile.read_text().splitlines():
        if not line.strip():
            continue
        name, expected = line.split()
        repo = vendor_dir / name
        git_dir = repo / ".git"
        if not git_dir.exists():
            print(f"missing repo: {repo}")
            ok = False
            continue
        result = subprocess.run([
            "git",
            "-C",
            str(repo),
            "rev-parse",
            "HEAD",
        ], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"failed to read sha for {name}")
            ok = False
            continue
        sha = result.stdout.strip()
        if sha != expected:
            print(f"mismatch for {name}: {sha} != {expected}")
            ok = False
    if not ok:
        sys.exit(1)
    print("[OK] vendor matches repos.lock")


def main() -> None:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} repos.lock vendor_dir")
        sys.exit(1)
    lockfile = Path(sys.argv[1])
    vendor_dir = Path(sys.argv[2])
    verify(lockfile, vendor_dir)


if __name__ == "__main__":
    main()
