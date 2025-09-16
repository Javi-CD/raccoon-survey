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

Runs before each commit to validate and automatically fix:

#### Frontend (UI) Linting
- **ESLint**: JavaScript and HTML code quality and style
- **Stylelint**: CSS code quality and style  
- **Prettier**: Code formatting for HTML, CSS, JS, TS, JSON, and Markdown

#### Backend (Python) Linting
- **Ruff**: Python code quality, style, and automatic fixes
- **isort**: Python import sorting and organization
- **Ruff Format**: Python code formatting validation

All linting tools run with automatic fixing enabled during pre-commit to ensure code quality before commits are made.

### Commit-msg Hook

Validates commit message format using commitlint rules.

---

## Available Linting Commands

### Manual Execution

#### Frontend (UI) Commands
```bash
# Run all UI linting (with auto-fix)
npm run lint:ui

# Run UI linting checks only (no auto-fix)
npm run lint:ui-check

# Individual commands
npm run lint:js          # ESLint with auto-fix
npm run lint:js-check    # ESLint check only
npm run lint:css         # Stylelint with auto-fix  
npm run lint:css-check   # Stylelint check only
npm run format:ui        # Prettier with auto-fix
npm run format:ui-check  # Prettier check only
```

#### Backend (Python) Commands
```bash
# Run all Python linting (with auto-fix)
npm run lint:python

# Run Python linting checks only (no auto-fix)
npm run lint:python-check

# Individual commands
npm run lint:python-ruff       # Ruff with auto-fix
npm run lint:python-ruff-check # Ruff check only
npm run lint:python-isort      # isort with auto-fix
npm run lint:python-isort-check # isort check only
npm run lint:python-format-check # Ruff format check only
```

#### Combined Commands
```bash
# Run pre-commit validation manually
npm run lint:pre-commit

# This executes both:
# - npm run lint:ui
# - npm run lint:python
```

### CI/CD Integration

For continuous integration, use the check-only commands:
- `npm run lint:ui-check` - Frontend validation without modifications
- `npm run lint:python-check` - Backend validation without modifications

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

Contains scripts for linting, formatting, and commitlint configuration.

### `commitlint.config.js`

Detailed commitlint rules and configuration.

### `.husky/`

Directory containing git hook scripts:

- `pre-commit`: Pre-commit validations (UI + Python linting)
- `commit-msg`: Commit message validation

### Frontend Configuration

- `.eslintrc.js` - ESLint configuration for JavaScript/HTML
- `.stylelintrc.js` - Stylelint configuration for CSS
- `.prettierrc.js` - Prettier formatting configuration

### Backend Configuration

- `pyproject.toml` - Python project configuration including:
  - `[tool.ruff]` - Ruff linter and formatter settings
  - `[tool.ruff.lint]` - Specific linting rules and configurations
  - `[tool.ruff.lint.isort]` - Import sorting configuration
  - `[tool.isort]` - Additional isort settings

---

## Best Practices

### Commit Messages
1. **Write clear descriptions**: Be specific about what changed
2. **Use appropriate types**: Choose the most accurate type
3. **Include scope when relevant**: Helps with organization
4. **Write body for complex changes**: Explain why, not just what
5. **Reference issues**: Use `Closes #123` or `Fixes #456`
6. **Keep commits atomic**: One logical change per commit

### Code Quality
7. **Run linting before committing**: Use `npm run lint:pre-commit` to check both frontend and backend
8. **Fix linting issues**: Address any issues reported by ESLint, Stylelint, or Ruff
9. **Maintain consistent formatting**: Let Prettier and Ruff handle code formatting automatically
10. **Organize imports properly**: isort will automatically organize Python imports according to PEP 8
11. **Follow Python conventions**: Ruff enforces PEP 8 and other Python best practices

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
