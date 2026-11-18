"""Original CO5 policy demonstration; no third-party dependencies."""

def schedule(network, battery, urgent=False):
    if urgent:
        return "user-visible immediate action"
    if not network:
        return "queue for later"
    if battery < 20:
        return "defer"
    return "scheduled batch"


def video_quality(kbps):
    if kbps < 600:
        return "low quality"
    if kbps < 2500:
        return "medium quality"
    return "high quality"


def main():
    for case in [(False, 80, False), (True, 10, False), (True, 75, False)]:
        print("background task", case, "->", schedule(*case))
    for bandwidth in [300, 1200, 5000]:
        print(f"bandwidth={bandwidth} kbps -> {video_quality(bandwidth)}")


if __name__ == "__main__":
    main()
