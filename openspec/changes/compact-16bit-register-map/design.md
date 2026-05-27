## Context

The bridge currently publishes metrics as 32-bit values split across two 16-bit Modbus registers. Downstream consumers in this project benefit more from a simple contiguous single-register map than from 32-bit width and configurable word order.

## Goals / Non-Goals

**Goals:**
- Publish each metric as one 16-bit register.
- Use a compact contiguous block from `1` to `7`.
- Keep existing scaling semantics where possible.
- Make Modbus polling and client mapping simpler.

**Non-Goals:**
- Backward compatibility with the previous 32-bit register map.
- Supporting both 16-bit and 32-bit modes at runtime.
- Introducing new metrics beyond the current 7 outputs.

## Decisions

- Hard-switch to 16-bit only encoding for all points.
  - Rationale: avoids dual-mode complexity and aligns with explicit scope.
- Use data types `uint16` for currents and `int16` for real power.
  - Rationale: preserves sign handling for real power while keeping one register per metric.
- Adopt compact mapping:
  - `1` current_l1
  - `2` current_l2
  - `3` current_l3
  - `4` current_n
  - `5` real_power_l1
  - `6` real_power_l2
  - `7` real_power_l3
- Keep scaling values unchanged (`0.01 A` and `0.001 kW`).
  - Rationale: preserves engineering units expected by downstream clients.
- Clamp raw values to 16-bit bounds before publishing.
  - Rationale: predictable behavior when values exceed representable range.

## Risks / Trade-offs

- [Risk] Existing clients break due to removed 32-bit layout -> Mitigation: clearly document breaking change and new map.
- [Risk] High values may saturate due to 16-bit limits -> Mitigation: explicit clamp behavior in implementation/tests.
- [Trade-off] `modbus.word_order` becomes irrelevant for value encoding -> Mitigation: document this and keep config handling explicit.

## Migration Plan

1. Update register encoding to 16-bit single-register writes.
2. Update config example data types and addresses to the compact map.
3. Update tests and docs for new addressing and expectations.
4. Validate with unit tests and mbpoll against `1..7`.

Rollback: redeploy previous artifact that still publishes the 32-bit map.

## Open Questions

- None.
