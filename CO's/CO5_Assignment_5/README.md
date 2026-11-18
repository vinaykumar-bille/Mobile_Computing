# CO5: Background Execution and Adaptive Mobile Services

**Student:** Vinay Kumar | **Register no.:** 192373042

## Aim
Compare background-task strategies and implement an adaptive feed selection model for constrained mobile devices.

## Part A: Design
- **Explicit intent:** launch a known component, such as an appointment details screen.
- **Implicit intent:** request an external action, such as opening a web URL, and verify a suitable handler exists.
- **WorkManager:** schedule persistent, deferrable synchronization with network constraints and retry/backoff.
- **Foreground service:** reserve for genuinely user-visible ongoing tasks, respecting Android's current platform restrictions.
- **Push messaging:** process incoming notifications with minimal background work; avoid treating delivery as guaranteed or immediate.
- **Adaptive media:** reduce media resolution on constrained links; avoid automatic playback on metered or low-bandwidth connections.

## Part B: Simulation
Run `python adaptive_service.py` to compare deterministic scheduling choices and media quality. These are policy outputs, not measured network or battery performance.

## Test cases
| Scenario | Expected policy |
|---|---|
| No network | queue for later |
| Low battery, nonurgent | defer |
| Connected, normal battery | scheduled batch |
| 300 kbps bandwidth | low quality |
| 5000 kbps bandwidth | high quality |

## Evidence to collect
Android Studio project, emulator screenshots, Logcat excerpts, network toggling tests, battery constraints, and actual measured observations. Do not submit simulated results as device measurements.
