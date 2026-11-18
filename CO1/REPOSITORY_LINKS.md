# Mobile Computing – Assignment and Lab Index

**Student:** B. Student | **Register:**  | **SIMATS Engineering**

This repository is organized into **CO1, CO2, CO3, CO4, CO5 and Lab_Experiments**. The CO3–CO5 companion reports and scripts are **original**; diagrams are stored in Mermaid text and render in GitHub Markdown. Supporting files are educational logic models, not fabricated Android or wireless measurements.

| Section | Repository folder | Core report or evidence |
|---|---|---|
| CO1 | [CO1](https://github.com/Student-bille/Mobile_Computing/tree/main/CO1) | Concept map PDF |
| CO2 | [CO2](https://github.com/Student-bille/Mobile_Computing/tree/main/CO2) | Assessment PDFs |
| CO3 | [CO3](https://github.com/Student-bille/Mobile_Computing/tree/main/CO3) | [Original report](https://github.com/Student-bille/Mobile_Computing/blob/main/CO3/CO3_Assignment_3/REPORT.md), [Python simulations](https://github.com/Student-bille/Mobile_Computing/tree/main/CO3/CO3_Assignment_3/experiments.py), [Tests](https://github.com/Student-bille/Mobile_Computing/tree/main/CO3/CO3_Assignment_3/test_experiments.py) |
| CO4 | [CO4](https://github.com/Student-bille/Mobile_Computing/tree/main/CO4) | [Original report](https://github.com/Student-bille/Mobile_Computing/blob/main/CO4/CO4_Assignment_4/REPORT.md), [Practical model](https://github.com/Student-bille/Mobile_Computing/tree/main/CO4/CO4_Assignment_4/practical_model.py), [Tests](https://github.com/Student-bille/Mobile_Computing/tree/main/CO4/CO4_Assignment_4/test_practical_model.py), [Android evidence guide](https://github.com/Student-bille/Mobile_Computing/tree/main/CO4/CO4_Assignment_4/EVIDENCE.md) |
| CO5 | [CO5](https://github.com/Student-bille/Mobile_Computing/tree/main/CO5) | [Original report](https://github.com/Student-bille/Mobile_Computing/blob/main/CO5/CO5_Assignment_5/REPORT.md), [Python simulations](https://github.com/Student-bille/Mobile_Computing/tree/main/CO5/CO5_Assignment_5/experiments.py), [Tests](https://github.com/Student-bille/Mobile_Computing/tree/main/CO5/CO5_Assignment_5/test_experiments.py), [Evidence guide](https://github.com/Student-bille/Mobile_Computing/tree/main/CO5/CO5_Assignment_5/EVIDENCE.md) |
| Lab | [Lab experiments](https://github.com/Student-bille/Mobile_Computing/tree/main/Lab_Experiments) | Existing lab experiment screenshots |

## Source-based organization
- CO3 topics: wireless architecture, mobility and handoff, Mobile IP, cellular vs ad hoc networks, DSDV, AODV and emergency routing, as covered by the uploaded CO3 assignment.
- CO4 topics: architecture diagnosis, platform comparison, runtime, SecureNotes security audit, power reasoning and RuralCare offline-first design, as covered by the uploaded Part I assignment.
- CO5 topics: intent/service scheduling, incremental sync, common background workflow, local/cloud tradeoffs, UI approximation and practical investigation, as covered by the uploaded CO5 reference assignment.

## Run the Python investigations
From the repository root, on Windows PowerShell:

```powershell
python CO3/CO3_Assignment_3/experiments.py
python -m unittest discover -s CO3/CO3_Assignment_3 -p "test_*.py" -v
python CO4/CO4_Assignment_4/practical_model.py
python -m unittest discover -s CO4/CO4_Assignment_4 -p "test_*.py" -v
python CO5/CO5_Assignment_5/experiments.py
python -m unittest discover -s CO5/CO5_Assignment_5 -p "test_*.py" -v
```

**Evidence policy:** Run tests before citing pass counts. Obtain screenshots/OS metrics from your own Android emulator or device; mark theoretical and simulated data accurately. The uploaded CO5 reference PDF was authored for another student and has not been presented as your own assignment.
