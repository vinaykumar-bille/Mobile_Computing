# Android Evidence Checklist

**Do not fabricate screenshots, profiler measurements or runtime logs.** Capture these on your own phone or emulator and record the model, Android version, time, app build and test conditions. Remove private data before uploading evidence.

## 1. Device and environment
```powershell
adb devices
adb shell getprop ro.build.version.release
adb shell getprop ro.product.model
```

## 2. Process and lifecycle
Install a **test application that you own**. Replace `com.example.myapp` with its actual package name:
```powershell
adb shell am force-stop com.example.myapp
adb shell am start -W -n com.example.myapp/.MainActivity
adb shell pidof com.example.myapp
adb logcat -d -s ActivityTaskManager ActivityManager
```
The actual launcher activity may differ from `.MainActivity`. Record the launch output and any relevant lifecycle logs. Repeat after a warm launch, specifying setup conditions.

## 3. Permission/security
Review the app manifest, package permissions and result of user denial:
```powershell
adb shell dumpsys package com.example.myapp
```
Capture the permission request and the app's behavior after denial. Never post tokens, private records or debug secrets.

## 4. Background and battery
Inspect power status and idle state **on the actual Android system**:
```powershell
adb shell dumpsys battery
adb shell dumpsys deviceidle
adb shell dumpsys jobscheduler
```
Device-idle forcing commands can change test state and are unsuitable for production devices. Consult official Android documentation and use a dedicated test device when experimenting.

## Suggested evidence filenames
- `01_environment.txt`
- `02_cold_launch.txt`
- `03_warm_launch.txt`
- `04_permission_denial.png`
- `05_battery_deviceidle.txt`
- `06_workmanager_execution.txt`

## Reporting
Create a table with **test objective, actual environment, command, observed output, interpretation, limitation**. Do not convert sample Python model durations into claimed physical measurements.
