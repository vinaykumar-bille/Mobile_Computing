# PART I — Architectural Analysis and Structured Design

**Student:** Vinay Kumar | **Register number:** 192373042  
**Case study:** RuralReach, an offline-first mobile field-visit tool

> This part is a design exercise. All flows and predictions below are reasoned examples, not measurements from an IDE, emulator or device.

## Task 1 — Repair an incomplete mobile operating-system architecture (6 marks)

### Problem diagnosis
Calling an OS merely “applications running above a kernel” hides essential boundaries. A useful architecture must reveal where a hardware request is translated, where application code executes, where permissions are checked and how background work is controlled. Seven missing items are: (1) a device-independent hardware abstraction layer, (2) system services, (3) native libraries, (4) a named runtime and its memory model, (5) process isolation and IPC, (6) explicit security enforcement points, and (7) a power policy.

### Corrected Android architecture

| Layer, top to bottom | Specific responsibility | Interface or dependency |
|---|---|---|
| RuralReach and other apps | Screens, user actions, background jobs and local record logic | Public Android framework APIs |
| Android framework/system services | Activity lifecycle, notifications, permissions, location, job scheduling | Binder IPC, native services |
| Android Runtime (ART) | Execute verified DEX via interpretation/JIT/AOT; managed garbage collection | Linux processes and native support |
| Native components | SQLite, graphics, TLS/crypto, media and Bionic | HAL and kernel facilities |
| Hardware abstraction layer (HAL) | Stable vendor interfaces for sensors, radios, camera and audio | Kernel drivers or vendor services |
| Linux kernel | Scheduling, memory, processes, filesystems, network stack, drivers and SELinux hooks | Hardware |
| Hardware | CPU, RAM, storage, GPS, modem, display, battery | Electrical/physical functions |

The layers are a conceptual model: system services are not strictly “beneath” ART because some services use managed code and others use native code. A location request, for example, goes from an application API through privileged system service checks and hardware abstractions to location hardware. Process sandboxing uses per-app UIDs and SELinux; dangerous permission decisions are made and enforced at framework/service boundaries. Power policy spans application scheduling, framework restrictions and kernel idle/suspend capabilities.

### Defended design decision
The revised diagram is actionable: if the GPS feature fails, the developer can separately inspect app permission state, location service configuration, vendor HAL and driver availability. If an offline upload is delayed, WorkManager constraints and Doze are inspected before blaming the kernel. Each layer now has an observable responsibility instead of a vague promise.

## Task 2 — Choose a platform for reliable background messaging (8 marks)

### Formal requirement
A worker must receive an urgent visit update even when the app has not been visible recently. Success means that a *system-delivered notification* can alert the worker and the authoritative server retains the message until acknowledged. It does **not** mean unrestricted background execution or guaranteed delivery within seconds.

**Hypothesis:** Background execution policy, rather than raw CPU speed, is the strongest differentiator for notification reliability.

| Attribute | Android | iOS | Windows packaged applications |
|---|---|---|---|
| Kernel | Linux | XNU | Windows NT |
| Application code | ART/DEX plus native | Native Swift/Objective-C runtime, signed binaries | Native or managed, depending on application model |
| Isolation | App UID, sandbox, SELinux and permission checks | Sandbox, entitlements and code signing | AppContainer/capabilities for packaged apps |
| Typical IPC | Binder and intents | XPC and Mach-backed facilities | COM/RPC and app services |
| Push integration | FCM/vendor push plus OS notification system | APNs and notification system | WNS for supported app models |
| Background constraints | Doze, standby buckets, process importance, job limits | Suspended processes and restricted background tasks | App-model-dependent background execution policy |

### Message journey
**Android:** server stores message with UUID → push transport signals device → OS decides notification visibility → worker taps notification → app process starts or resumes → ART executes handler → app authenticates and downloads content → server records acknowledgement.

**iOS:** server stores message → APNs delivers notification to OS → OS can show it without app code executing → tap or permitted wake launches application → native handler fetches content → server records acknowledgement.

**Windows:** WNS notification and the packaged app's declared background capabilities determine allowed actions; desktop Windows applications follow a different process model and cannot be assumed to share mobile restrictions.

