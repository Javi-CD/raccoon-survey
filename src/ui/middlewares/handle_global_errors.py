from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request, url_for


def _is_api_request() -> bool:
    """Check if the current request is an API request.

    Returns:
        bool: True if the request is an API request, False otherwise.
    """
    try:
        path = request.path or ""
        if path.startswith("/api/"):
            return True
        accept = (request.headers.get("Accept") or "").lower()
        return "application/json" in accept and "text/html" not in accept
    except Exception:
        return False


def register_global_error_handlers(bp: Blueprint) -> None:
    """Register UI/API-aware error handlers on the provided blueprint.

    Args:
        bp (Blueprint): Flask blueprint to register error handlers on.
    """

    def ui_not_found(error: Exception):  # type: ignore[unused-ignore]
        """Handle not found errors.

        Args:
            error (Exception): The exception that was raised.

        Returns:
            tuple: A tuple containing the error response and status code.
        """
        if _is_api_request():
            return jsonify({"error": "Not Found", "code": 404}), 404

        return (
            render_template(
                "pages/public/error.html",
                code=404,
                title="Página no encontrada",
                message="No pudimos encontrar la página solicitada.",
                home_url=url_for("ui.home"),
                login_url=url_for("ui.login_page"),
            ),
            404,
        )

    def ui_unauthorized(error: Exception):  # type: ignore[unused-ignore]
        """Handle unauthorized errors.

        Args:
            error (Exception): The exception that was raised.

        Returns:
            tuple: A tuple containing the error response and status code.
        """
        if _is_api_request():
            return jsonify({"error": "Unauthorized", "code": 401}), 401

        return (
            render_template(
                "pages/public/error.html",
                code=401,
                title="Acceso no autorizado",
                message="Necesitas iniciar sesión para continuar.",
                home_url=url_for("ui.home"),
                login_url=url_for("ui.login_page"),
            ),
            401,
        )

    def ui_bad_request(error: Exception):  # type: ignore[unused-ignore]
        """Handle bad request errors.

        Args:
            error (Exception): The exception that was raised.

        Returns:
            tuple: A tuple containing the error response and status code.
        """
        if _is_api_request():
            return jsonify({"error": "Bad Request", "code": 400}), 400

        return (
            render_template(
                "pages/public/error.html",
                code=400,
                title="Solicitud incorrecta",
                message="La petición enviada no es válida.",
                home_url=url_for("ui.home"),
                login_url=url_for("ui.login_page"),
            ),
            400,
        )

    def ui_internal_error(error: Exception):  # type: ignore[unused-ignore]
        """Handle internal server errors.

        Args:
            error (Exception): The exception that was raised.

        Returns:
            tuple: A tuple containing the error response and status code.
        """
        if _is_api_request():
            return jsonify({"error": "Internal Server Error", "code": 500}), 500

        return (
            render_template(
                "pages/public/error.html",
                code=500,
                title="Error interno del servidor",
                message="Ha ocurrido un error inesperado. Intenta de nuevo más tarde.",
                home_url=url_for("ui.home"),
                login_url=url_for("ui.login_page"),
            ),
            500,
        )

    # Attach handlers to blueprint
    bp.register_error_handler(404, ui_not_found)
    bp.register_error_handler(401, ui_unauthorized)
    bp.register_error_handler(400, ui_bad_request)
    bp.register_error_handler(500, ui_internal_error)
