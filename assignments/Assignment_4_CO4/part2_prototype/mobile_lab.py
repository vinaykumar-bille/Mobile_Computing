"""Original standard-library policy models for Mobile Computing CO4.

All numbers in this script are illustrative simulations, NOT phone measurements.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceContext:
    online: bool
    battery_percent: int
    charging: bool
    foreground: bool
    maintenance_window: bool = False

    def __post_init__(self):
        if not 0 <= self.battery_percent <= 100:
            raise ValueError("battery_percent must be between 0 and 100")


def allow_sync(context: DeviceContext, *, urgent: bool = False) -> bool:
    """Illustrative app-level sync policy; OS scheduling may still defer work."""
    if not context.online:
        return False
    if urgent and context.foreground:
        return True
    if context.battery_percent < 20 and not context.charging:
        return False
    return context.foreground or context.maintenance_window


class Inbox:
    """Minimal in-memory demonstration of duplicate-safe message processing."""

    def __init__(self):
        self._seen = set()

    def receive(self, message_id: str) -> bool:
        if not message_id or not message_id.strip():
            raise ValueError("A nonempty message ID is required")
        if message_id in self._seen:
            return False
        self._seen.add(message_id)
        return True

    @property
    def unique_count(self) -> int:
        return len(self._seen)


def startup_model(*, cold: bool) -> dict[str, int]:
    """Return fictional component durations in ms; no device measurement."""
    phases = {
        "process_setup": 95 if cold else 0,
        "runtime_init": 110 if cold else 15,
        "app_init": 70 if cold else 20,
        "first_frame": 55,
    }
    phases["total"] = sum(phases.values())
    return phases


def permission_decision(*, granted: bool, user_denied: bool) -> bool:
    """Deny-by-default; denied permission cannot be bypassed."""
    return granted and not user_denied


def main() -> None:
    scenarios = [
        ("Online foreground", DeviceContext(True, 65, False, True)),
        ("Low battery", DeviceContext(True, 12, False, False, True)),
        ("Charging + idle window", DeviceContext(True, 12, True, False, True)),
        ("No network", DeviceContext(False, 80, True, True)),
        ("Background deferred", DeviceContext(True, 80, False, False)),
    ]
    print("SIMULATED sync decisions (not Android scheduling evidence)")
    for name, context in scenarios:
        print(f"  {name:28s} -> {'ALLOW' if allow_sync(context) else 'DEFER'}")
    inbox = Inbox()
    print("\nSIMULATED message deduplication")
    for message in ("A", "B", "A", "C", "B"):
        print(f"  {message} -> {'NEW' if inbox.receive(message) else 'DUPLICATE'}")
    print(f"Unique messages: {inbox.unique_count}")
    print("\nFICTIONAL startup model (milliseconds)")
    print("Cold:", startup_model(cold=True))
    print("Warm:", startup_model(cold=False))
    print("\nSIMULATED permission denial:", permission_decision(granted=True, user_denied=True))


if __name__ == "__main__":
    main()
