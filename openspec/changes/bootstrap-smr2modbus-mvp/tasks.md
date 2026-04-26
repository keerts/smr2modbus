## 1. Project Scaffold

- [x] 1.1 Create project structure for ingest, parse, register-map, modbus-server, config, and health modules
- [x] 1.2 Add and lock required dependencies for telnet communication, Modbus TCP server, and testing
- [x] 1.3 Implement startup configuration loader and validation with clear error reporting

## 2. SMR Ingest and Parse Pipeline

- [x] 2.1 Implement persistent telnet reader that frames complete P1 telegram messages
- [x] 2.2 Implement parser for required MVP OBIS fields and normalize to internal metric identifiers
- [x] 2.3 Add error handling so malformed telegrams are logged and excluded from snapshot updates

## 3. Modbus Publishing

- [x] 3.1 Define static register map with addresses, scaling rules, and value encodings
- [x] 3.2 Implement in-memory latest-good snapshot store shared between parser and Modbus server
- [x] 3.3 Implement Modbus TCP read handlers that serve values from snapshot according to mapping

## 4. Health, Freshness, and Observability

- [x] 4.1 Implement readiness and health status signals for startup and runtime ingestion state
- [x] 4.2 Add data-freshness tracking and degraded status when update age exceeds threshold
- [x] 4.3 Add structured logging for ingest failures, parse failures, startup config errors, and state transitions

## 5. Validation and Delivery

- [x] 5.1 Add unit tests for telegram framing, OBIS parsing, and register mapping correctness
- [x] 5.2 Add integration-style register encoding tests using fixture telegram values
- [x] 5.3 Document configuration keys, register map, and local run instructions in project README
