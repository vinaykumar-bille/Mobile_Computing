"""Illustrative policy choices, not measured energy consumption."""

def choose_policy(battery_percent, network_available, urgent):
    if urgent:
        return "foreground user-triggered request"
    if battery_percent < 20:
        return "defer nonessential sync"
    if not network_available:
        return "queue locally and wait for network"
    return "batch pending work with WorkManager"


def main():
    cases = [(80, True, False), (15, True, False), (65, False, False), (10, False, True)]
    for battery, network, urgent in cases:
        print(f"battery={battery}% network={network} urgent={urgent}: {choose_policy(battery, network, urgent)}")


if __name__ == "__main__":
    main()
