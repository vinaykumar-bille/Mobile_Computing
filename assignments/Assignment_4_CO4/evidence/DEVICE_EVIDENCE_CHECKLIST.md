# Android Studio and device evidence collection

**These are instructions; evidence is NOT yet collected.** Use your own test package and disposable emulator/device. Do not publish real patient data, passwords, account tokens or unredacted device identifiers.

## Test environment record (fill after running)
- Android version:
- Device/emulator model:
- RAM:
- App package and version:
- Date/time:
- Network/charging state:
- Android Studio version:
- Test input size:
- Trace/screenshot file names:

## Task 1 — Lifecycle
Run the demo app in foreground, background for five minutes, then a controlled emulator memory-pressure scenario. Save:
```bash
adb shell getprop ro.build.version.release
adb shell ps -A
adb shell dumpsys activity processes
adb shell dumpsys meminfo your.package.name
adb logcat -d -s ActivityManager ActivityTaskManager
```
Capture PID, PSS and your own lifecycle callback logs. Do not infer process death from the screen turning off.

## Task 2 — CPU and threads
Use Android Studio CPU Profiler or Perfetto. With identical input and warmup, record single-thread and bounded-worker runs: elapsed ms, CPU time, active thread count, frame delays, PSS and device thermal condition. Attach real exported traces/screenshots.

## Task 3 — Runtime
For a disposable app only, capture cold/warm startup, GC activity and compilation state. If commands are supported on that Android build:
```bash
adb shell dumpsys package your.package.name
adb shell cmd package compile -m verify -f your.package.name
adb shell cmd package compile -m speed-profile -f your.package.name
adb shell cmd package compile -m speed -f your.package.name
```
Record unsupported commands and version differences. Do not assert an ART speedup without repeated measurements.

## Task 4 — Security
Inspect `AndroidManifest.xml`, permissions, exported components and Network Security Config. Verify the app rejects plaintext endpoints and handles denied permissions. Use safe test fixtures only.

## Task 5 — Power
For fixed workloads with baseline and optimized versions:
```bash
adb shell dumpsys batterystats --reset
adb shell dumpsys batterystats
adb shell dumpsys deviceidle
adb shell dumpsys power
```
Track elapsed time, wakeups, job timing and radio/sensor activity. A percentage change by itself is not a calibrated energy measurement.

## Task 6 — Offline system
Disable network, save two synthetic visit IDs, re-enable network, interrupt after simulated server commit but before ACK, then retry. Screenshot actual UI pending/synced status and show server unique IDs. Do not claim that the Python JSON simulator is encrypted Android storage.

## Evidence directory naming
Use `evidence/actual/` for your own true artifacts, for example:
- `task1_lifecycle_log.txt`
- `task2_cpu_profile.png`
- `task3_art_gc.txt`
- `task4_manifest_review.md`
- `task5_batterystats.txt`
- `task6_offline_sync.png`

**Submission check:** Every screenshot must correspond to a real execution and be labelled with the tested device and date.