### Stress case
Suppose the app is killed under memory pressure. The push service can still deliver a visible notification subject to device connectivity and user settings, but silent handlers may not execute. The robust design therefore uses server retention, message UUIDs, acknowledgements and a later authenticated fetch. It avoids storing sensitive clinical text in notification payloads. A user with notifications disabled may have to open the app to receive the update; alerts are not a substitute for a safety-critical channel.

### Platform choice
Use native Android and iOS clients with a shared server protocol. Both support OS push, but background behavior must be designed independently. Windows should be a separate supported client only when field-device requirements justify it.

## Task 3 — Explain mobile runtime startup and low-memory behavior (9 marks)

Android packages may contain DEX. ART verifies and loads methods, may interpret or JIT-compile them, and may use ahead-of-time compiled artifacts guided by profiles. An app process is normally forked from Zygote when needed. Its runtime creates the Application object and Activity lifecycle callbacks before the first frame is rendered. Native libraries are loaded through the dynamic linker as required.

iOS applications typically ship signed native executable images loaded by dyld; Swift and Objective-C runtime facilities provide object behavior, while ARC automates reference-count changes. Windows may run native PE binaries or managed .NET code, depending on the app technology; the “Windows Runtime” is not identical to a universal managed-language virtual machine.

| Question | Android ART | Apple native runtime | Windows native/.NET |
|---|---|---|---|
| Initial code | DEX/native libraries | Native Mach-O | Native PE or managed IL |
| Compilation at execution | May use interpreter/JIT; profile-guided AOT | Usually compiled ahead of launch | Native or CLR JIT/AOT |
| Heap management | Tracing garbage collection | ARC for reference-managed objects | Native ownership or .NET GC |
| Typical startup cost | Process fork, runtime/class setup, UI | Process/loader/framework/UI | Loader/runtime and UI depending on app |

**Dependency order:** launcher request → app process → runtime and classes → Application/Activity callbacks → surface/layout/draw. A warm start can reuse a running process; a cold start cannot. A cached process can be terminated without an application callback, so RuralReach must persist records *before* claiming they are saved.

**Low-memory decision:** Native code is not automatically superior. The correct test compares peak proportional set size, allocations, pause durations and startup on the target devices. Restrict unbounded caches and image loading, paginate large lists, and keep persisted state independent of the Activity.

## Task 4 — Security failure analysis for a mobile notes/visit app (7 marks)

Assume an engineer proposes four shortcuts: ask every permission immediately, keep bearer tokens in shared files, use HTTP, and allow arbitrary unsigned updates.

| Shortcut | Security boundary weakened | Plausible failure | Corrective measure |
|---|---|---|---|
| Blanket permissions | Least privilege | Unneeded location/camera access | Request at point of use; tolerate denial |
| Shared bearer token | App-private storage | Another process reads token | Private storage, protected key material, short token lifetime |
| Plain HTTP | Transport integrity/confidentiality | On-path interception or alteration | HTTPS with certificate and host verification |
| Arbitrary update | Signing-chain integrity | Tampered app binary accepted | Official signed distribution and signature verification |

**Threat walkthrough:** A worker logs in on an untrusted hotspot. HTTP transmits an access token; a local network attacker can intercept it. The confidentiality boundary is broken *in transit*, even if the token was encrypted at rest. Switching to TLS and enforcing certificate validation repairs that specific boundary; token expiry, server authorization and revocation reduce impact of compromise.

For RuralReach, the app should also set internal components non-exported where possible, validate data from exported intents, request only required capabilities, use encrypted local storage with keys protected by Android Keystore or iOS Keychain, and avoid storing identifiers in logs. A lost phone with an active unlocked session remains a residual risk; use short app-lock windows and remote credential revocation.

**Regression case:** On camera permission denial the worker can enter an observation manually, save it, and later attach a photo after granting permission. Security hardening should not prevent the core offline workflow.

## Task 5 — Reason about CPU, Doze and battery policy (7 marks)

Define three *conceptual* application states, not literal universal Android OS modes:

