# Changelog CI Documentation

This document explains how the automatic changelog generation system works in the raccoon-survey project.

---

## File Structure

### `.github/workflows/`

- **`changelog.yml`**: Basic workflow for generating changelog
- **`release.yml`**: Advanced workflow for releases with automatic changelog

### `.github/changelog-config.yml`

Configuration file that defines:

- Commit patterns for each category
- Commits to ignore
- Date and version formats

---

## How It Works

### 1. Automatic Activation

The CI is triggered when:

- A version tag is created (e.g., `v1.0.0`, `v1.2.3`)
- Manually executed from GitHub Actions

### 2. Commit Categorization

Commits are automatically categorized according to these rules:

#### **Added** (New features)

- Keywords: `add`, `new`, `create`, `implement`, `introduce`, `feat`, `feature`
- Prefixes: `feat:`, `add:`, `new:`

#### **Changed** (Changes to existing features)

- Keywords: `update`, `change`, `modify`, `improve`, `refactor`, `enhance`
- Prefixes: `refactor:`, `update:`, `change:`, `improve:`

#### **Fixed** (Bug fixes)

- Keywords: `fix`, `bug`, `resolve`, `correct`, `patch`
- Prefixes: `fix:`, `bug:`, `patch:`

#### **Removed** (Removed features)

- Keywords: `remove`, `delete`, `drop`
- Prefixes: `remove:`, `delete:`

#### **Deprecated** (Deprecated features)

- Keywords: `deprecate`, `obsolete`
- Prefixes: `deprecate:`

#### **Security** (Security fixes)

- Keywords: `security`, `vulnerability`, `cve`, `exploit`
- Prefixes: `security:`

### 3. Ignored Commits

Commits with these patterns are automatically ignored:

- `chore:` - Maintenance tasks
- `docs:` - Documentation changes
- `style:` - Format/style changes
- `test:` - Add or modify tests
- `ci:` - CI/CD changes
- `build:` - Build changes
- Pull request and branch merges

---

## System Usage

### Create an Automatic Release

1. **Make commits following conventions:**

   ```bash
   git commit -m "feat: add user authentication system"
   git commit -m "fix: resolve login validation bug"
   git commit -m "docs: update API documentation"
   ```

2. **Create and push version tag:**

   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **The CI automatically:**
   - Analyzes commits since the last tag
   - Categorizes changes
   - Updates CHANGELOG.md
   - Creates a GitHub Release
   - Updates version links

### Manual Execution

You can also run the workflow manually:

1. Go to GitHub Actions in your repository
2. Select "Generate Changelog"
3. Click "Run workflow"
4. Specify the version (e.g., `v1.0.0`)

## Recommended Commit Conventions

For best results, use these formats:

```bash
# New features
feat: add user registration endpoint
add: implement password reset functionality

# Bug fixes
fix: resolve database connection timeout
bug: correct validation error messages

# Improvements
refactor: optimize database queries
improve: enhance error handling

# Removals
remove: delete deprecated API endpoints

# Security
security: fix SQL injection vulnerability
```

---

## Customization

### Modify Categories

Edit `.github/changelog-config.yml` to:

- Add new keywords
- Change commit prefixes
- Modify ignore patterns

### Change Date Format

Modify the `date_format` in the configuration:

```yaml
format:
  date_format: "%d/%m/%Y" # For DD/MM/YYYY format
```

---

## Generated Changelog Example

```markdown
## [1.0.0] - 2024-12-19

### Added

- feat: add user authentication system
- add: implement password reset functionality

### Fixed

- fix: resolve database connection timeout
- bug: correct validation error messages

### Changed

- refactor: optimize database queries
- improve: enhance error handling
```

---

## Troubleshooting

### Workflow doesn't execute

- Verify that the tag follows the `v*.*.*` format
- Make sure to push the tag: `git push origin --tags`

### Commits aren't categorized correctly

- Check that you're using the correct keywords or prefixes
- Verify the configuration in `changelog-config.yml`

### Permission errors

- Ensure GitHub Actions has write permissions
- Verify that `GITHUB_TOKEN` is available

---

## System Benefits

1. **Complete automation**: No need to maintain the changelog manually
2. **Consistency**: Uniform format following Keep a Changelog
3. **Traceability**: Each change is linked to specific commits
4. **Automatic releases**: GitHub releases are created automatically
5. **Flexibility**: Customizable configuration according to project needs
