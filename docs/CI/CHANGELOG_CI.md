# Changelog CI Documentation

This document explains how the automatic changelog generation and version synchronization system works in the raccoon-survey project.

---

## Quick Start

For the recommended release creation approach:

1. **Make conventional commits** following the patterns below
2. **Go to GitHub Actions** → "Create Release with Changelog"
3. **Run workflow manually** with your desired version (e.g., `v1.0.1`)
4. **The system automatically** updates CHANGELOG.md, synchronizes versions in all files, commits changes, creates tags, and publishes the release

---

## File Structure

### `.github/workflows/`

- **`changelog.yml`**: Basic workflow for generating changelog only
- **`release.yml`**: **Advanced workflow** for complete releases with automatic changelog and version synchronization

### `.github/scripts/`

- **`update_pyproject_version.py`**: Updates version in `pyproject.toml`
- **`update_package_version.py`**: Updates version in `package.json`
- **`update_package_lock.js`**: Updates version in `package-lock.json`

### `.github/changelog-config.yml`

Configuration file that defines:

- Commit patterns for each category
- Commits to ignore
- Date and version formats

---

## How It Works

### 1. Workflow Activation

The CI can be triggered in two ways:

#### **Manual Execution (Recommended)**
- Go to GitHub Actions → "Create Release with Changelog"
- Click "Run workflow" and specify version
- **Advantages**: Full control, version synchronization, conflict prevention

#### **Automatic via Tag Push**
- Create and push a version tag (e.g., `v1.0.0`)
- **Note**: Only creates/updates releases, doesn't commit changes to repository

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

### Manual Release Creation (Recommended)

1. **Make commits following conventions:**

   ```bash
   git commit -m "feat: add user authentication system"
   git commit -m "fix: resolve login validation bug"
   git commit -m "docs: update API documentation"
   ```

2. **Execute workflow manually:**

   - Go to GitHub Actions → "Create Release with Changelog"
   - Click "Run workflow"
   - Specify the version (e.g., `v1.0.1`)

3. **The workflow automatically:**
   - Analyzes commits since the last tag
   - Categorizes changes
   - Updates CHANGELOG.md
   - **Synchronizes versions** in `pyproject.toml`, `package.json`, `package-lock.json`
   - Commits all changes to the repository
   - Creates version tag
   - Creates GitHub Release with release notes

### Automatic Release via Tag Push

1. **Create and push version tag:**

   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **The workflow automatically:**
   - Analyzes commits and generates changelog
   - Creates or updates GitHub Release
   - **Note**: Does not commit changes to repository

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

## Workflow Behavior Differences

| Feature | Manual Trigger | Tag Push |
|---------|---------------|----------|
| **Changelog Generation** | Yes | Yes |
| **Version Synchronization** | Yes (`pyproject.toml`, `package.json`, `package-lock.json`) | No |
| **Repository Commits** | Yes (commits changes) | No |
| **Tag Creation** | Yes (creates tag) | Yes (uses existing tag) |
| **Release Creation** | Yes | Yes |
| **Conflict Prevention** | Yes (smart handling) | Limited |

### Smart Release Management

The workflow includes intelligent release handling:

- **Release Existence Check**: Automatically detects if a release already exists
- **Update vs Create**: Updates existing releases or creates new ones as needed
- **Conflict Prevention**: Avoids duplicate releases and handles edge cases gracefully

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

### Common Issues

1. **No commits found for changelog**
   - Ensure commits follow conventional format
   - Check if there are commits since the last tag

2. **Workflow doesn't trigger**
   - Verify tag format (must start with 'v')
   - Check workflow permissions

3. **Empty changelog**
   - Review commit messages
   - Check configuration patterns in `.github/changelog-config.yml`

4. **Version synchronization fails**
   - Ensure version format is valid (e.g., `v1.0.0`, not `1.0.0`)
   - Check if target files (`pyproject.toml`, `package.json`, `package-lock.json`) exist
   - Verify file permissions and repository access

5. **Commit step fails**
   - Check if there are actual changes to commit
   - Verify Git configuration and permissions
   - Ensure the workflow has write access to the repository

6. **Release already exists error**
   - The workflow automatically handles existing releases
   - If issues persist, manually delete the problematic release and re-run

### Workflow doesn't execute

- Verify that the tag follows the `v*.*.*` format
- Make sure to push the tag: `git push origin --tags`

### Commits aren't categorized correctly

- Check that you're using the correct keywords or prefixes
- Verify the configuration in `changelog-config.yml`

### Permission errors

- Ensure GitHub Actions has write permissions
- Verify that `GITHUB_TOKEN` is available

### Best Practices

- **Use manual workflow execution** for better control and version synchronization
- **Follow semantic versioning** (e.g., `v1.0.0`, `v1.2.3-beta.1`)
- **Make conventional commits** for better changelog categorization
- **Test version updates** in feature branches before main releases

---

## System Benefits

1. **Complete automation**: No need to maintain the changelog manually
2. **Consistency**: Uniform format following Keep a Changelog
3. **Traceability**: Each change is linked to specific commits
4. **Automatic releases**: GitHub releases are created automatically
5. **Flexibility**: Customizable configuration according to project needs
