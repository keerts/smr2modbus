## Why

The current 32-bit pair-register mapping increases client-side complexity and makes quick verification harder for Modbus tools and charger integrations. A compact 16-bit contiguous register block simplifies configuration and polling.

## What Changes

- Replace 32-bit two-register value encoding with 16-bit single-register encoding for all published metrics.
- Change the published register map to a compact contiguous range from `1` through `7`.
- Remove backward compatibility with the existing 32-bit map.
- Update configuration examples, tests, and documentation to reflect the new 16-bit model.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `modbus-register-publish`: change metric encoding from 32-bit paired registers to 16-bit single registers and adopt a compact contiguous address map.
- `bridge-configuration-and-health`: update configuration expectations for register data types and clarify that 32-bit word-order semantics are no longer relevant for published metric values.

## Impact

- Breaking change for any existing clients expecting 32-bit paired-register values.
- Runtime register values and addresses change for real power metrics and current N placement.
- Requires updates to test expectations and operational verification procedures.
