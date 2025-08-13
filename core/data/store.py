"""Data storage stubs for Redis and PostgreSQL."""

from __future__ import annotations

from typing import Dict, Any


class Store:
    """In-memory placeholder store."""

    def __init__(self):
        self.records: list[Dict[str, Any]] = []

    def write(self, record: Dict[str, Any]) -> None:
        self.records.append(record)

    def all(self) -> list[Dict[str, Any]]:
        return list(self.records)
