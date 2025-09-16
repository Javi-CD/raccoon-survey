# Python Linting with Ruff and isort

This document describes the implementation of the Python code linting system
using Ruff and isort in the project.

---

## Tools Used

### Ruff

- **Purpose**: Extremely fast Python code linter and formatter
- **Features**:
  - Combines functionality from multiple tools (flake8, black, isort, etc.)
  - Written in Rust for maximum performance
  - Compatible with PEP 8 and other Python conventions
  - Automatic fixing of many issues

### isort

- **Purpose**: Automatic organization of Python imports
- **Features**:
  - Sorts imports alphabetically
  - Separates standard, third-party, and local imports
  - Compatible with PEP 8

---

## Configuration

### pyproject.toml

The configuration is located in `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py311"
include = ["*.py", "*.pyi", "**/pyproject.toml"]
exclude = [
    ".bzr", ".direnv", ".eggs", ".git", ".hg", ".mypy_cache",
    ".nox", ".pants.d", ".ruff_cache", ".svn", ".tox", ".venv",
    "__pypackages__", "_build", "buck-out", "build", "dist",
    "node_modules", "venv"
]
line-length = 88

[tool.ruff.lint]
# Enabled rules
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]

# Ignored rules
ignore = [
    "E501",  # line too long (handled by formatter)
    "B008",  # do not perform function calls in argument defaults
]

# Rules that can be auto-fixed
fixable = ["ALL"]
unfixable = []

# Regex for dummy variables
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports in __init__.py

[tool.ruff.lint.isort]
combine-as-imports = true
force-sort-within-sections = true
```

---

## Available Commands

### Manual Execution

```bash
# Complete Python linting (with automatic fixing)
npm run lint:python

# Check only (without automatic fixing)
npm run lint:python-check

# Individual commands
npm run lint:python-ruff        # Ruff with auto-fix
npm run lint:python-ruff-check  # Ruff check only
npm run lint:python-isort       # isort with auto-fix
npm run lint:python-isort-check # isort check only
npm run lint:python-format-check # Format verification
```

### Direct Execution with uv

```bash
# Ruff
uv run ruff check src/           # Check
uv run ruff check src/ --fix     # With automatic fixing
uv run ruff format src/          # Formatting
uv run ruff format --check src/  # Format verification

# isort
uv run isort src/                # Organize imports
uv run isort --check-only src/   # Check only
```

---

## Pre-commit Integration

The system runs automatically before each commit:

1. **Ruff check**: Analyzes code and applies automatic fixes
2. **isort**: Organizes imports automatically
3. **Ruff format**: Verifies that formatting is consistent

If there are errors that cannot be automatically fixed, the commit will be
rejected.

---

## Main Rules

### Ruff (Linting)

- **E/W**: pycodestyle errors and warnings
- **F**: pyflakes errors (unused variables, incorrect imports)
- **I**: Import organization (integrated with isort)
- **B**: Common bug detection (flake8-bugbear)
- **C4**: Comprehension improvements
- **UP**: Syntax updates for modern Python

### isort (Imports)

- Separation of imports into groups: standard, third-party, local
- Alphabetical ordering within each group
- Combination of imports from the same module
- Consistent formatting

---

## Correction Examples

### Before Linting

```python
import os
from myapp.models import User
import sys
from django.db import models
import json

def bad_function( x,y ):
    unused_var = "hello"
    if x==y:
        return True
    else:
        return False
```

### After Linting

```python
import json
import os
import sys

from django.db import models

from myapp.models import User


def bad_function(x, y):
    return x == y
```

---

## Troubleshooting

### Common Errors

#### Ruff not found

```bash
# Install dependencies
uv add --dev ruff isort
```

#### Configuration not applied

```bash
# Check configuration
uv run ruff check --show-settings
```

#### Format conflicts

```bash
# Apply formatting automatically
uv run ruff format src/
```

### Ignoring Specific Rules

```python
# Ignore specific rule on a line
import unused_module  # noqa: F401

# Ignore multiple rules
long_line = "this is a very long line that exceeds the limit"  # noqa: E501, B950
```

---

## Benefits

1. **Consistency**: Uniform code throughout the project
2. **Quality**: Automatic detection of errors and bad practices
3. **Productivity**: Automatic fixing of many issues
4. **Maintainability**: Code that's easier to read and maintain
5. **Collaboration**: Clear standards for the entire team

---

## Best Practices

1. **Run linting before commit**: `npm run lint:python`
2. **Fix errors immediately**: Don't accumulate linting issues
3. **Use auto-fix**: Take advantage of automatic corrections
4. **Review changes**: Verify that automatic corrections are correct
5. **Keep configuration updated**: Periodically review the rules

---

## IDE Integration

### VS Code

Install recommended extensions:

- **Ruff**: Real-time linting and formatting
- **Python**: Complete Python support

### Automatic configuration

The project includes VS Code configuration in `.vscode/settings.json`

---

## References

- [Official Ruff Documentation](https://docs.astral.sh/ruff/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Pre-commit hooks](https://pre-commit.com/)
