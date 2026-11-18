"""Original CO3 educational routing simulations; no physical network measurements."""
from collections import deque
import csv
from pathlib import Path


def choose_access_point(current: str, dbm: dict[str, int], hysteresis_db: int = 5) -> str:
    """Switch only when an alternative is sufficiently stronger than current."""
    if current not in dbm or hysteresis_db < 0:
        raise ValueError("invalid current AP or hysteresis")
    best = max(dbm, key=dbm.get)
    return best if dbm[best] >= dbm[current] + hysteresis_db and best != current else current


def shortest_hop_path(graph: dict[str, list[str]], start: str, target: str) -> list[str] | None:
    """On-demand BFS illustration, NOT full AODV."""
    if start not in graph or target not in graph:
        return None
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        node, path = queue.popleft()
        if node == target:
            return path
        for nxt in graph[node]:
            if nxt in graph and nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))
    return None


def update_home_binding(bindings: dict[str, tuple[str, int]], home: str, coa: str, seq: int) -> bool:
    """Reject stale updates to a toy mobility binding table."""
    previous = bindings.get(home)
    if seq < 0 or not home or not coa:
        raise ValueError("bad binding")
    if previous and seq <= previous[1]:
        return False
    bindings[home] = (coa, seq)
    return True


def sample_trace() -> list[dict[str, object]]:
    readings = [
        {"step": 0, "AP1": -48, "AP2": -82},
        {"step": 1, "AP1": -56, "AP2": -73},
        {"step": 2, "AP1": -64, "AP2": -65},
        {"step": 3, "AP1": -74, "AP2": -56},
        {"step": 4, "AP1": -81, "AP2": -49},
    ]
    active = "AP1"
    result = []
    for reading in readings:
        active = choose_access_point(active, {"AP1": reading["AP1"], "AP2": reading["AP2"]})
        result.append({**reading, "selected_ap": active})
    return result


def main():
    trace = sample_trace()
    out = Path(__file__).parent / "results"
    out.mkdir(exist_ok=True)
    with (out / "handoff_simulated.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["step", "AP1", "AP2", "selected_ap"])
        writer.writeheader()
        writer.writerows(trace)
    graph = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D"], "D": ["B", "C", "E"], "E": ["D"]}
    print("SIMULATED CO3 handoff trace (dBm values invented for teaching)")
    for record in trace:
        print(record)
    print("ON-DEMAND shortest-hop path:", shortest_hop_path(graph, "A", "E"))
    bindings = {}
    print("New Mobile IP registration:", update_home_binding(bindings, "10.0.0.5", "172.16.1.5", 1))
    print("Stale registration rejected:", not update_home_binding(bindings, "10.0.0.5", "172.16.2.5", 1))
    print("Saved model CSV:", out / "handoff_simulated.csv")


if __name__ == "__main__":
    main()
