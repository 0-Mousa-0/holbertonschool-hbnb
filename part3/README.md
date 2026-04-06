# HBnB - Part 3

This directory contains the Flask REST API for the HBnB project, including authentication, SQLAlchemy models, repository/facade layers, and SQL scripts for schema generation and seed data.

## What is implemented

- Application factory with `Flask`, `Flask-RESTX`, `Flask-SQLAlchemy`, `Flask-JWT-Extended`, and `Flask-Bcrypt`
- Persistent SQLAlchemy entities:
  - `User`
  - `Place`
  - `Review`
  - `Amenity`
- Bidirectional relationships:
  - One-to-many: `User -> Place`, `User -> Review`, `Place -> Review`
  - Many-to-many: `Place <-> Amenity` through `place_amenity`
- Relationship validation tests in `tests/test_relationships.py`
- Raw SQL scripts for Task 9 in `sql/`

## Relationship mapping (Task 8)

The ORM mapping now uses consistent `back_populates` definitions on both sides:

- `User.places` <-> `Place.owner`
- `User.reviews` <-> `Review.user`
- `Place.reviews` <-> `Review.place`
- `Place.amenities` <-> `Amenity.places` through `place_amenity`

This fixes inconsistent `backref/back_populates` usage and ensures relationship loading, persistence, and traversal work correctly.

## SQL scripts (Task 9)

The following files are available:

- `sql/create_tables.sql`  
  Creates `users`, `places`, `reviews`, `amenities`, and `place_amenity` with constraints, foreign keys, and checks.

- `sql/seed_data.sql`  
  Inserts:
  - Admin user with fixed id: `00000000-0000-0000-0000-000000000001`
  - Bcrypt-hashed password for `admin1234`
  - Initial amenities: `WiFi`, `Swimming Pool`, `Air Conditioning` with generated UUID-like ids

- `sql/crud_checks.sql`  
  Runs sample `INSERT`, `SELECT`, `UPDATE`, and `DELETE` queries to verify integrity and relationship constraints.

## Quick start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the API:

```bash
python run.py
```

## Testing

Use the project test runner:

```bash
bash test.sh
```

### `test.sh` brief

`test.sh` is a single verification script that:

1. Runs Python relationship tests (`tests/test_relationships.py`)
2. Builds a fresh SQLite DB from raw SQL scripts
3. Seeds admin + amenities
4. Executes CRUD checks
5. Verifies admin password is hashed (not plain text) and seeded amenities exist