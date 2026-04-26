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

## Docker

Build locally:

```bash
docker build -t smr2modbus:local .
```

Run locally with mounted config and published Modbus/health ports:

```bash
docker run --rm \
  -p 502:502 \
  -p 8080:8080 \
  -v "$(pwd)/config.example.toml:/app/config.toml:ro" \
  smr2modbus:local \
  --config /app/config.toml
```

## GHCR Publishing and Tags

This repository publishes container images to `ghcr.io/<owner>/smr2modbus`.

Tag channels:

- `edge`: moving development tag published from `master`
- `sha-<shortsha>`: immutable commit tag published from `master` and releases
- `vX.Y.Z`: immutable release tag published from git tags like `v1.2.3`
- `vX`: moving major tag published on releases (for example `v1`)
- `latest`: moving stable tag published only on releases

Branch pushes do not move stable channels (`latest` and `vX`).

## NAS Deployment Guidance

Recommended tracking strategy:

- Track `vX` (for example `ghcr.io/<owner>/smr2modbus:v1`) for stable updates within one major line.
- Pin `vX.Y.Z` when you need strict change control.

Rollback:

- Repoint deployment to the previous immutable tag (for example from `v1.2.4` back to `v1.2.3`).

## Release Process

1. Merge release-ready changes into `master`.
2. Create and push a SemVer git tag (for example `v1.0.0`).
3. Wait for the `Publish Container` workflow to publish `vX.Y.Z`, `vX`, `latest`, and `sha-<shortsha>`.
4. Verify pull and startup with your target config.

Example:

```bash
git tag v1.0.0
git push origin v1.0.0
```
