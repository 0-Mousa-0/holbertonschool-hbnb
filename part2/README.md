# HBnB Evolution - Part 2: Business Logic & API Implementation

This repository contains the second phase of the HBnB project. In this stage, the focus shifts from architectural design to implementing the **Business Logic Layer** and the **API Layer** using Python and Flask-RESTx.

## 📌 Project Overview
The objective of Part 2 is to create a functional RESTful API that handles core entities (Users, Places, Reviews, and Amenities) while following the **Facade Pattern** to maintain a strict separation of concerns between the user interface (API) and the underlying data logic.



---

## 🛠️ Project Structure

```text
part2/
├── app/
│   ├── __init__.py          # Flask app initialization & API configuration
│   ├── api/                 # API Layer
│   │   └── v1/              # Version 1 of the API (Namespaces & Routes)
│   ├── models/              # Business Logic Layer (Entity Classes)
│   ├── persistence/         # Data Access Layer (Repository Pattern)
│   └── services/            # Facade Pattern (Orchestrator)
├── tests/                   # Unit Testing Suite
├── run.py                   # Application Entry Point
├── requirements.txt         # Project Dependencies
└── README.md                # Documentation
