# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=False)
except Exception:  # noqa: S110
    pass

from src.core import create_app
from src.core.extensions.scheduler import start_scheduler

app = create_app()

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")  # noqa: S104
    port = int(os.getenv("PORT", "3000"))
    debug = bool(app.config.get("DEBUG", True))

    # Start BackgroundScheduler only once (avoid double-start with Flask reloader)
    start_scheduler(app, debug=debug)

    # Start server
    app.run(host=host, port=port, debug=debug, threaded=True)
