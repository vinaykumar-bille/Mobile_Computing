# Part II – Reproducible Mobile Computing Prototype

**Student:** Vinay Kumar (192373042)

## Aim
To create and test a small **logic-level simulation** of mobile background synchronization, duplicate message handling, startup cost and permission checks.

## Tools
Python 3.10+ with standard library only. Run in Windows PowerShell:

```powershell
cd assignments/Assignment_4_CO4
python part2_prototype/mobile_lab.py
python -m unittest discover -s part2_prototype -p "test_*.py" -v
```

## Experiment 1: Sync decision policy
The function `allow_sync` returns false for offline operation or a battery below 20% unless the phone is charging. It also defers non-urgent background work unless the simulated maintenance window is available.

**Metrics:** Cases allowed, cases deferred, coverage across network/battery/foreground combinations.

## Experiment 2: Idempotent delivery
The `Inbox` model records a message ID at most once and reports whether a new ID was stored.

**Scenario:** Message IDs A, B, A, C, B. Unique count should be 3, regardless of duplicate arrivals.

## Experiment 3: Startup timing model
A configurable deterministic model sums process, runtime, application initialization and rendering costs. A warm launch skips some cold setup. These input durations are **illustrative constants**, not real ART profiling samples.

## Experiment 4: Permission audit
The `permission_decision` helper denies actions for an absent or explicitly denied permission; no permission grant is inferred from requesting it.

## Procedure and evidence
1. Execute the script and save its console table.
2. Run unit tests; preserve the test command output.
3. Explain inputs, expected outputs, edge cases and model assumptions.
4. For real Android claims, collect logs/screenshots using [the Android evidence guide](../evidence/android_evidence.md).
5. Label every output as either **simulated** or **measured on a device/emulator**.

## Limitations
No Android SDK, Binder, ART, radio, physical battery, background quota or kernel API is invoked in these Python models. They cannot verify Doze, OS enforcement, scheduling times, hardware energy usage or iOS behaviors. Device validation remains a separate step.
