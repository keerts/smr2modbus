# smr2modbus

Bridge SMR v5 telegrams from a telnet stream to Modbus TCP Input Registers.

## Scope

- Input source: unauthenticated telnet stream with DSMR/SMR telegram frames
- Output protocol: Modbus TCP (Input Registers)
- Supported outputs:
  - Current L1
  - Current L2
  - Current L3
  - Current N (fixed to zero)
  - Real Power L1
  - Real Power L2
  - Real Power L3

## OBIS Mapping

- Current L1: `1-0:31.7.0`
- Current L2: `1-0:51.7.0`
- Current L3: `1-0:71.7.0`
- Current N: fixed `0`
- Real Power L1: `1-0:21.7.0 - 1-0:22.7.0`
- Real Power L2: `1-0:41.7.0 - 1-0:42.7.0`
- Real Power L3: `1-0:61.7.0 - 1-0:62.7.0`

## Register Profile (Alfen-friendly default)

- Current L1: address `23312`, `UNSIGNED32`, scale `x0.01 A`
- Current L2: address `23314`, `UNSIGNED32`, scale `x0.01 A`
- Current L3: address `23316`, `UNSIGNED32`, scale `x0.01 A`
- Current N: address `23318`, `UNSIGNED32`, scale `x0.01 A`
- Real Power L1: address `23324`, `SIGNED32`, scale `x0.001 kW`
- Real Power L2: address `23326`, `SIGNED32`, scale `x0.001 kW`
- Real Power L3: address `23328`, `SIGNED32`, scale `x0.001 kW`

Word order is configurable: `high_to_low` or `low_to_high`.
Enable query logging with `modbus.log_register_queries = true`.

## Run

```bash
python3 -m smr2modbus --config config.example.toml
```

Health endpoint defaults to `http://0.0.0.0:8080` and returns JSON readiness state.

## Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
