"""Original CO5 deterministic educational experiments, not Android measurements."""
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Work:
    work_id: str
    permission: bool
    encrypted: bool
    sensitive: bool
    critical: bool = False


@dataclass(frozen=True)
class Environment:
    online: bool
    battery: int
    charging: bool = False


def decide(work: Work, env: Environment) -> str:
    """Privacy constraints precede scheduling choices."""
    if not work.permission:
        return "REJECT_PERMISSION"
    if work.sensitive and not work.encrypted:
        return "REJECT_ENCRYPTION"
    if not env.online:
        return "DEFER_OFFLINE"
    if env.battery < 20 and not env.charging and not work.critical:
        return "DEFER_BATTERY"
    return "SCHEDULE"


def rank_items(items: list[tuple[str, float]], cap: int | None = None) -> tuple[list[str], int]:
    """Toy ranking cost model: scores inspected, not CPU milliseconds."""
    if cap is not None and cap < 1:
        raise ValueError("cap must be >= 1")
    candidate = items if cap is None else items[:cap]
    return [key for key, _ in sorted(candidate, key=lambda entry: (-entry[1], entry[0]))], len(candidate)


def choose_media_kbps(estimated_bandwidth_kbps: int) -> int:
    if estimated_bandwidth_kbps < 0:
        raise ValueError("invalid bandwidth")
    if estimated_bandwidth_kbps < 600:
        return 240
    if estimated_bandwidth_kbps < 2500:
        return 720
    return 1800


def run():
    cases = [
        ("normal", Work("w1", True, True, True), Environment(True, 60)),
        ("offline", Work("w2", True, True, True), Environment(False, 60)),
        ("low_battery", Work("w3", True, True, True), Environment(True, 10)),
        ("no_permission", Work("w4", False, True, True), Environment(True, 60)),
        ("plaintext", Work("w5", True, False, True), Environment(True, 60)),
    ]
    decisions = [{"case": name, "decision": decide(job, state)} for name, job, state in cases]
    items = [(f"item-{i}", (i * 17 % 101) / 100) for i in range(50)]
    exact, exact_scans = rank_items(items)
    approximate, approx_scans = rank_items(items, 12)
    result = {
        "notice": "SIMULATED policy results, not Android device measurements",
        "decisions": decisions,
        "ranking": {"exact_items_scored": exact_scans, "approx_items_scored": approx_scans,
                    "exact_top3": exact[:3], "approx_top3": approximate[:3]},
        "media": [{"estimated_bandwidth_kbps": v, "selected_bitrate_kbps": choose_media_kbps(v)}
                  for v in (300, 1200, 5000)],
    }
    out = Path(__file__).parent / "results"
    out.mkdir(exist_ok=True)
    with (out / "model_results.json").open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
    print("Saved SIMULATED results:", out / "model_results.json")


if __name__ == "__main__":
    run()
