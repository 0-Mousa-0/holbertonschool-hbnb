# HBnB Evolution - Part 2

This directory contains **Part 2** of the HBnB project: business logic and REST API implementation.
The project is organized in layers (API, facade/service, models, persistence) to keep responsibilities clean and maintainable.

## Project Overview

Part 2 implements:

- Core entities: `User`, `Place`, `Review`, and `Amenity`
- A facade service (`HBnBFacade`) that orchestrates business operations
- In-memory repositories used by the facade
- Flask-RESTx API endpoints under `/api/v1/...`

## Requirements

- Python 3.10+ (recommended)
- `pip`

## Install Dependencies

From the `part2/` directory:

```bash
pip install -r requirements.txt
```

## Run the Application

From the `part2/` directory:

```bash
python run.py
```

Then open:

- API root: `http://127.0.0.1:5000/`
- Swagger UI: `http://127.0.0.1:5000/api/v1/`

## Run Tests

From the `part2/` directory:

```bash
python3 -m unittest discover -s test_models -p "test_*.py"
python3 -m unittest discover -s tests -p "test_*.py"
```

Additional manual HTTP checks:

```bash
./tests/curl_blackbox_tests.sh
```

Detailed results summary is documented in `tests/TESTING_REPORT.md`.

## Directory and File Structure

```text
part2/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── amenities.py
│   │       ├── places.py
│   │       └── reviews.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── amenity.py
│   │   ├── place.py
│   │   └── review.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── repository.py
│   └── services/
│       ├── __init__.py
│       └── facade.py
├── test_models/
├── tests/
├── run.py
├── config.py
├── requirements.txt
├── README.md
└── ISSUE_SOLUTIONS.md
```

### Purpose of Each Directory

- `app/`: Main application package.
- `app/api/`: Presentation layer with endpoint namespaces.
- `app/models/`: Business layer entities and validations.
- `app/persistence/`: Repository contract and in-memory implementation.
- `app/services/`: Facade that coordinates business operations.
- `test_models/`: Independent tests for model classes.
- `tests/`: API black-box/integration tests and reports.

### Purpose of Key Files

- `run.py`: Application entry point.
- `config.py`: Environment/application configuration.
- `requirements.txt`: Python dependencies.
- `app/__init__.py`: Flask app factory and namespace registration.
- `app/services/facade.py`: Business-operation gateway used by API routes.
- `app/persistence/repository.py`: Generic repository interface and in-memory storage.
- `ISSUE_SOLUTIONS.md`: Notes on mistakes found and solutions applied per task.

---
---
---
# Part 2 - Issue Solutions Log

This file records each graded situation (t0 to t6), the original mistake, and the implemented fix.
Each section is updated in the same commit as its corresponding code change.

## t0 - README and project setup documentation

### Mistake
- `part2/README.md` had a brief overview but it did not include clear dependency installation steps.
- It also missed explicit run commands and detailed per-directory/per-file purpose descriptions.

### Solution implemented
- Rewrote `part2/README.md` with:
  - explicit dependency installation command (`pip install -r requirements.txt`);
  - explicit run command (`python run.py`);
  - test commands;
  - detailed project structure and purpose notes for key directories/files.

## t1 - Core classes, inheritance, timestamps, and independent tests

### Mistake
- There was no shared base model using `id`, `created_at`, and `updated_at`.
- Entity classes did not consistently follow inheritance and expected method behavior (`save()` and `update(data)`).
- Existing tests were inconsistent with model constructor signatures and attribute names, so they did not validate the real implementation.

### Solution implemented
- Added `app/models/base_model.py` with:
  - UUID `id` as string;
  - `created_at` and `updated_at` timestamps;
  - `save()` and `update(data)` methods.
- Refactored `User`, `Place`, `Review`, and `Amenity` to inherit from `BaseModel`.
- Standardized business attributes to expected names and validations (`first_name`, `last_name`, `email`, `text`, `rating`, etc.).
- Added/reworked independent tests in `part2/test_models/` to verify:
  - valid instance creation;
  - validation failures for bad input;
  - relationship handling between `Place`, `Review`, and `Amenity`;
  - timestamp updates on `save()`/`update()`.

