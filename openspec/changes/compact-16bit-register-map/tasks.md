## 1. 16-bit Register Encoding

- [x] 1.1 Replace 32-bit pair-register encoding with single-register 16-bit encoding in the publisher
- [x] 1.2 Implement and apply 16-bit clamp behavior for `uint16` and `int16` point types
- [x] 1.3 Remove paired-register writes (`address + 1`) from snapshot generation

## 2. Compact Register Map Configuration

- [x] 2.1 Update example point addresses to contiguous `1..7`
- [x] 2.2 Update example point data types from `uint32`/`int32` to `uint16`/`int16`
- [x] 2.3 Ensure unsupported legacy point types fail with actionable startup errors

## 3. Test Updates

- [x] 3.1 Update register encoding tests for single-register 16-bit behavior
- [x] 3.2 Remove word-order-dependent assertions from register tests
- [x] 3.3 Add/adjust coverage for 16-bit clamping behavior

## 4. Documentation and Validation

- [x] 4.1 Update README register mapping and encoding description to compact 16-bit layout
- [x] 4.2 Update mbpoll verification examples for contiguous range polling
- [x] 4.3 Run test suite and verify expected register values via local polling workflow
