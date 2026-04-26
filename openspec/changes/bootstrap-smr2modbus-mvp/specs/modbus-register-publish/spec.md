## ADDED Requirements

### Requirement: Modbus server SHALL expose stable register mapping
The bridge SHALL expose normalized metrics through a fixed Modbus TCP Input Register map where each metric is bound to a deterministic register address and encoding rule.

#### Scenario: Client polls known register
- **WHEN** a Modbus client reads a register defined in the mapping
- **THEN** the server returns the value encoded according to the mapping specification

### Requirement: Publisher MUST serve the latest valid snapshot
The Modbus publisher MUST serve values from the most recently accepted normalized snapshot and MUST keep values unchanged when a newer telegram fails validation.

#### Scenario: Invalid telegram follows valid snapshot
- **WHEN** a parse failure occurs after a previously valid snapshot was published
- **THEN** Modbus reads continue returning values from the last valid snapshot

### Requirement: Publisher SHALL support configurable 32-bit word order
The publisher SHALL encode 32-bit values in either high-to-low or low-to-high word order according to configuration.

#### Scenario: Word order is configured to low-to-high
- **WHEN** the publisher encodes a 32-bit value
- **THEN** the two 16-bit Modbus words are emitted in low-word-first order
