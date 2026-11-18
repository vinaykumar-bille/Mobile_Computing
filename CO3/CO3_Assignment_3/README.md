# CO3: Mobility and Routing

**Course:** Mobile Computing

## Aim
Understand handoff decisions, Mobile IP registration, and route discovery in wireless mobile networks through simple reproducible simulations.

## Concepts
- **Handoff:** when a mobile station changes its serving access point as signal conditions change. Hysteresis helps avoid repeated switching.
- **Mobile IP:** a mobile node retains its home address while a care-of address indicates its visited network. The home agent maintains a binding.
- **DSDV:** proactive distance-vector routing maintains sequence-numbered routing tables.
- **AODV:** on-demand routing discovers paths through route requests and route replies.

## Procedure
Run `python simulations.py` and inspect printed traces. Compare the proactive and reactive routing behavior, then explain why fast movement or broken links may increase overhead.

## Observation
All numbers are deliberately synthetic examples, not measurements from a real wireless network. Extend the simulator to model latency, loss and changing topology for your own experiment.
