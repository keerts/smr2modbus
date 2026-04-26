## ADDED Requirements

### Requirement: Parser SHALL extract required OBIS metrics
The parser SHALL extract configured required OBIS fields from each ingested telegram and map them to exactly these normalized metric identifiers: Current L1/L2/L3/N and Real Power L1/L2/L3.

#### Scenario: Required OBIS fields are present
- **WHEN** a telegram contains all required OBIS fields for MVP
- **THEN** the parser outputs a normalized metric set containing each required identifier and value

### Requirement: Parser SHALL compute per-phase signed real power
The parser SHALL compute per-phase real power as import minus export (`21.7.0-22.7.0`, `41.7.0-42.7.0`, `61.7.0-62.7.0`) and SHALL allow negative values for export conditions.

#### Scenario: Export exceeds import on one phase
- **WHEN** a telegram has phase export value greater than phase import value
- **THEN** the parser outputs a negative real power value for that phase

### Requirement: Parser MUST reject invalid metric values safely
The parser MUST reject malformed, out-of-range, or non-numeric required values and MUST not overwrite the current snapshot with invalid data.

#### Scenario: One required field is malformed
- **WHEN** a telegram includes a malformed value for a required OBIS field
- **THEN** the parser reports a parse failure and no new snapshot is published from that telegram
