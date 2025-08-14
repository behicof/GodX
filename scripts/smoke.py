#!/usr/bin/env python3
"""Basic smoke test to ensure key modules import."""
import importlib
import sys
from pathlib import Path

# ensure repository root is on PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parents[1]))

MODULES = ["core", "orchestrator"]

for mod in MODULES:
    importlib.import_module(mod)
print("[OK] smoke imports passed")
