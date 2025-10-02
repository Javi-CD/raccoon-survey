import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=False)
except Exception:
    pass

from src.core import create_app

app = create_app()

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "3000"))
    debug = bool(app.config.get("DEBUG", True))

    # Start server
    app.run(host=host, port=port, debug=debug, threaded=True)