## t2 - User endpoint validation and error handling

### Mistake
- Invalid user input (for example an invalid email format) raised uncaught model exceptions and returned server errors instead of `400 Bad Request`.
- Update flow mixed attribute names and did not consistently validate/handle invalid payloads.

### Solution implemented
- Updated `app/api/v1/users.py` to:
  - use consistent payload/response keys (`first_name`, `last_name`, `email`);
  - catch `ValueError` from the business layer and return structured `400` responses;
  - keep `404` behavior for unknown `user_id` in `PUT /api/v1/users/<user_id>`.
- Updated user methods in `app/services/facade.py` to:
  - enforce email uniqueness in create/update;
  - route update changes through `user.update(...)` so model validations are applied consistently.

## t3 - Amenity invalid input handling

### Mistake
- Invalid amenity names (empty/invalid values) produced uncaught exceptions and inconsistent API responses instead of reliable `400 Bad Request`.
- Amenity update path did not consistently map validation errors to structured API responses.

### Solution implemented
- Updated `app/api/v1/amenities.py` to catch `ValueError` from create/update operations and return structured `400` responses.
- Kept `404` response behavior for unknown amenity IDs.
- Updated `app/services/facade.py` amenity update flow to use `amenity.update(...)`, ensuring model validations are always applied through one path.

## t4 - Place endpoint contract alignment and update behavior

### Mistake
- API payload contract and facade/model signatures were misaligned (`owner` vs `owner_id`, amenity IDs vs amenity objects).
- Place detail serialization referenced non-existent owner attributes and caused runtime errors.
- Place update flow depended on inconsistent update logic and did not reliably return updated data.

### Solution implemented
- Updated place creation/update business logic in `app/services/facade.py` to:
  - validate `owner_id` against existing users;
  - validate all amenity IDs and map them to amenity objects;
  - apply updates through model-level `place.update(...)` validation.
- Reworked `app/api/v1/places.py` to:
  - use correct payload fields (`owner_id`, amenities list of IDs);
  - serialize owner fields using correct attribute names (`first_name`, `last_name`);
  - return complete place data (including `id`, provided fields, and timestamps) for create and update;
  - return clean `400` responses on validation failures and `404` when place ID does not exist.

## t5 - Review API/facade integration and behavior fixes

### Mistake
- Facade created `Review` objects with payload keys that did not match the model constructor.
- Review serialization expected attributes that did not exist on the model.
- Route `GET /api/v1/places/<place_id>/reviews` was missing from the places namespace.
- Delete operation always returned a not-found outcome because repository delete had no boolean return contract.
- Update responses did not return updated review data, making verification difficult.

### Solution implemented
- Updated review business logic in `app/services/facade.py` to:
  - validate user/place existence with specific errors;
  - instantiate `Review` with correct arguments (`text`, `rating`, `place`, `user`);
  - keep place-review relationships synchronized on create/delete;
  - apply update through `review.update(...)` validation.
- Updated `app/persistence/repository.py` delete method to return `True` when deletion happens and `False` otherwise.
- Reworked `app/api/v1/reviews.py` to:
  - use consistent field names (`text`, `rating`, `user_id`, `place_id`);
  - return structured `400` errors for invalid input;
  - return full updated review data on `PUT`;
  - return proper `200`/`404` behavior on delete.
- Added `GET /api/v1/places/<place_id>/reviews` in `app/api/v1/places.py` with correct `200` and `404` handling.

## t6 - Black-box tests and testing report

### Mistake
- No dedicated black-box test suite existed for API endpoints.
- No detailed report documented successful vs edge/failure cases.

### Solution implemented
- Added automated API black-box tests in `part2/tests/test_api_blackbox.py`.
- Added reproducible cURL checks in `part2/tests/curl_blackbox_tests.sh`.
- Added a detailed testing report in `part2/tests/TESTING_REPORT.md` including:
  - executed commands;
  - coverage summary;
  - successful cases;
  - edge/failure cases and expected outcomes.
