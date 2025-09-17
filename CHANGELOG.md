# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2025-09-17

### Added
- feat(release): upgrade to version 1.0.1
- feat(release): enhance release workflow with version sync and manual trigger
- feat(release): enhance release workflow with version synchronization
- ci(release): add manual trigger and version updates to release workflow
- ci(scripts): add script to update package-lock.json version
- feat(ci): add script to update package version
- ci(scripts): add script to update version in pyproject.toml
- feat: Upgrade to version 1.0.0

### Changed
- docs(CI): update changelog generation documentation
- ci(changelog): modify workflow to support manual triggering

## [0.0.0] - 2024-12-19

### Added
- Initial project structure for raccoon-survey platform
- Core application directories (`src/core/`) with subdirectories for database, models, routes, services, and utils
- UI directories (`src/ui/`) with public, static, and templates folders
- Test directories structure with e2e, integration, and unit test folders
- Documentation directory (`docs/`)
- GitHub workflows directory (`.github/workflows/`)
- Project configuration files:
  - `pyproject.toml` with basic project metadata
  - `.python-version` specifying Python 3.13
  - `.gitignore` with Python-specific exclusions
  - `uv.lock` for dependency management
- Project documentation files:
  - `README.md`
  - `LICENSE` (MIT)
  - `CODE_OF_CONDUCT.md`
  - `CONTRIBUTING.md`
  - `SECURITY.md`
  - `CHANGELOG.md`

[Unreleased]: https://github.com/Javi-CD/raccoon-survey/compare/v1.0.1...HEAD
[0.0.0]: https://github.com/Javi-CD/raccoon-survey/releases/tag/v0.0.0
[1.0.1]: https://github.com/Javi-CD/raccoon-survey/releases/tag/v1.0.1
