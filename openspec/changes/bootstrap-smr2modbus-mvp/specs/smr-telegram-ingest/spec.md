## ADDED Requirements

### Requirement: Bridge SHALL ingest complete P1 telegram frames
The bridge SHALL read telegram data from a configured unauthenticated telnet source and only emit ingest events when a full telegram frame boundary is detected.

#### Scenario: Complete frame is received
- **WHEN** bytes arrive that form a valid full telegram frame
- **THEN** the bridge emits one ingest event containing exactly that frame

### Requirement: Bridge MUST tolerate transient telnet failures
The bridge MUST continue attempting reads after transient telnet connection failures and MUST surface the failure in logs/health without terminating the process.

#### Scenario: Telnet connection drops
- **WHEN** the telnet connection closes unexpectedly or a read operation fails
- **THEN** the bridge reconnects using exponential backoff capped at 30 seconds and reports degraded ingest status
