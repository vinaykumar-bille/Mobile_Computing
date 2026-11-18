"""Deterministic decision policy for synthetic RuralReach scenarios.

This is not Android OS battery control and does not measure real energy usage.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Context:
    battery: int
    network: str   # wifi, lte, offline
    moving: bool = False
    charging: bool = False
    hot: bool = False
    emergency: bool = False
    battery_saver: bool = False

    def __post_init__(self):
        if not 0 <= self.battery <= 100:
            raise ValueError("battery must be between 0 and 100")
        if self.network not in {"wifi", "lte", "offline"}:
            raise ValueError("network must be wifi, lte or offline")


@dataclass(frozen=True)
class Decision:
    seconds: int
    upload: str
    reason: str


def decide(ctx: Context) -> Decision:
    """Explicit priority order: emergency, thermal, critical, offline, charging, normal."""
    if ctx.emergency:
        return Decision(5, "urgent" if ctx.network != "offline" else "queue",
                        "Emergency priority, constrained by connectivity")
    if ctx.hot:
        return Decision(90, "defer" if ctx.network != "offline" else "queue",
                        "Reduce heat and background traffic")
    if ctx.battery_saver or (ctx.battery <= 15 and not ctx.charging):
        return Decision(180, "queue", "Battery reserve")
    if ctx.network == "offline":
        return Decision(30 if ctx.moving else 120, "queue", "No network")
    if ctx.charging and ctx.network == "wifi":
        return Decision(10, "batch", "Charging and Wi-Fi")
    if ctx.battery <= 25 and not ctx.moving:
        return Decision(120, "defer", "Low battery and stationary")
    if ctx.moving:
        return Decision(15, "batch", "Moving on available network")
    return Decision(60, "batch", "Normal periodic sampling")
