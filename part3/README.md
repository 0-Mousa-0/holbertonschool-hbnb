# Tasks-0: Application Factory & Configuration

In this task, the project structure was updated to follow the **Application Factory Pattern** for better scalability and environment management.

## Key Changes

| Feature                   | Description                                                                                                                             |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Dynamic Configuration** | Updated the `create_app()` function in `app/__init__.py` to accept a `config_class` parameter                                           |
| **Config Loading**        | Integrated `app.config.from_object(config_class)` to automatically load settings (like `DEBUG`, `SECRET_KEY`) from the `config.py` file |
| **Default Behavior**      | Set `config.DevelopmentConfig` as the default setting to ensure the app runs in development mode by default                             |
| **Clean Startup**         | Refactored `run.py` to use the factory instance, removing the need to manually pass `debug=True`                                        |

---

## Tasks-1: User Password Hashing

### Overview

Added secure password hashing to enhance API security using industry-standard practices.

### Implementation Details

- **Bcrypt Integration**: Added secure password hashing using `flask-bcrypt`
- **User Model**: Updated to include:
  - `hash_password` method
  - `verify_password` method
- **API Security**:
  - Modified `POST /api/v1/users/` to accept passwords
  - Passwords are strictly excluded from all `GET` responses via the serialization layer

### Code Example

```
python
# User model password methods
class User(BaseModel):
    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
```

**Diagram Title:** The Magical Project ER 🌳

**Description:**  
Imagine the project as a magical tree. Each `entity` is a leaf on this tree, and the branches show how they are connected. The diagram shows **how entities relate to each other** using familiar symbols:

**Shapes and Symbols in the Diagram:**  
- **Rectangle (`Entity`)**: Represents a main object or data type, like `User` or `Product`.  
- **Diamond (`Relationship`)**: Represents a connection between entities, like "writes" or "enrolls in".  
- **Oval (`Attribute`)**: Shows details about an entity, like `name`, `email`, or `price`.  
- **Lines with symbols**: Show the type of relationship:
  - **`1---*`** : One-to-Many. A single branch supports many leaves. Example: one `User` can write many `Posts`.  
  - **`*---*`** : Many-to-Many. Two branches share many leaves. Example: `Students` and `Courses` can link to many of each other.

This ER diagram gives you a **magical, visual view** of how data flows and relates in the project.
```mermaid
erDiagram
    %% 1. جدول المستخدمين (User)
    User {
        string id PK
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }

    %% 2. جدول العقارات (Place)
    Place {
        string id PK
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id FK
    }

    %% 3. جدول التقييمات (Review)
    Review {
        string id PK
        string text
        int rating
        string user_id FK
        string place_id FK
    }

    %% 4. جدول الخدمات (Amenity)
    Amenity {
        string id PK
        string name
    }

    %% 5. الجدول الوسيط لحل علاقة المتعدد-إلى-متعدد (Place_Amenity)
    Place_Amenity {
        string place_id FK
        string amenity_id FK
    }

    %% 6. تحدي الفهم الإضافي: جدول الحجوزات (Reservation)
    Reservation {
        string id PK
        string user_id FK
        string place_id FK
        date start_date
        date end_date
        string status
    }

    %% ==========================================
    %% رسم العلاقات (Relationships)
    %% ==========================================

    User ||--o{ Place : "owns (يمتلك)"
    User ||--o{ Review : "writes (يكتب)"
    Place ||--o{ Review : "has (يحتوي على)"

    %% ربط العقار والخدمات عبر الجدول الوسيط
    Place ||--o{ Place_Amenity : "includes (يتضمن)"
    Amenity ||--o{ Place_Amenity : "belongs_to (ينتمي إلى)"

    %% ربط تحدي الحجوزات
    User ||--o{ Reservation : "makes (يقوم بـ)"
    Place ||--o{ Reservation : "is_booked_via (يُحجز عبر)"
```
