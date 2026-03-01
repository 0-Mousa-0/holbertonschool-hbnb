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