| State | Entry | Work permitted by design | Exit |
|---|---|---|---|
| ACTIVE | Foreground interaction | UI, capture, bounded processing | Screen off/inactivity |
| QUIET | No visible activity | Persisted queue; OS-scheduled routine sync | App opens or deeper idle |
| DEFERRED | Device idle/power constraints | No polling; wait for allowed maintenance/urgent OS delivery | User activity, scheduling window or permitted event |

In ACTIVE, CPU cores can scale frequency using device policy; a permanent maximum clock is wasteful. In QUIET, the app should not spin or sample GPS continually. In DEFERRED, WorkManager and OS policies delay routine transfers. A high-priority notification may be handled according to platform rules, but it does not grant unlimited execution or a guaranteed delivery deadline.

**Conflict test:** If a developer holds a partial wakelock all night, sleep opportunities decrease and battery savings are defeated. A more defensible design stores each visit transactionally, queues uploads and releases any short-lived wake resource in a finally block.

**15% battery policy:** Decrease nonurgent location sampling, compress/batch uploads, stop decorative background animation and postpone bulk synchronization. Emergency alerts use a separate priority route. This knowingly trades location granularity for a longer field shift.

## Task 6 — Design RuralReach across three device classes (13 marks)

### Requirements and decision
Workers collect synthetic visit records during six-hour outages and must operate for a ten-hour shift. The design must avoid duplicate server records and limit exposure if a device is stolen. The supported clients are: (A) an Android smartphone, (B) an iPhone, and (C) a legacy J2ME/WML feature phone.

| Device | Execution/storage | Offline approach | Security decision |
|---|---|---|---|
| A Android | ART, local SQLite/Room | Transactional pending queue | App-private encrypted database, Keystore-backed keys |
| B iPhone | Native frameworks, protected local files/database | Equivalent durable queue | Data Protection and Keychain-protected secrets |
| C legacy phone | Limited J2ME/browser environment | Minimal form if capable | **Do not** store identifiable records offline without verified protection |

### Mobile architecture
UI → input validation → local repository → encrypted storage + pending outbox → OS-scheduled synchronizer → authenticated TLS API → server-side idempotent database. Pseudonymous identifiers, record UUID, schema version, modification version and sync state travel through the protocol; encryption keys do not.

### Record state transitions
1. Worker signs in and obtains short-lived authorized access.
2. A record UUID is generated once, not on each retry.
3. Input is validated and encoded into a transaction.
4. On production smartphones, record and outbox metadata are encrypted and durably committed.
5. UI displays “Saved on device”, not “Uploaded”.
6. Synchronizer selects an eligible batch when connectivity/power conditions permit.
7. Server verifies authorization and unique UUID, then commits before acknowledging.
8. Only after a durable acknowledgement does the device mark the UUID synced.
9. Failure, timeout or process death leaves the same UUID pending for retry.
10. Conflicting edits require version-aware reconciliation, not silent last-writer-wins.

### Desk-check: lost Android phone after six hours offline
At 09:00 the worker records entry R-17, which is stored as pending. Connectivity remains absent, so the server has no copy. At 14:30 the battery reaches 20%, causing routine transfers to remain queued and sampling to slow. At 15:00 the phone is lost before synchronization. The administrator revokes its credential and attempts remote wipe if supported. Encryption limits disclosure, but the *unsynced record can be irretrievably lost* if there is no approved encrypted backup. Never claim that revocation restores an unsynced record.

### Four adversarial desk-checks
- **Reply lost after server commit:** retry same UUID; unique constraint prevents duplicate.
- **Stolen but unlocked device:** an open session can expose data; enforce re-authentication and revocation.
- **Wrong device clock:** order and conflict resolution must use server versions/time, not client clock alone.
- **Legacy storage without encryption:** prohibit offline personally identifiable health records and use an approved alternative workflow.

### Engineering evaluation
This proposal balances availability and privacy but cannot simultaneously guarantee zero data loss on an offline lost device. Its strongest properties are clear trust boundaries, user-visible sync status, server-side idempotency and explicit restrictions on weak legacy hardware. Field validation is still required for battery life, reliable notifications and encrypted-at-rest behavior.
