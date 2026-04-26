## 1. Container Build Definition

- [x] 1.1 Add a Dockerfile that builds a runnable `smr2modbus` image and starts the bridge with `python -m smr2modbus`
- [x] 1.2 Add image metadata labels and runtime defaults suitable for GHCR distribution
- [ ] 1.3 Validate local image build and container startup with mounted config and published Modbus/health ports

## 2. GHCR Publish Automation

- [x] 2.1 Add CI workflow to publish `edge` and `sha-<shortsha>` on default-branch pushes
- [x] 2.2 Add CI workflow tag path to publish `vX.Y.Z`, `vX`, and `latest` on `v*` git tags
- [x] 2.3 Ensure workflow permissions and login configuration support pushing to `ghcr.io/<owner>/smr2modbus`

## 3. Release Safety and Verification

- [x] 3.1 Add checks that stable tags do not move on non-release events
- [ ] 3.2 Verify published release tags are pullable and traceable to source commit
- [x] 3.3 Document rollback procedure using prior immutable version tags

## 4. Operator Documentation

- [x] 4.1 Document GHCR image naming and tag channels (`edge`, `sha-*`, `vX.Y.Z`, `vX`, `latest`)
- [x] 4.2 Document NAS consumption guidance for `vX` tracking versus pinned `vX.Y.Z`
- [x] 4.3 Document initial release process, including first SemVer tag creation and verification steps
