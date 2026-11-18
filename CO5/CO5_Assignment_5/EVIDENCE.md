# CO5 real evidence plan
Use a sample application with no real patient data. Record Android version, model, SDK, app build, dates and all test conditions. The Python `experiments.py` models policy decisions only.

- **B1:** Instrument a WorkManager worker; record enqueue, constraints, start, finish and unique work ID.
- **B2:** Run offline → online, battery-restricted and permission-revoked scenarios; log cancellation, retry and duplicate suppression.
- **B3:** Profile exact and approximate candidate ranking in the app; capture frame timing and correctness comparison. Python inspected-item count is only a complexity illustration.
- **B4:** Test multimedia quality changes on throttled Wi-Fi if possible; document bandwidth estimate, selected bitrate and playback buffering.
- Keep screenshot names descriptive, e.g. `offline_queue.png`, `workmanager_log.txt`, `frame_time.png`.
- Redact device ID, usernames, tokens, health data and other sensitive records.
