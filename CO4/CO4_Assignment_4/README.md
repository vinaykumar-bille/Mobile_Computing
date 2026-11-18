# CO4: Mobile Application Development and Android System Design

**Course:** Mobile Computing## Aim
Design a lightweight Android application for a rural health appointment reminder system that works reliably with intermittent connectivity.

## Part 1: Architecture

```text
User Interface (Activity / Compose)
           |
ViewModel (UI state and validation)
           |
Repository (single data access interface)
       /         \\
 Room local DB   HTTPS remote API
       \\         /
        WorkManager sync
```

**Activity lifecycle:** onCreate initializes the interface; onStart makes it visible; onResume enables interaction; onPause suspends foreground work; onStop releases nonessential resources; onDestroy cleans up. Save transient UI state in SavedStateHandle or rememberSaveable where appropriate.

**Offline-first design:** write user requests to a local queue; assign a unique request ID; display pending status; synchronize when a network connection is available; handle server conflicts and retries with idempotency keys. Never claim a request is confirmed before the server acknowledges it.

**Security:** use TLS; store tokens in Android Keystore-backed storage; validate all server input; request only necessary permissions; never include sensitive patient data in logs or notifications.

**Battery policy:** prefer WorkManager for deferrable work, use constraints for network availability, batch requests, and apply exponential backoff. Avoid unrestricted polling or persistent background services.

## Part 2: Prototype
Run `python battery_policy.py` for a policy simulation. This models a design decision, not Android OS scheduling behavior or measured battery usage.

## Verification checklist
1. Test fresh launch and rotation in Android Studio.
2. Turn on airplane mode and queue a request.
3. Restore network and verify exactly-once server handling.
4. Deny notification permission and confirm graceful degradation.
5. Capture your own emulator/device screenshots and logs.

## Result
The proposed architecture separates presentation, storage and synchronization, with explicit offline and security requirements. Real device tests remain to be completed.
