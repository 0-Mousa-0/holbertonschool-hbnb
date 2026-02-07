# HBnB Evolution

**HBnB Evolution** is a comprehensive software engineering project to build a simplified, full-stack AirBnB clone. The project is divided into four distinct phases, guiding the development from architectural design to a fully functional web application.

## 📂 Project Roadmap

The development is structured into four parts:

| Phase | Title | Status | Description |
| :--- | :--- | :--- | :--- |
| **Part 1** | **Technical Documentation & Design** | ✅ Completed | UML diagrams, architectural blueprints, and technical specifications. |
| **Part 2** | **Business Logic & API** | 🚧 Upcoming | Implementation of core models, the facade pattern, and the REST API. |
| **Part 3** | **Auth & Persistence** | ⏳ Upcoming | Integration of a SQL database and User Authentication (JWT). |
| **Part 4** | **Simple Web Client** | ⏳ Upcoming | Development of a front-end interface to interact with the API. |

---

## 🏗️ Part 1: Technical Documentation & Design

The goal of this phase was to design a robust, scalable architecture before writing code. We adopted a **Layered Architecture** using the **Facade Pattern** to separate concerns between the API, Business Logic, and Persistence layers.

### 📂 Directory: [`part1/`](./part1)

### Key Artifacts
1.  **High-Level Package Diagram:** illustrates the interaction between the Presentation (API), Business Logic (Facade), and Persistence layers.
2.  **Detailed Class Diagram:** Defines the data models (**User, Place, Review, Amenity**) and their relationships.
3.  **Sequence Diagrams:** Visualizes the flow of data for critical operations:
    * User Registration
    * Place Creation
    * Listing Places
    * Review Submission
4.  **Technical Document:** A compiled guide explaining the design decisions.

### Architecture Overview
The system is built on three main layers:
* **Presentation Layer:** Services and API endpoints (interacts only with the Facade).
* **Business Logic Layer:** Contains the `HBnBFacade` and entities (`User`, `Place`, etc.).
* **Persistence Layer:** Handles data storage (abstracted repositories).

### Domain Entities
* **User:** Attributes for profile management and authentication (Admin/Regular).
* **Place:** Properties listed by users, including location (lat/long) and amenities.
* **Review:** Ratings and comments linked to specific places and users.
* **Amenity:** Features associated with places (e.g., WiFi, Pool).

---

## 🚀 Part 2: Business Logic & API (Upcoming)

In this phase, we will translate the design from Part 1 into actual Python code.
* **Objective:** Implement the `HBnBFacade`, the entity classes, and the endpoints.
* **Tech Stack:** Python, Flask (likely), UUID generation.

---

## 🔐 Part 3: Authentication & Database (Upcoming)

* **Objective:** Replace in-memory/file storage with a real SQL Database and secure the API.
* **Key Features:** SQL Alchemy (ORM), JWT Authentication, Password Hashing.

---

## 🌐 Part 4: Simple Web Client (Upcoming)

* **Objective:** Create a user-friendly frontend.
* **Features:** Forms for login/registration, dynamic listings of places, and review submission forms.

---

## 🛠️ Repository Structure

```text
holbertonschool-hbnb/
├── part1/                  # Technical Documentation & UMLs
│   ├── High-Level_Package.jpeg
│   ├── Detailed_Class_Diagram.jpeg
│   ├── Sequence_*.jpeg
│   └── technical_documentation.md
├── part2/                  # Source code for Business Logic & API (Coming Soon)
├── part3/                  # Database & Auth integration (Coming Soon)
└── part4/                  # Frontend Web Client (Coming Soon)
```
## ✍️ Authors
* **Abdullah Manahi** 
* **Mohammed Alabdali** 
* **Mousa Alqarni** 
