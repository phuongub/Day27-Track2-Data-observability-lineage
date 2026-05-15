# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a teaching lab for an Apache Airflow data-quality pipeline. Students build a DAG that validates sales order CSV data, writes a JSON summary, and sends Discord notifications. The lab runs locally without Airflow via a standalone script.

## Architecture

```
assignment/           — Student-facing materials
  lab_brief.py        — Assignment description and validation rules
  implementation_steps.py — Step-by-step checklist
  pseudocode.py       — Python-style pseudocode (close to reference implementation)
starter_project/      — The project students work on
  dags/
    sales_data_quality_pipeline.py — Airflow DAG skeleton (students fill in validate_orders_task)
  data/
    orders_failed.csv — Dataset intentionally failing validation
    orders_passed.csv — Clean dataset passing all rules
  expected/
    validation_summary_failed.json — Expected output for failing dataset
    validation_summary_passed.json — Expected output for passing dataset
  scripts/
    run_local_check.py — CLI to run validation logic without Airflow
  src/
    config.py          — Paths, valid statuses, webhook URL from env
    validation.py      — Core logic: CSV reading, validation, JSON writing, Discord notification
grading/
  rubric.md           — 10-point scoring rubric for instructors
```

### Key Design Points

- **Core validation lives in `src/validation.py`**, not in the DAG. The DAG's `validate_orders_task` is a thin wrapper that calls `run_lab_check()`.
- **No external dependencies** for the validation logic — uses only stdlib (`csv`, `json`, `os`, `urllib.request`). Airflow is an optional import guarded by `try/except`.
- **Discord webhook URL** comes from the `DISCORD_WEBHOOK_URL` env var. When empty, `send_discord_message` is a no-op.
- **`output/` is gitignored** — the `validation_summary.json` is generated at runtime and should not be committed.

## Commands

### Local validation (no Airflow required)

```bash
# Run against the passing dataset
python starter_project/scripts/run_local_check.py starter_project/data/orders_passed.csv --skip-discord

# Run against the failing dataset (expected to fail)
python starter_project/scripts/run_local_check.py starter_project/data/orders_failed.csv --allow-failure --skip-discord
```

### Verify generated output against expected

```bash
# After running against orders_failed.csv
python -c "import json; a=json.load(open('starter_project/output/validation_summary.json')); b=json.load(open('starter_project/expected/validation_summary_failed.json')); print('MATCH' if a==b else 'MISMATCH')"

# After running against orders_passed.csv
python -c "import json; a=json.load(open('starter_project/output/validation_summary.json')); b=json.load(open('starter_project/expected/validation_summary_passed.json')); print('MATCH' if a==b else 'MISMATCH')"
```
