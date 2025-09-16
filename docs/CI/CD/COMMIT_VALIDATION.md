# Commit Validation with Husky and Commitlint

This document explains the commit validation system implemented in the project using Husky and commitlint to ensure consistent and high-quality commit messages.

---

## Overview

The project uses:

- **Husky**: Git hooks management
- **Commitlint**: Commit message validation
- **Conventional Commits**: Standardized commit format

---

## Installation and Setup

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Git repository

### Automatic Setup

When you run `npm install`, the following happens automatically:

1. Husky installs git hooks
2. Dependencies are installed
3. Git hooks are configured

---

## Commit Message Format

All commit messages must follow the Conventional Commits specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Examples

```bash
# Simple commit
feat: add user authentication system

# With scope
fix(auth): resolve login validation issue

# With body and footer
feat(survey): implement anonymous survey creation

Add functionality to create surveys without requiring user registration.
This enables anonymous data collection while maintaining privacy.

Closes #123
```

---

## Allowed Commit Types

| Type       | Description              | Example                                    |
| ---------- | ------------------------ | ------------------------------------------ |
| `feat`     | New feature              | `feat: add survey dashboard`               |
| `fix`      | Bug fix                  | `fix: resolve database connection issue`   |
| `docs`     | Documentation changes    | `docs: update API documentation`           |
| `style`    | Code style changes       | `style: format code with prettier`         |
| `refactor` | Code refactoring         | `refactor: simplify user service logic`    |
| `perf`     | Performance improvements | `perf: optimize database queries`          |
| `test`     | Adding/updating tests    | `test: add unit tests for auth module`     |
| `chore`    | Maintenance tasks        | `chore: update dependencies`               |
| `ci`       | CI/CD changes            | `ci: add automated testing workflow`       |
| `build`    | Build system changes     | `build: configure webpack for production`  |
| `revert`   | Revert previous commit   | `revert: undo user authentication changes` |
| `hotfix`   | Critical bug fixes       | `hotfix: fix security vulnerability`       |
| `security` | Security improvements    | `security: implement input validation`     |
| `deps`     | Dependency updates       | `deps: upgrade Django to 4.2`              |
| `config`   | Configuration changes    | `config: update database settings`         |

---

## Validation Rules

### Subject Line Rules

- **Length**: 10-72 characters
- **Case**: sentence-case or lower-case
- **Required**: Type and description are mandatory
- **Format**: Must follow conventional commits format

### Body and Footer Rules

- **Line length**: Maximum 100 characters per line
- **Optional**: Body and footer are optional but recommended for complex changes

### Scope Rules (Optional)

- **Case**: lowercase only
- **Length**: Maximum 20 characters
- **Examples**: `auth`, `survey`, `api`, `ui`, `db`

---

## Git Hooks

### Pre-commit Hook

Runs before each commit to validate:

- Basic linting

### Commit-msg Hook

Validates commit message format using commitlint rules.

---

## Usage Examples

### Valid Commits

```bash
git commit -m "feat: add survey creation endpoint"
git commit -m "fix(auth): resolve token expiration issue"
git commit -m "docs: update installation instructions"
git commit -m "test(survey): add integration tests for API"
```

### Invalid Commits (Will be rejected)

```bash
git commit -m "added new feature"           # Missing type
git commit -m "fix"                         # Too short
git commit -m "FEAT: ADD NEW FEATURE"       # Wrong case
git commit -m "random: some changes"       # Invalid type
```

---

## Breaking Changes

For breaking changes, use one of these formats:

```bash
# With BREAKING CHANGE footer
feat(api): change authentication endpoint

BREAKING CHANGE: The /auth endpoint now requires API key in header

# With ! in type
feat(api)!: change authentication endpoint
```

---

## Integration with Changelog

The commit validation system integrates with the automatic changelog generation:

1. **Categorization**: Commits are automatically categorized based on type
2. **Filtering**: Only valid conventional commits appear in changelog
3. **Consistency**: Ensures uniform changelog entries

---

## Troubleshooting

### Common Issues

#### Hook not running

```bash
# Reinstall hooks
npx husky install
```

#### Commitlint errors

```bash
# Test commit message
echo "feat: test message" | npx commitlint
```

#### Permission issues (Unix/Linux)

```bash
# Make hooks executable
chmod +x .husky/*
```

### Bypassing Validation (Emergency Only)

```bash
# Skip pre-commit hook
git commit --no-verify -m "emergency fix"

# Note: commit-msg validation will still run
```

---

## Configuration Files

### `package.json`

Contains scripts and basic commitlint configuration.

### `commitlint.config.js`

Detailed commitlint rules and configuration.

### `.husky/`

Directory containing git hook scripts:

- `pre-commit`: Pre-commit validations
- `commit-msg`: Commit message validation

---

## Best Practices

1. **Write clear descriptions**: Be specific about what changed
2. **Use appropriate types**: Choose the most accurate type
3. **Include scope when relevant**: Helps with organization
4. **Write body for complex changes**: Explain why, not just what
5. **Reference issues**: Use `Closes #123` or `Fixes #456`
6. **Keep commits atomic**: One logical change per commit

> Visit the CommitS Convention Guide for more details: https://www.conventionalcommits.org/es/v1.0.0/

---

## Team Guidelines

### For Developers

- Always write meaningful commit messages
- Use conventional commits format
- Test your changes before committing
- Include relevant scope when applicable

### For Code Reviews

- Verify commit messages follow conventions
- Check that commits are atomic and logical
- Ensure proper categorization for changelog

---

## Integration with CI/CD

The validation system works with:

- **GitHub Actions**: Validates commits in pull requests
- **Automatic Changelog**: Generates changelog from commit history
- **Release Process**: Creates releases based on conventional commits
