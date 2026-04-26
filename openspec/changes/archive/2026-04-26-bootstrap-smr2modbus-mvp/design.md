## Context

The project starts from an empty repository and needs a clean MVP path from an SMR v5 telnet telegram source to Modbus TCP output. The bridge must run continuously, survive malformed telegrams, and present deterministic register values that polling clients can trust. We also need enough observability to diagnose source connectivity and parsing issues without deep debugging.

## Goals / Non-Goals

**Goals:**
- Deliver a single-process bridge that ingests SMR v5 telegrams over telnet, parses required OBIS fields, and serves values via Modbus TCP.
- Guarantee stable register addresses and value encoding for core metrics.
- Provide configuration and health signals to make deployment and troubleshooting practical.
- Keep module boundaries clear so future capability additions (extra OBIS fields, alternate transports) do not require rework.

**Non-Goals:**
- Historical data persistence, aggregation, or analytics.
- Bidirectional control/writes back to the meter.
- Multi-meter fan-in and tenant isolation.
- Auto-discovery of meter model or dynamic register schemas in MVP.
- Serial P1 ingest mode.
- Modbus RTU output mode.

## Decisions

- Use a pipeline architecture: `ingest -> parse -> normalize -> publish`.
  - Rationale: isolates failure domains and keeps parsing concerns separate from protocol serving.
  - Alternative considered: direct parser-to-modbus coupling for less code; rejected due to lower testability and harder evolution.
- Keep latest-good metric snapshot in memory as the Modbus source of truth.
  - Rationale: Modbus polling is state-based; snapshot model makes reads deterministic and low-latency.
  - Alternative considered: on-demand parse per Modbus request; rejected due to latency and dependence on serial timing.
- Define an explicit register map module with semantic field IDs, scaling rules, and data types.
  - Rationale: prevents accidental register drift and makes client contract reviewable.
  - Alternative considered: inline register constants in server handlers; rejected due to maintainability risk.
- Treat malformed or incomplete telegrams as soft failures with metrics/logging; continue serving last-good snapshot.
  - Rationale: availability is more important than clearing values to null/zero on transient serial errors.
  - Alternative considered: invalidate snapshot on parse error; rejected because clients would see frequent disruptive drops.
- Expose health endpoints/signals that separate startup readiness from runtime degradation.
  - Rationale: operators need to distinguish "cannot start" from "running with stale data."
- Use a persistent unauthenticated telnet connection with exponential reconnect backoff up to 30 seconds.
  - Rationale: source emits telegrams on interval and should be consumed as a stream.
  - Alternative considered: reconnect for each interval; rejected due to unnecessary overhead and higher failure rate.
- Scope parser and Modbus map to exactly 7 outputs: Current L1/L2/L3/N and Real Power L1/L2/L3.
  - Rationale: fixed downstream client needs and lower complexity.
  - Alternative considered: broader OBIS support for totals and voltage; rejected for MVP focus.

## Risks / Trade-offs

- [Risk] Register schema may not match downstream SCADA expectations on first attempt -> Mitigation: keep mapping in a dedicated module and publish mapping table in docs/spec.
- [Risk] Stream interruptions can stall updates -> Mitigation: reconnect with exponential backoff and expose connection status in health output.
- [Risk] Serving stale snapshot can hide prolonged ingest failure -> Mitigation: include data-age indicator and degraded health status when freshness threshold is exceeded.
- [Trade-off] MVP chooses static configuration over dynamic discovery -> Mitigation: design config model to support future profile expansion.

## Migration Plan

No existing runtime is in place, so migration is greenfield:
1. Implement telnet ingest, parser, mapping, Modbus, and health modules.
2. Run unit tests with fixture telegrams.
3. Start bridge against test telnet stream and validate Modbus register responses.
4. Promote to target host and monitor connection/freshness indicators.

Rollback: stop the bridge process and revert to previous deployment artifact when available.

## Open Questions

- None for MVP scope.
