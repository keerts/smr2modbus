## MODIFIED Requirements

### Requirement: Modbus server SHALL expose stable register mapping
The bridge SHALL expose normalized metrics through a fixed Modbus TCP Input Register map where each metric is bound to one deterministic 16-bit register address and encoding rule.

#### Scenario: Client polls known register
- **WHEN** a Modbus client reads a register defined in the mapping
- **THEN** the server returns the value encoded according to the mapping specification

### Requirement: Publisher MUST serve the latest valid snapshot
The Modbus publisher MUST serve values from the most recently accepted normalized snapshot and MUST keep values unchanged when a newer telegram fails validation.

#### Scenario: Invalid telegram follows valid snapshot
- **WHEN** a parse failure occurs after a previously valid snapshot was published
- **THEN** Modbus reads continue returning values from the last valid snapshot

### Requirement: Publisher SHALL use compact contiguous 16-bit register layout
The publisher SHALL encode each required metric into one 16-bit register and SHALL publish the 7 metrics in a contiguous range from `1` through `7`.

#### Scenario: Client reads compact range
- **WHEN** a client reads registers `1` through `7`
- **THEN** the response includes exactly one value for each metric in order: current L1/L2/L3/N, real power L1/L2/L3

### Requirement: Publisher SHALL clamp values to 16-bit data type bounds
The publisher SHALL clamp encoded values to the configured 16-bit type bounds before publishing (`uint16` for current, `int16` for real power).

#### Scenario: Encoded value exceeds 16-bit range
- **WHEN** a scaled metric exceeds the representable bound for its configured 16-bit type
- **THEN** the published register value is clamped to the nearest valid bound
