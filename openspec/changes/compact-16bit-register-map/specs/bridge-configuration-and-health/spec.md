## MODIFIED Requirements

### Requirement: Bridge SHALL validate startup configuration
The bridge SHALL load telnet source and Modbus configuration at startup and SHALL fail fast with actionable errors when required settings are missing or invalid, including unsupported point data types for the active register publishing model.

#### Scenario: Configuration is invalid at startup
- **WHEN** the process starts with an invalid telnet host/port or Modbus port binding
- **THEN** startup fails and the error output identifies the invalid setting

#### Scenario: Unsupported point data type is configured
- **WHEN** a point uses an unsupported data type for compact 16-bit publishing
- **THEN** startup fails and the error output identifies the invalid point data type

### Requirement: Bridge MUST report readiness and runtime freshness
The bridge MUST expose readiness and health information that reflects ingest/parser state and marks the service degraded when data freshness exceeds a configured threshold.

#### Scenario: Data becomes stale
- **WHEN** no valid telegram has updated the snapshot before the freshness threshold expires
- **THEN** health status changes to degraded while the process remains running
