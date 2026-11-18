"""Original educational CO3 demonstrations; standard library only."""
from collections import deque


def handoff():
    print("HANDOFF: hysteresis threshold = 4 dB")
    serving = "AP-A"
    for time, a, b in [(0, -52, -74), (1, -61, -66), (2, -70, -62), (3, -73, -59)]:
        signals = {"AP-A": a, "AP-B": b}
        candidate = max(signals, key=signals.get)
        if candidate != serving and signals[candidate] >= signals[serving] + 4:
            serving = candidate
        print(f"t={time}s AP-A={a} AP-B={b} serving={serving}")


def mobile_ip():
    home_address = "10.0.0.8"
    home_agent = {}
    for network, care_of in [("home", None), ("visited-1", "172.16.1.8"), ("visited-2", "172.16.2.8")]:
        if care_of is None:
            home_agent.pop(home_address, None)
        else:
            home_agent[home_address] = care_of
        print(f"network={network} home={home_address} binding={home_agent.get(home_address, 'local delivery')}")


def shortest_hops(graph, source, destination):
    queue = deque([(source, [source])])
    visited = {source}
    while queue:
        node, path = queue.popleft()
        if node == destination:
            return path
        for neighbor in sorted(graph.get(node, [])):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None


def routing():
    topology = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D"], "D": ["B", "C", "E"], "E": ["D"]}
    print("DSDV simplified table: A to E, hop count", len(shortest_hops(topology, "A", "E")) - 1)
    print("AODV simplified discovery: A to E", " -> ".join(shortest_hops(topology, "A", "E")))
    topology["D"].remove("E")
    topology["E"].remove("D")
    print("AODV after link break:", shortest_hops(topology, "A", "E"))


if __name__ == "__main__":
    handoff()
    mobile_ip()
    routing()
