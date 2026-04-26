## Why

Deploying `smr2modbus` to a NAS should not require local source checkout or ad-hoc image builds. Publishing versioned container images to GHCR enables consistent deployments, predictable upgrades, and fast rollback.

## What Changes

- Add a containerization and release pipeline that publishes `smr2modbus` images to GHCR.
- Define stable and development image channels with explicit tag movement rules.
- Ensure release images are traceable to source commits and support deterministic rollback.
- Document how operators should consume tags for NAS deployments.

## Capabilities

### New Capabilities
- `container-image-publishing`: Build and publish release/dev container tags with stable channel guarantees and rollback-safe immutability.

### Modified Capabilities
- None.

## Impact

- Adds Docker build and publishing workflow configuration.
- Introduces GHCR package as a deployment artifact for this repository.
- Defines release/tagging expectations for operators consuming images on NAS systems.
