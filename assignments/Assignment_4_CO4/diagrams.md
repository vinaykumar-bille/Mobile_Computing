# Original design diagrams (Mermaid)

The following diagrams are conceptual; they do not assert observed operating-system behavior.

## 1. Mobile layered architecture
```mermaid
flowchart TD
  A[RuralReach application] --> B[Android framework and system services]
  B --> C[Binder and native services]
  B --> D[Android Runtime ART]
  C --> E[Hardware Abstraction Layer]
  C --> F[Linux kernel]
  D --> F
  E --> F
  F --> G[CPU storage sensors radios]
```

## 2. Notification and acknowledgement
```mermaid
sequenceDiagram
  participant S as Message server
  participant P as OS push service
  participant U as Worker
  participant A as Mobile app
  S->>S: Persist UUID and message
  S->>P: Push notification hint
  P-->>U: Display alert if allowed
  U->>A: Open app
  A->>S: Authenticated fetch(UUID)
  S-->>A: Message payload
  A->>S: Acknowledge UUID
```

## 3. Offline sync status machine
```mermaid
stateDiagram-v2
  [*] --> PENDING: durable local commit
  PENDING --> IN_FLIGHT: send same UUID
  IN_FLIGHT --> SYNCED: server durable ACK
  IN_FLIGHT --> PENDING: timeout or error
  SYNCED --> [*]
```

## 4. Trust and key boundary
```mermaid
flowchart LR
  subgraph Device
    UI[Worker UI] --> V[Validation]
    V --> DB[Encrypted local queue]
    K[Protected key store] -. key reference .-> DB
  end
  DB --> T[Authenticated HTTPS]
  T --> API[Authorization + schema checks]
  API --> ID[Server UUID uniqueness check]
  ID --> S[Server storage]
```

## 5. Adaptive energy policy
```mermaid
flowchart TD
  I[Battery network motion temperature emergency] --> E{Emergency?}
  E -->|Yes| U[Fast sampling and immediate attempt]
  E -->|No| H{Hot or critical battery?}
  H -->|Yes| Q[Slow sampling queue upload]
  H -->|No| N{Offline?}
  N -->|Yes| O[Record locally queue]
  N -->|No| B[Batch on eligible connection]
```
