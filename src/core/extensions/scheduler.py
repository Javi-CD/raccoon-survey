# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

import atexit
import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from src.core.services import tokens_service


def create_scheduler(app: Flask) -> BackgroundScheduler:
    """Create BackgroundScheduler with registered jobs.

    Args:
        app (Flask): Flask application instance

    Returns:
        BackgroundScheduler: Configured scheduler instance
    """
    scheduler = BackgroundScheduler(timezone="UTC")

    def _run_cleanup():
        # Ensure Flask application context for DB operations
        with app.app_context():
            try:
                result = tokens_service.cleanup_expired_tokens(dry_run=False)
                app.logger.info(f"cleanup_expired_tokens ran: {result}")
            except Exception as e:
                app.logger.exception("cleanup_expired_tokens failed", exc_info=e)

    # Read schedule from config
    try:
        raw_hour = app.config.get("CLEANUP_CRON_HOUR", 3)
        raw_minute = app.config.get("CLEANUP_CRON_MINUTE", 0)
        hour = int(raw_hour)
        minute = int(raw_minute)
    except Exception:
        app.logger.warning(
            "Invalid CLEANUP_CRON_* values: hour=%r minute=%r; using defaults 3:00",
            raw_hour,
            raw_minute,
        )
        hour, minute = 3, 0

    if hour < 0 or hour > 23:
        app.logger.warning(
            "CLEANUP_CRON_HOUR out of range (%s). Clamping to 3.", hour
        )
        hour = 3
    if minute < 0 or minute > 59:
        app.logger.warning(
            "CLEANUP_CRON_MINUTE out of range (%s). Clamping to 0.", minute
        )
        minute = 0

    # Run daily at configured time
    scheduler.add_job(
        _run_cleanup,
        trigger="cron",
        hour=hour,
        minute=minute,
        id="cleanup_expired_tokens_daily",
        replace_existing=True,
        misfire_grace_time=3600,
    )

    return scheduler


def start_scheduler(app: Flask, debug: bool | None = None) -> None:
    """Start BackgroundScheduler safely, avoiding double-start under Flask reloader.

    Args:
        app (Flask): Flask application instance
        debug (Optional[bool]): Debug flag to infer reloader behavior
    """
    should_start = True
    if debug:
        # When reloader is enabled, only start in the subprocess where WERKZEUG_RUN_MAIN == "true"
        should_start = os.environ.get("WERKZEUG_RUN_MAIN") == "true"

    if not should_start:
        return

    scheduler = create_scheduler(app)
    scheduler.start()

    # Run cleanup immediately on startup (controlled by config)
    run_on_start = bool(app.config.get("CLEANUP_RUN_ON_START", True))
    if run_on_start:
        with app.app_context():
            try:
                result = tokens_service.cleanup_expired_tokens(dry_run=False)
                app.logger.info(f"cleanup_expired_tokens ran (startup): {result}")
            except Exception as e:
                app.logger.exception(
                    "cleanup_expired_tokens failed on startup", exc_info=e
                )

    # Gracefully shutdown scheduler on app exit
    atexit.register(lambda: scheduler.shutdown(wait=False))
