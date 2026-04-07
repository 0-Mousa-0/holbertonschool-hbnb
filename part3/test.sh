#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_PATH="${ROOT_DIR}/instance/hbnb_sql_scripts.db"
HTTP_DB_PATH="${ROOT_DIR}/instance/hbnb_http_smoke.db"
HTTP_HOST="127.0.0.1"
HTTP_PORT="5055"
SERVER_LOG="${ROOT_DIR}/instance/test_server.log"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Python interpreter not found (python3/python)." >&2
  exit 1
fi

echo "--- HBnB Part 3 Test ---"

echo "==> Running relationship unit tests"
"${PYTHON_BIN}" -m unittest discover -s tests -v

echo "==> Executing SQL schema + seed + CRUD checks"
"${PYTHON_BIN}" - <<'PY'
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

admin = conn.execute(
    "SELECT email, is_admin, password FROM users WHERE id = ?",
    ("00000000-0000-0000-0000-000000000001",),
).fetchone()
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

echo "==> Running API smoke checks (without login)"
"${PYTHON_BIN}" - <<'PY'
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review


class TestConfig:
    SECRET_KEY = "test-secret"
    JWT_SECRET_KEY = "test-jwt-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True


app = create_app(TestConfig)

with app.app_context():
    db.create_all()
    owner = User(
        first_name="Admin",
        last_name="User",
        email="admin@hbnb.io",
        password="admin1234",
        is_admin=True,
    )
    reviewer = User(
        first_name="Reviewer",
        last_name="User",
        email="reviewer@hbnb.io",
        password="review1234",
        is_admin=False,
    )
    wifi = Amenity(name="WiFi")
    db.session.add_all([owner, reviewer, wifi])
    db.session.flush()

    place = Place(
        title="Smoke Place",
        description="No login flow",
        price=100.0,
        latitude=10.0,
        longitude=20.0,
        owner_id=owner.id,
    )
    place.amenities.append(wifi)
    db.session.add(place)
    db.session.flush()

    review = Review(text="Nice", rating=5, user_id=reviewer.id, place_id=place.id)
    db.session.add(review)
    db.session.commit()

client = app.test_client()
places = client.get("/api/v1/places/")
assert places.status_code == 200, "GET /places failed"
payload_list = places.get_json()
assert isinstance(payload_list, list) and len(payload_list) >= 1, "No places returned"
place_id = payload_list[0]["id"]

place_details = client.get(f"/api/v1/places/{place_id}")
assert place_details.status_code == 200, "GET /places/<id> failed"
payload = place_details.get_json()
assert len(payload.get("amenities", [])) >= 1, "Place amenities missing"
assert len(payload.get("reviews", [])) >= 1, "Place reviews missing"

print("API no-login smoke checks passed.")
PY

echo "==> All checks passed (unit + SQL + API no-login)"