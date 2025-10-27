from __future__ import annotations

import json
import os
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flask import Blueprint, jsonify

bp = Blueprint("docs", __name__)


def _fallback_spec() -> dict:
    """
    Fallback specification for the Raccoon Survey API.

    Returns:
        dict: Fallback specification for the Raccoon Survey API.
    """
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "Raccoon Survey API",
            "version": _resolve_version("1.12.12"),
            "description": "FallBack",
        },
        "servers": [{"url": "/api/v1"}],
        "paths": {
            "/auth/login": {
                "post": {
                    "tags": ["Auth"],
                    "summary": "Iniciar sesión",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["email", "password"],
                                    "properties": {
                                        "email": {"type": "string", "format": "email"},
                                        "password": {"type": "string"},
                                    },
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "Tokens generados"},
                        "400": {"description": "Email y contraseña requeridos"},
                        "401": {"description": "Credenciales inválidas"},
                        "403": {"description": "No autorizado"},
                        "404": {"description": "Usuario no encontrado"},
                    },
                }
            },
            "/auth/me": {
                "get": {
                    "tags": ["Auth"],
                    "summary": "Perfil del usuario",
                    "security": [{"bearerAuth": []}],
                    "responses": {
                        "200": {"description": "Perfil con id, role, team_id, name"}
                    },
                }
            },
        },
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        },
    }


_latest_version_cache: str | None = None
_latest_version_cache_ts: float = 0.0
_CACHE_TTL_SECONDS = 600  # 10 minutes


def _parse_semver(name: str) -> tuple[int, int, int]:
    """Parse a tag name into a SemVer-like tuple for sorting.

    Non-numeric parts are treated as zeros.

    Args:
        name (str): The tag name to parse.

    Returns:
        tuple[int, int, int]: A tuple of three integers representing the SemVer version.
    """
    s = name.strip().lstrip("vV")
    parts = s.replace("-", ".").split(".")
    nums: list[int] = []
    for p in parts[:3]:
        try:
            nums.append(int(p))
        except ValueError:
            nums.append(0)

    while len(nums) < 3:
        nums.append(0)

    return nums[0], nums[1], nums[2]


def _get_latest_github_tag(repo: str = "Javi-CD/raccoon-survey") -> str | None:
    """Fetch the latest tag name from GitHub.

    Tries to sort tags by SemVer and returns the highest.

    Args:
        repo (str, optional): The GitHub repository to fetch tags from. Defaults to "Javi-CD/raccoon-survey".

    Returns:
        str | None: The latest tag name, or None if not found or an error occurs.
    """
    url = f"https://api.github.com/repos/{repo}/tags"
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        req = Request(url, headers=headers, method="GET")  # noqa: S310
        with urlopen(req, timeout=3) as resp:  # noqa: S310
            body = resp.read()

        tags = json.loads(body.decode("utf-8"))
        if isinstance(tags, list) and tags:
            try:
                tags_sorted = sorted(
                    tags,
                    key=lambda t: _parse_semver(str(t.get("name", ""))),
                    reverse=True,
                )
                name = str(tags_sorted[0].get("name", "")).strip()
            except Exception:
                name = str(tags[0].get("name", "")).strip()

            return name or None

        return None
    except (URLError, HTTPError, TimeoutError, Exception):
        return None


def _resolve_version(current_version: str) -> str:
    """Resolve the API version using the latest GitHub tag, with cache/fallback.

    Args:
        current_version (str): The current version string.

    Returns:
        str: The resolved version string.
    """
    global _latest_version_cache, _latest_version_cache_ts
    now = time.time()

    if _latest_version_cache and (now - _latest_version_cache_ts) < _CACHE_TTL_SECONDS:
        return _latest_version_cache

    tag = _get_latest_github_tag()
    if tag:
        version = tag.lstrip("vV")
        _latest_version_cache = version
        _latest_version_cache_ts = now

        return version

    return current_version or "1.0.0"


@bp.get("/openapi.json")
def openapi_spec():
    """Serve the OpenAPI specification as JSON.

    Returns:
        JSON: The OpenAPI document.
    """
    try:
        spec_path = Path(__file__).resolve().parent.parent / "openapi.json"
        with spec_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        current_version = str(data.get("info", {}).get("version", ""))
        resolved_version = _resolve_version(current_version)
        data.setdefault("info", {})
        data["info"]["version"] = resolved_version

        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify(_fallback_spec()), 200
    except json.JSONDecodeError:
        return jsonify(_fallback_spec()), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
