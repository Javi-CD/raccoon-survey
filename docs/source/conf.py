from __future__ import annotations

from datetime import datetime
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# Project information
project = "Raccoon Survey"
author = "Raccoon Survey Team"
copyright = f"{datetime.now().year}, {author}"


# Version - try to read it from OpenAPI
def _read_release() -> str:
    try:
        with (ROOT / "src" / "core" / "openapi.json").open(encoding="utf-8") as f:
            data = json.load(f)
            return data.get("info", {}).get("version", "0.0.0")
    except Exception:
        return "0.0.0"


release = _read_release()

# Enabled extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",  # Google/Numpy style docstrings
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx.ext.ifconfig",
    "myst_parser",  # Markdown support (MyST)
]

# Flag to control if OpenAPI is available
has_openapi = False

try:
    import sphinxcontrib.openapi  # type: ignore # noqa: F401

    extensions.append("sphinxcontrib.openapi")
    has_openapi = True
except Exception:  # noqa: S110
    pass

# Common options
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Html Theme
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "sticky_navigation": True,
    "logo_only": True,
}
html_static_path = ["_static"]
html_logo = "_static/raccoon_survey_dark.svg"
html_favicon = "_static/raccoon_survey_white.svg"
html_css_files = [
    "custom.css",
]

# Parse both .rst and .md sources
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# MyST configuration
myst_heading_anchors = 3

# Autodoc / Autosummary
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# Napoleon Configuration (Google Style)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_attr_annotations = True

# Set up environment variables for documentation build
os.environ.setdefault("FLASK_ENV", "testing")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault(
    "SECRET_KEY",
    "DNEjDTSsxOxwawnYYiYIlSp6F8oNRSqTQ0XOiM-VCshhigcYBZk6dgMeGe_iHJx6rJSfiwEC-0xj48TmFZSy4w",
)
os.environ.setdefault(
    "JWT_SECRET_KEY",
    "qRbR8HKnEjsBPg-cZRjCYQSeHVZrY_PwZETIXguOp2AZLVSIr-Z5RzpMBWgk1vyWb2OS65oFu8O70fB08ELgAQ",
)
os.environ.setdefault("DEFAULT_USER_ADMIN_EMAIL", "admin@docs.local")
os.environ.setdefault("DEFAULT_USER_ADMIN_PASSWORD", "pass_doc_local")
os.environ.setdefault("DEFAULT_USER_ADMIN_NAME", "Docs Admin")
os.environ.setdefault("FLASK_DEBUG", "0")
os.environ.setdefault("CORS_ORIGINS", "*")


# Create a minimal Flask app context for documentation
def setup_app_context():
    """Setup a minimal Flask application context for Sphinx autodoc"""
    try:
        from src.core import create_app
        from src.core.database import db

        # Create app with minimal config for docs
        app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
                "SECRET_KEY": "DNEjDTSsxOxwawnYYiYIlSp6F8oNRSqTQ0XOiM-VCshhigcYBZk6dgMeGe_iHJx6rJSfiwEC-0xj48TmFZSy4w",
                "JWT_SECRET_KEY": "qRbR8HKnEjsBPg-cZRjCYQSeHVZrY_PwZETIXguOp2AZLVSIr-Z5RzpMBWgk1vyWb2OS65oFu8O70fB08ELgAQ",
                "WTF_CSRF_ENABLED": False,
            }
        )

        # Push application context
        ctx = app.app_context()
        ctx.push()

        # Create tables in memory
        with app.app_context():
            db.create_all()

        return app, ctx
    except Exception as e:
        print(f"Warning: Could not setup Flask app context: {e}")
        return None, None


# Setup the app context
_app, _ctx = setup_app_context()

# Minimal autodoc mock imports for packages that might not be available
autodoc_mock_imports = [
    "dotenv",
    "psycopg2",
    "redis",
    "flask",
    "flask_sqlalchemy",
    "flask_jwt_extended",
    "flask_cors",
    "sqlalchemy",
    "apscheduler",
]

todo_include_todos = True


def setup(app):
    app.add_config_value("has_openapi", has_openapi, "env")
