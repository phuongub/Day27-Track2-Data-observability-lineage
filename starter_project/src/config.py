from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load .env file into process environment if present (stdlib equivalent of python-dotenv)
_env_path = PROJECT_ROOT / ".env"
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            if not os.environ.get(key):
                os.environ[key] = value

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

PASSED_DATASET = DATA_DIR / "orders_passed.csv"
FAILED_DATASET = DATA_DIR / "orders_failed.csv"
SUMMARY_FILE = OUTPUT_DIR / "validation_summary.json"

VALID_STATUSES = {"completed", "pending", "cancelled"}

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
AIRFLOW_INPUT_FILE = os.getenv("AIRFLOW_INPUT_FILE", str(PASSED_DATASET))
