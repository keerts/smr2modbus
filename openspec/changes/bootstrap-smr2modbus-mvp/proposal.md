## Why

SMR meters expose rich real-time data, but many home and industrial systems consume Modbus registers instead of P1 telegrams. Building a focused SMR-to-Modbus bridge now creates an interoperable foundation that can be integrated with existing PLC, SCADA, and energy dashboards.

## What Changes

- Build a service that reads DSMR/SMR telegrams from an unauthenticated telnet stream.
- Parse and normalize only the required metrics: Current L1/L2/L3/N and Real Power L1/L2/L3.
- Expose parsed metrics through a Modbus TCP server with a stable register layout.
- Add configuration for telnet source settings, network bind address, word order, and register mapping profile.
- Add health/readiness signals and structured logs for operational visibility.

## Capabilities

### New Capabilities
- `smr-telegram-ingest`: Acquire and validate telegram frames from a persistent telnet source with reconnect backoff.
- `smr-telegram-parse`: Parse required OBIS fields for the 7 requested outputs and normalize values.
- `modbus-register-publish`: Publish normalized metrics as Modbus TCP input registers with configurable word order.
- `bridge-configuration-and-health`: Configure runtime behavior and expose startup/runtime health status.

### Modified Capabilities
- None.

## Impact

- Creates a new bridge service codebase and runtime entrypoint.
- Introduces telnet stream I/O and Modbus TCP dependencies.
- Establishes initial Modbus register contract that downstream clients will rely on.
- Requires test fixtures for SMR v5 telegram samples and register encoding behavior.
