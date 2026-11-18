# CO4: Evidence and validation checklist
**Design-only Part I:** Do not claim Android tooling was used to produce the Part I design. Any real-device checks below are supplemental practical investigation.

For a separate Android practical exercise, use a test app with no confidential patient data and capture:
1. Android version, device model, app build and timestamp.
2. Cold and warm activity launch with `adb shell am start -W -n PACKAGE/ACTIVITY`. Confirm the activity name first.
3. Runtime permission grant and denial, with screenshots showing correct app fallback.
4. Offline write to a local outbox followed by a network-restored sync and server ACK.
5. `adb shell dumpsys deviceidle` and `adb shell dumpsys jobscheduler` excerpts for context. Do not claim job timing from the Python policy simulator.

Windows PowerShell commands (replace package/activity):
```powershell
adb devices
adb shell getprop ro.build.version.release
adb shell am force-stop com.example.testapp
adb shell am start -W -n com.example.testapp/.MainActivity
adb shell dumpsys deviceidle
adb shell dumpsys jobscheduler
```

Redact personal data and device identifiers. Record when evidence was captured, and distinguish observed values from theoretical expectations.
