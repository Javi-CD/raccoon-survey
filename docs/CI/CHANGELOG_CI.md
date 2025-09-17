# Changelog CI Documentation

This document explains how the automatic changelog generation system works in the raccoon-survey project.

## 🚀 Quick Start

**Recommended approach for creating releases:**

1. Make your commits with conventional format
2. Go to GitHub Actions → "Create Release with Changelog"
3. Click "Run workflow" and enter version (e.g., `v1.0.1`)
4. The system handles everything automatically!

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

### 1. Workflow Activation

The CI can be triggered in **two ways**:

#### **Option 1: Manual Execution (Recommended)**
- Go to GitHub Actions → "Create Release with Changelog"
- Click "Run workflow" and specify the version
- **Advantages**: Full control, no conflicts, safer process

#### **Option 2: Automatic via Tag Push**
- Create and push a version tag (e.g., `v1.0.0`, `v1.2.3`)
- **Note**: Only creates/updates the GitHub Release (no commits)

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

### Method 1: Manual Release Creation (Recommended)

1. **Make commits following conventions:**

   ```bash
   git commit -m "feat: add user authentication system"
   git commit -m "fix: resolve login validation bug"
   git commit -m "docs: update API documentation"
   ```

2. **Execute workflow manually:**

   - Go to GitHub Actions in your repository
   - Select "Create Release with Changelog"
   - Click "Run workflow"
   - Specify the version (e.g., `v1.0.0`)

3. **The workflow automatically:**
   - Analyzes commits since the last tag
   - Categorizes changes
   - Updates CHANGELOG.md
   - Commits and pushes changes
   - Creates the version tag
   - Creates a GitHub Release

### Method 2: Automatic via Tag Push

1. **Create and push version tag:**

   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **The workflow automatically:**
   - Detects the tag push trigger
   - Analyzes commits since the previous tag
   - Checks if a GitHub Release already exists
   - Creates or updates the GitHub Release
   - **Note**: Does NOT commit changes (avoids conflicts)

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

### Manual Trigger vs Tag Push

| Aspect | Manual Trigger | Tag Push |
|--------|----------------|----------|
| **Changelog Update** | ✅ Updates CHANGELOG.md | ❌ No file changes |
| **Git Operations** | ✅ Commits and pushes | ❌ No commits/pushes |
| **Tag Creation** | ✅ Creates new tag | ❌ Tag already exists |
| **Release Creation** | ✅ Creates new release | ✅ Creates/updates release |
| **Conflict Risk** | ❌ No conflicts | ❌ No conflicts |
| **Use Case** | Complete release process | Quick release from existing tag |

### Smart Release Management

The workflow includes intelligent release handling:

- **Duplicate Prevention**: Checks if a release already exists
- **Update Capability**: Updates existing releases instead of failing
- **Conditional Logic**: Different behavior based on trigger type
- **Error Prevention**: Avoids git conflicts and permission issues

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

**For Manual Triggers:**
- Ensure you have the correct repository permissions
- Verify the workflow file exists in `.github/workflows/release.yml`
- Check that GitHub Actions is enabled for the repository

**For Tag Push Triggers:**
- Verify that the tag follows the `v*.*.*` format
- Make sure to push the tag: `git push origin --tags`
- Confirm the tag was created successfully: `git tag -l`

### Commits aren't categorized correctly

- Check that you're using the correct keywords or prefixes
- Verify the configuration in `changelog-config.yml`
- Review the commit message format in the documentation

### Release already exists errors

**This is now handled automatically!** The workflow:
- Checks if a release exists before creating
- Updates existing releases instead of failing
- Prevents duplicate release errors

### Permission errors

- Ensure GitHub Actions has write permissions
- Verify that `GITHUB_TOKEN` is available
- Check repository settings → Actions → General → Workflow permissions

### Git conflicts (Legacy Issue - Now Resolved)

The new workflow prevents git conflicts by:
- Using conditional logic based on trigger type
- Only committing changes on manual triggers
- Avoiding push operations when triggered by tag push

---

## System Benefits

1. **Complete automation**: No need to maintain the changelog manually
2. **Dual trigger modes**: Manual control or automatic tag-based execution
3. **Conflict prevention**: Smart logic prevents git conflicts and duplicate releases
4. **Consistency**: Uniform format following Keep a Changelog standards
5. **Traceability**: Each change is linked to specific commits with full history
6. **Intelligent release management**: Automatically handles existing releases
7. **Error resilience**: Robust error handling and recovery mechanisms
8. **Flexibility**: Customizable configuration according to project needs
9. **Safe operations**: Conditional logic ensures safe execution in all scenarios
