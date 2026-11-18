# Mobile Computing – Assignment 4 (CO4)

**Student:** Vinay Kumar  
**Register number:** 192373042  
**Institution:** Saveetha School of Engineering, SIMATS  
**Course:** Mobile Computing / Mobile Application Development Environment  
**Submission:** Part I (design) and Part II (simulation plus device-evidence plan)

## Original case study
**RuralReach:** A battery-aware, offline-first field visit recorder for healthcare workers. This is a teaching prototype using *synthetic, non-patient* records. It does not provide medical advice, does not handle real patient data, and is **not** a production healthcare system.

## Contents
- `part1_design.md`: six independent architectural/design answers
- `part2_experiments.md`: six tasks with predictions, reproduction steps, evaluation and limitations
- `diagrams.md`: Mermaid system, lifecycle, trust boundary and sync diagrams
- `prototype/policy.py`: deterministic sampling and upload scheduler
- `prototype/offline_queue.py`: simulated durable/idempotent synchronization
- `prototype/audit.py`: secure-design configuration linter (not a penetration test)
- `prototype/run_all.py`: reproducible demonstration, generating local CSV
- `tests/test_assignment4.py`: standard-library unit tests
- `evidence/DEVICE_EVIDENCE_CHECKLIST.md`: genuine Android Studio/ADB instructions

## How to run on Windows PowerShell
From this folder:

```powershell
python -m unittest discover -s tests -v
python prototype/run_all.py
```

Python 3.10+; no external packages. `prototype/run_all.py` writes `results/policy_decisions.csv` and `results/sync_trace.csv`. Files in `results/` are generated **on the machine running the script**, not proof of device execution.

## Academic integrity and evidence
The reference repository helped identify the assessment's themes and task boundaries, but this project uses a distinct example, independent architecture, independently authored simulation and original tests. Do not describe any simulated decision or CSV output as measured Android battery consumption, measured ART execution or actual encrypted storage. Actual device measurements and screenshots are **not included** and must be collected on a personal Android test device/emulator. Replace all placeholders with truthful evidence before submission.

## Source references
1. [Android platform architecture](https://source.android.com/docs/core/architecture)
2. [Android app processes and lifecycle](https://developer.android.com/guide/components/activities/process-lifecycle)
3. [Android WorkManager](https://developer.android.com/topic/libraries/architecture/workmanager)
4. [Android power management](https://developer.android.com/training/monitoring-device-state/doze-standby)
5. [Android app security](https://developer.android.com/privacy-and-security/security-best-practices)
6. [Android Runtime](https://source.android.com/docs/core/runtime)
7. [Apple background execution](https://developer.apple.com/documentation/backgroundtasks)
8. [Apple platform security](https://support.apple.com/guide/security/welcome/web)
9. [Microsoft Windows app security](https://learn.microsoft.com/windows/uwp/security/)
10. Reference for the assignment's task structure: [Mobile-Computing- commit](https://github.com/jaswanthkrishna802/Mobile-Computing-/commit/ba6a36dda98f59e7d3eb718674af3bcf4a3fef6c)

**No credentials, tokens, patient identifiers, device IDs or personal data should be committed.**
