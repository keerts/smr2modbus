## Context

The runtime is currently started directly from source. Operators want to deploy on NAS infrastructure where pulling a prebuilt container image is simpler and more repeatable than building locally.

## Goals / Non-Goals

**Goals:**
- Publish deployable images to GHCR from repository automation.
- Keep stable channels (`latest`, major tag) tied only to SemVer release tags.
- Provide a development channel (`edge`, `sha-*`) without affecting stable consumers.
- Support deterministic rollback through immutable version tags.

**Non-Goals:**
- Implementing orchestrator-specific deployment manifests.
- Defining secrets management for every NAS platform.
- Changing application behavior or register/protocol semantics.

## Decisions

- Trigger release publishing on git tags matching `v*`.
  - Rationale: aligns image lifecycle with explicit release intent.
- Publish `vX.Y.Z`, `vX`, and `latest` on release tags.
  - Rationale: provides immutable, major-track, and convenience channels.
- Trigger development publishing on default-branch pushes.
  - Rationale: enables pre-release validation without moving stable channels.
- Publish `edge` and `sha-<shortsha>` on default-branch pushes.
  - Rationale: gives one moving dev tag and one immutable traceable dev tag.

## Risks / Trade-offs

- [Risk] Misconfigured workflow could move `latest` on non-release events -> Mitigation: separate event conditions for branch vs tag publishing.
- [Risk] NAS clients may track moving tags unintentionally -> Mitigation: document pinned-tag and major-tag consumption guidance.
- [Trade-off] Public GHCR package simplifies pulls but increases artifact visibility -> Mitigation: allow private package option if operational requirements change.

## Migration Plan

1. Add container build definition and CI publishing workflow.
2. Validate development publish on default branch (`edge`, `sha-*`).
3. Create first release tag (`v1.0.0` or chosen initial version) and verify stable tags.
4. Update NAS deployment to consume `v1` (or pinned `vX.Y.Z`).

Rollback: repoint NAS deployment to a prior immutable image tag (for example `v1.2.3`).

## Open Questions

- Should GHCR package visibility default to public immediately, or be private until first production rollout?
