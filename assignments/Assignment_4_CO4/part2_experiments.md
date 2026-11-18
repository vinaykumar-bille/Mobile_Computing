# PART II — Engineering Experiments and Verification

**Student:** Vinay Kumar (192373042)  
**Scope:** Reproducible Python *logic-model* testing with an explicit plan for authentic Android device instrumentation.

## Evidence rules
The provided code cannot measure ART, kernel thread placement, GC pauses, real app process death, Doze transitions, device encryption or battery discharge. An output labelled “simulated” validates only the model's decisions. Actual ADB/Android Studio commands must be run by the student, with captured files and device specifications. Do not invent screenshots.

## Task 1 — Process and lifecycle test (8 marks)

**Prediction before test:** A foreground Android app normally remains running; a cached app *may* be reclaimed after backgrounding or memory pressure. `onDestroy()` is not a reliable final callback when the OS kills the process.

**Device procedure:** Use a disposable sample Android app with `onCreate`, `onStart`, `onResume`, `onPause`, `onStop` logs and a form whose draft is persisted in saved state/local storage. Record PID, memory PSS and callbacks while foregrounded, after five minutes backgrounded, and after controlled emulator memory pressure.

**Measurements to capture:** `adb shell ps -A`, `adb shell dumpsys activity processes`, `adb shell dumpsys meminfo your.package`, `adb logcat -d -s ActivityTaskManager ActivityManager`. Capture before/after process IDs and form restoration. Device state determines outcomes; if process was not killed, record that as the actual result rather than claiming success by prediction.

**Failure interpretation:** A process restart is not a data-loss bug if drafts were durably saved. An in-memory-only form is a counterexample.

## Task 2 — Threads and responsiveness (9 marks)

**Hypothesis:** Moving CPU work off the UI thread improves frame responsiveness, but adding threads to tiny or lock-contended work may increase total elapsed time. Test single-worker vs four-worker execution with fixed inputs.

**Real test:** On Android instrument a CPU-bound calculation in (a) the main thread (brief controlled test only), (b) one background executor and (c) a bounded pool. Use Android Studio CPU profiler/Perfetto to capture elapsed duration, CPU utilization, thread count and missed frames. Stop before an app-not-responding dialog or thermal overload. In Python, the policy runner is not a CPU profiler; concurrency claims must be based on device traces.

**Counterexample:** For a small input, dispatch and synchronization overhead can exceed useful processing, so a pool can be slower. Repeat runs and report median/spread rather than selecting the fastest one.

## Task 3 — Runtime, compilation and garbage collection (10 marks)

**Prediction:** Cold startup generally incurs initialization absent in a warm resume; compilation profile may change hot-method performance, but improvements depend on device, app, code and Android release.

**Device procedure:** On a test-only package, collect cold and warm startup timings using suitable Android Studio tooling; note package and OS version. If supported, capture `adb shell cmd package compile -m verify -f your.package`, `-m speed-profile` and `-m speed` in separate controlled trials. Read real GC events from Logcat/profiler. Installation state and compilation filters must be reset or documented between experiments.

**Bounded negative test:** Retain a small reference temporarily in a disposable test build, inspect heap growth, then remove it and compare. Do not deliberately exhaust memory or crash other apps.

**Data sheet:** compilation mode | start type | 5 runs | median ms | peak PSS | GC count/pause | notes. No values are pre-filled because none were measured.

## Task 4 — Threat assessment and regression (7 marks)

**Hypothesis:** Changing a component to exported without validation introduces a reachable entry point; encrypted storage cannot repair an HTTP network leak.

**Simulated experiment:** `prototype/audit.py` classifies deliberately insecure and safer configuration examples. This is configuration reasoning only: it cannot prove runtime enforcement or actual Keystore use.

**Real validation:** Review manifest, `android:exported` and permissions; inspect Network Security Config; use test accounts and non-sensitive data to validate HTTPS enforcement and exported entry point handling in an emulator. Confirm that permission denial does not crash normal capture. Never attack a third-party package/network.

**Expected report:** asset | attempted action | predicted outcome | observed log/screenshot | residual risk.

## Task 5 — Energy and background scheduling (7 marks)

**Hypothesis:** Adaptive sampling and batch uploads reduce *modelled wakeups*, but not necessarily measured battery percentage in every workload. Higher sampling rates or frequent exact alarms may offset Doze-related savings.

**Simulated experiment:** Run the policy scenarios in `prototype/run_all.py`. Compare 10 s vs 120 s intervals: in one hour, periodic attempts occur 360 vs 30 times, respectively (idealized count; excludes OS restrictions and workload effects). That arithmetic does **not** equal measured mAh.

**Real validation:** Use a fixed Android test build and workload duration; capture `dumpsys batterystats`, `dumpsys deviceidle`, screen state, GPS usage, network sends and wakelocks. Repeat with and without batching, documenting charging state, temperature and signal strength. Include measurement uncertainty.

**Conflict:** A held wakelock defeats idle savings; release it and use OS-managed deferrable work.

## Task 6 — Battery-aware secure field app (9 marks)

### Decision model
Input: battery %, charging, Wi-Fi/LTE/offline, moving/stationary, hot/normal, emergency flag and pending-record count. Output: sampling seconds, upload action and reason. This model is transparent and testable, *not* an Android battery management implementation.

| Scenario | Expected interval | Expected upload |
|---|---:|---|
| Charging on Wi-Fi | 10 s | batch |
| 80% moving on LTE | 15 s | batch |
| 20% stationary on LTE | 120 s | defer |
| 12% battery saver | 180 s | queue |
| Offline while moving | 30 s | queue |
| Device hot | 90 s | defer |
| Emergency | 5 s | urgent |

### Offline idempotency exercise
Queue records with opaque IDs `VISIT-A` and `VISIT-B`. Deliberately simulate: (1) offline upload attempts, (2) server commit with lost acknowledgement, and (3) retry. Expected result: pending items are not claimed uploaded offline, and duplicate transmissions of the same UUID do not create duplicate server rows. The example queue persists to a local JSON file, which is **plaintext and contains only synthetic demo IDs**. A production replacement must use an encrypted transactional database, verified key management and authenticated TLS.

### Acceptance criteria
1. All model decisions match the table.
2. Duplicate message IDs never create two server rows.
3. A lost ACK leaves a pending item for later retry.
4. Actual Android screenshots are supplied separately before claiming device performance.
5. No real patient data, access tokens or device identifiers appear in submitted files.

### Evaluation of a change request
If 5,000 workers need emergency updates in seconds, the ordinary scheduled batch path is insufficient. Design priority ingestion, push, retry/ack monitoring, network failure escalation, load tests and battery guardrails. The requirement cannot be guaranteed by a local interval rule alone.

### Reproducible commands
```powershell
python -m unittest discover -s tests -v
python prototype/run_all.py
```

The unit tests cover branch logic and idempotency, not actual Android behavior.

## Final reflective assessment
The strongest design lesson is that reliability, privacy and energy efficiency pull in different directions. On a rural field shift, buffering data saves network energy and tolerates outages, but a lost offline device can lose unsynced data permanently. Encryption protects confidentiality without magically providing backup. Similarly, a notification can be delivered by the OS after app termination, but that does not guarantee that arbitrary app code runs immediately. Engineering reports should separate predictions, deterministic simulations and real observations so that every claim is testable.
