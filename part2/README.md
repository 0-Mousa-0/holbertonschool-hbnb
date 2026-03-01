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
python -m unittest discover -s test_models -p "test_*.py"
python -m unittest discover -s tests -p "test_*.py"
```

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
