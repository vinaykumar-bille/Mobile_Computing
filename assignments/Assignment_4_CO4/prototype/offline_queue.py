"""Synthetic offline queue with JSON persistence and idempotency logic.

IMPORTANT: JSON here is plaintext. Store ONLY made-up record IDs. This module
is deliberately not suitable for production patient data, encryption or auth.
"""
from pathlib import Path
import json


class FakeServer:
    def __init__(self):
        self.records = {}

    def commit(self, record):
        uid = record["id"]
        if uid not in self.records:
            self.records[uid] = record.copy()
        return uid


class OfflineQueue:
    def __init__(self, path):
        self.path = Path(path)
        self.rows = {}
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.rows = {r["id"]: r for r in raw}

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(list(self.rows.values()), indent=2),
            encoding="utf-8",
        )

    def enqueue(self, uid, label):
        if not uid or not uid.isascii() or len(uid) > 64:
            raise ValueError("use an opaque short synthetic ID")
        if uid in self.rows:
            return False
        self.rows[uid] = {"id": uid, "label": label, "state": "pending"}
        self._save()
        return True

    def sync(self, server, connected, lose_ack_for=None):
        trace = []
        for uid, record in self.rows.items():
            if record["state"] == "synced":
                continue
            if not connected:
                trace.append((uid, "offline: retained"))
                continue
            server.commit({"id": uid, "label": record["label"]})
            if uid == lose_ack_for:
                trace.append((uid, "server committed; ACK lost; pending"))
                continue
            record["state"] = "synced"
            trace.append((uid, "ACK received; synced"))
        self._save()
        return trace
