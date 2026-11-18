"""Run original synthetic demonstrations. Python 3.10+ standard library only."""
import csv
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from policy import Context, decide
from offline_queue import FakeServer, OfflineQueue
from audit import audit, verdict

OUT = HERE.parent / "results"


def write_csv(name, headings, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8", newline="") as stream:
        w = csv.writer(stream)
        w.writerow(headings)
        w.writerows(rows)


def main():
    scenarios = [
        ("charging_wifi", Context(65, "wifi", charging=True)),
        ("moving_lte_80", Context(80, "lte", moving=True)),
        ("stationary_lte_20", Context(20, "lte")),
        ("battery_saver_12", Context(12, "lte", battery_saver=True)),
        ("offline_moving", Context(50, "offline", moving=True)),
        ("hot_device", Context(50, "lte", hot=True)),
        ("emergency", Context(40, "lte", emergency=True)),
    ]
    rows = [(name, c.battery, c.network, c.moving, d.seconds, d.upload, d.reason)
            for name, c in scenarios for d in [decide(c)]]
    write_csv("policy_decisions.csv",
              ["scenario", "battery_percent", "network", "moving",
               "sample_seconds", "upload_action", "reason"], rows)
    with tempfile.TemporaryDirectory() as tmp:
        queue = OfflineQueue(Path(tmp) / "demo_records.json")
        server = FakeServer()
        queue.enqueue("VISIT-A", "synthetic example A")
        queue.enqueue("VISIT-B", "synthetic example B")
        trace = [("phase_1", *x) for x in queue.sync(server, False)]
        trace += [("phase_2", *x) for x in queue.sync(server, True, lose_ack_for="VISIT-A")]
        trace += [("phase_3", *x) for x in queue.sync(server, True)]
        if len(server.records) != 2 or any(r["state"] != "synced" for r in queue.rows.values()):
            raise AssertionError("idempotency demonstration failed")
    write_csv("sync_trace.csv", ["phase", "record_id", "event"], trace)
    insecure = audit(dict(https_only=False, private_token_storage=False,
                          signed_updates=False, permission_on_demand=False,
                          internal_components_exported=True))
    hardened = audit(dict(https_only=True, private_token_storage=True,
                          signed_updates=True, permission_on_demand=True,
                          internal_components_exported=False))
    print("SIMULATION ONLY: no device measurements or encryption have occurred")
    for row in rows:
        print(f"{row[0]}: every {row[4]} s; action={row[5]}")
    print("Insecure configuration:", verdict(insecure))
    print("Improved design flags:", verdict(hardened))
    print("Unique server records after lost ACK/retry: 2")
    print("Generated:", OUT / "policy_decisions.csv", "and", OUT / "sync_trace.csv")


if __name__ == "__main__":
    main()
