## ADDED Requirements

### Requirement: Release images MUST be published to GHCR on SemVer tags
The publish pipeline MUST build and push an image to `ghcr.io/<owner>/smr2modbus` whenever a git tag matching `v*` is created.

#### Scenario: Release tag is pushed
- **WHEN** a git tag `v1.2.3` is pushed
- **THEN** the pipeline publishes an image tagged `v1.2.3`
- **AND** the image can be pulled from GHCR by that exact tag

### Requirement: Stable channel tags MUST move only on release tags
The stable channel tags `latest` and major tag `v<major>` MUST only be updated during SemVer release-tag publishes, not during branch pushes.

#### Scenario: Branch push occurs
- **WHEN** code is pushed to the default branch without a release tag
- **THEN** `latest` remains unchanged
- **AND** major tags (for example `v1`) remain unchanged

#### Scenario: Release tag occurs
- **WHEN** tag `v1.3.0` is pushed
- **THEN** `latest` points to `v1.3.0`
- **AND** `v1` points to `v1.3.0`

### Requirement: Development channel MUST be published from default branch
The publish pipeline MUST publish development tags from the default branch to support pre-release validation without affecting stable channels.

#### Scenario: Default branch push
- **WHEN** code is pushed to the default branch
- **THEN** the pipeline publishes `edge`
- **AND** the pipeline publishes a commit-derived tag `sha-<shortsha>`

### Requirement: Published releases MUST be traceable and rollback-safe
Each release publish MUST include at least one immutable version tag and one commit-derived tag so operators can identify and roll back versions deterministically.

#### Scenario: Operator needs rollback
- **WHEN** release `v1.2.4` causes regression
- **THEN** operator can pin deployment to prior immutable tag (for example `v1.2.3`)
- **AND** release artifacts can be traced to source commit via `sha-<shortsha>`
