# Mobile Computing – Assignment 4 (CO4)

**Student:** Vinay Kumar  
**Register number:** 192373042  
**Institution:** Saveetha School of Engineering, SIMATS

## Goal
An original, individually authored design study and reproducible software model exploring modern mobile computing: platform architecture, secure push delivery, application runtime, security, power policy and offline-first healthcare.

## Contents
- [Part I design answers](part1_design/assignment_answers.md): six detailed tasks with original diagrams and engineering decisions.
- [Part II experiment guide](part2_prototype/EXPERIMENTS.md): method, metrics, expected findings, limitations, and evidence collection.
- [Python simulation](part2_prototype/mobile_lab.py): runnable standard-library prototype of background work, delivery idempotency, runtime startup, and permission checks.
- [Tests](part2_prototype/test_mobile_lab.py): repeatable unit tests.
- [Android evidence checklist](evidence/android_evidence.md): commands for collecting **real** Android data.

## Run
From this directory:
```bash
python part2_prototype/mobile_lab.py
python -m unittest discover -s part2_prototype -p "test_*.py" -v
```
Python 3.10+; no external dependencies.

## Evidence integrity
The Python results are **simulated policy outcomes**, not Android OS/device measurements. They cannot establish ART internals, Doze behavior, actual battery energy, CPU affinity, or permission enforcement. Collect your own screenshots, logs and environment details where required by the marking rubric. Do not commit API keys, patient information or real device IDs.

## Originality and attribution
The organization of questions was informed by an example student repository, but this submission contains newly written explanations and newly authored code. Academic and technical claims should be checked against the official references in Part I. Review the exact faculty question paper to confirm task wording before submitting.
