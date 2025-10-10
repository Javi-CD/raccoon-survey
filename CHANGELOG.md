# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2025-10-10

### Added
- feat(auth): implement JWT authentication with token expiration and blocklist
- feat(questions): add service and routes for question management
- feat(surveys): add surveys service and routes with CRUD operations
- feat(teams): add teams service and routes with CRUD operations
- feat(auth): implement jwt authentication with role-based access control
- feat(auth): add JWT authentication with token revocation
- feat(auth): add authentication routes
- feat(auth): add authentication routes with jwt support
- feat(auth): add in-memory JWT token blocklist service
- feat(middleware): add user_required decorator for authentication
- feat(rbac): add role-based access control middleware
- feat(config): add JWT token expiration time configuration

### Changed
- refactor(routes): centralize route registration in core module
- refactor(auth): move auth logic to service layer

## [1.1.1] - 2025-10-08

### Added
- feat: initialize database models and migrations
- feat: initialize database models and migrations
- feat(database): add database seeding script and admin config
- feat(database): add database seeding functionality and admin user config
- feat(database): add new database migrations
- feat(database): add migrations audit log, category and question category tables
- feat(models): add new models for audit logs and categories
- feat(models): add new model classes to `__init__` file
- feat(models): add QuestionCategory model for question-category mapping
- feat(models): add Category model with database schema
- feat(models): add audit log model for tracking system changes
- feat(database): add initial database schema and migrations
- feat(database): add initial migration database schema for core tables
- feat(models): add database models for survey system
- feat(models): add models module and import in core package
- feat(models): add Response model for survey responses
- feat(models): add Question model for survey questions
- feat(models): add SurveyToken model for survey access control
- feat(models): add Survey model for survey management
- feat(models): add User model with relationships and indexes
- feat(models): add Role model with basic fields and relationships
- feat(models): add Team model for database relationships
- feat(database): add alembic for database migrations
- feat(database): add alembic for database migrations
- feat(database): add SQLAlchemy integration with PostgreSQL support
- feat(database): add SQLAlchemy integration with PostgreSQL
- feat: add main application entry point with env configuration
- feat(core): initial App Factory setup
- feat(core): add configuration module for App Factory

### Changed
- refactor(models): change question options column type from JSONB to JSON

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

[Unreleased]: https://github.com/Javi-CD/raccoon-survey/compare/v1.2.0...HEAD
[0.0.0]: https://github.com/Javi-CD/raccoon-survey/releases/tag/v0.0.0
[1.0.1]: https://github.com/Javi-CD/raccoon-survey/releases/tag/v1.0.1
[1.1.1]: https://github.com/Javi-CD/raccoon-survey/releases/tag/v1.1.1
[1.2.0]: https://github.com/Javi-CD/raccoon-survey/releases/tag/v1.2.0
