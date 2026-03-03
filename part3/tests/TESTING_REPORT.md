# Part 2 API Testing Report

Date: 2026-03-01  
Scope: Black-box validation of `/api/v1/users`, `/api/v1/amenities`, `/api/v1/places`, and `/api/v1/reviews`.

## 1) Test Strategy

Two complementary black-box approaches were used:

1. **Automated API tests** using Flask test client (`tests/test_api_blackbox.py`)
2. **HTTP-level cURL checks** (`tests/curl_blackbox_tests.sh` + temporary local server execution)

This validates both expected success paths and edge/error behavior (`400`, `404`).

## 2) Commands Executed

From `part2/`:

```bash
python3 -m unittest discover -s test_models -p "test_*.py"
python3 -m unittest discover -s tests -p "test_*.py"
```

Results:

- `test_models`: **24 tests passed**
- `tests` (API black-box): **10 tests passed**

## 3) Automated Black-Box Coverage Summary

Covered scenarios in `tests/test_api_blackbox.py`:

- User
  - create + retrieve by ID
  - invalid user input returns `400`
  - update with unknown user ID returns `404`
- Amenity
  - invalid name returns `400`
- Place
  - create with valid owner + amenities
  - update existing place returns updated data and changed `updated_at`
  - update unknown place returns `404`
  - create with invalid owner returns `400`
- Review
  - create/get/update/delete lifecycle
  - `GET /places/<place_id>/reviews`
  - invalid rating returns `400`
  - unknown place for reviews returns `404`

## 4) cURL Black-Box Execution (Representative Cases)

The following representative HTTP checks were executed successfully:

- `POST /api/v1/users/` valid payload -> `201`
- `POST /api/v1/users/` invalid email -> `400`
- `POST /api/v1/amenities/` valid payload -> `201`
- `POST /api/v1/places/` valid owner/amenities -> `201`
- `PUT /api/v1/places/<id>` valid update -> `200`
- `POST /api/v1/reviews/` valid payload -> `201`
- `GET /api/v1/places/<id>/reviews` -> `200`
- `PUT /api/v1/reviews/<id>` invalid rating -> `400`
- `DELETE /api/v1/reviews/<id>` -> `200`
- `GET /api/v1/reviews/<id>` after delete -> `404`

The reusable script for manual reruns is:

```bash
./tests/curl_blackbox_tests.sh
```

## 5) Successful Cases and Edge Cases

### Successful cases

- Resource creation returns expected IDs and payload fields.
- Update endpoints return updated resource data (including timestamp updates where relevant).
- Review deletion removes the resource and subsequent retrieval returns `404`.

### Edge cases handled correctly

- Invalid email format and empty user names -> `400`.
- Invalid amenity name -> `400`.
- Invalid place owner reference -> `400`.
- Invalid review rating (outside 1-5) -> `400`.
- Unknown IDs for user/place/review retrieval or update -> `404` where required.

## 6) Conclusion

Black-box tests now exist and were executed.
The report includes both passing scenarios and failure/edge scenarios, with expected and observed behavior aligned to the Part 2 requirements.
