#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_PATH="${ROOT_DIR}/instance/hbnb_sql_scripts.db"

echo "==> Running relationship unit tests"
python -m unittest discover -s tests -v

echo "==> Executing SQL schema + seed + CRUD checks"
python - <<'PY'
import sqlite3
from pathlib import Path

root = Path.cwd()
db_path = root / "instance" / "hbnb_sql_scripts.db"
db_path.parent.mkdir(exist_ok=True)

if db_path.exists():
    db_path.unlink()

conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys = ON;")

for script_name in ["create_tables.sql", "seed_data.sql", "crud_checks.sql"]:
    script = (root / "sql" / script_name).read_text(encoding="utf-8")
    conn.executescript(script)

admin = conn.execute("SELECT email, is_admin, password FROM users WHERE id = ?", ("00000000-0000-0000-0000-000000000001",)).fetchone()
amenities = conn.execute("SELECT name FROM amenities ORDER BY name").fetchall()

assert admin is not None, "Admin user not found"
assert admin[0] == "admin@hbnb.io", "Unexpected admin email"
assert admin[1] == 1, "Admin flag is not TRUE"
assert admin[2] != "admin1234", "Admin password is stored in plain text"
assert admin[2].startswith("$2"), "Admin password is not a bcrypt hash"

amenity_names = [row[0] for row in amenities]
for name in ["Air Conditioning", "Swimming Pool", "WiFi"]:
    assert name in amenity_names, f"{name} was not seeded"

conn.close()
print("SQL checks passed.")
PY

echo "==> All checks passed"
