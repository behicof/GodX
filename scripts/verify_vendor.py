#!/usr/bin/env python3
import subprocess, sys, pathlib

lock = pathlib.Path('repos.lock')
vendor_dir = pathlib.Path('vendor')

if not lock.exists():
    print('repos.lock missing', file=sys.stderr)
    sys.exit(1)

mismatches = []
for line in lock.read_text().splitlines():
    if not line.strip() or line.strip().startswith('#'):
        continue
    path, expected = line.strip().split()
    repo = vendor_dir / path
    if not repo.exists():
        mismatches.append(f'{path} missing')
        continue
    result = subprocess.run(['git', '-C', str(repo), 'rev-parse', 'HEAD'], capture_output=True, text=True)
    if result.returncode != 0:
        mismatches.append(f'{path} not a git repo')
    elif result.stdout.strip() != expected:
        mismatches.append(f'{path} expected {expected} got {result.stdout.strip()}')

if mismatches:
    print('vendor verification failed:')
    for m in mismatches:
        print(' -', m)
    sys.exit(1)
else:
    print('vendor verified')
