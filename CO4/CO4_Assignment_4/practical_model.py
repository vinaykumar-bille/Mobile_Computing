"""Supplemental CO4 policy model; not a real Android runtime measurement."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Context:
    network: bool
    battery: int
    charging: bool
    foreground: bool

    def __post_init__(self):
        if not 0 <= self.battery <= 100:
            raise ValueError("Battery percentage outside 0–100")


def sync_decision(ctx: Context, data_is_encrypted: bool, permission: bool) -> str:
    if not permission:
        return "REJECT: no permission"
    if not data_is_encrypted:
        return "REJECT: sensitive data unencrypted"
    if not ctx.network:
        return "DEFER: offline"
    if ctx.battery < 20 and not ctx.charging:
        return "DEFER: low battery"
    if not ctx.foreground:
        return "SCHEDULE: OS-managed worker"
    return "RUN: foreground sync"


def model_startup(cold: bool) -> int:
    """Fictional time in ms for comparing launch components, NOT profiling."""
    return (120 if cold else 0) + (110 if cold else 20) + 70


if __name__ == "__main__":
    for case in [
        Context(False, 70, False, True),
        Context(True, 8, False, False),
        Context(True, 80, False, False),
        Context(True, 80, False, True),
    ]:
        print("SIMULATION:", case, sync_decision(case, True, True))
    print("ILLUSTRATIVE cold/warm startup ms:", model_startup(True), model_startup(False))
