#!/usr/bin/env bash
# Black-box API checks using cURL.
# Run the Flask app first: python3 run.py

set -u

BASE_URL="${BASE_URL:-http://127.0.0.1:5000/api/v1}"

request() {
  local method="$1"
  local path="$2"
  local payload="${3:-}"

  if [ -n "$payload" ]; then
    curl -s -X "$method" "$BASE_URL$path" \
      -H "Content-Type: application/json" \
      -d "$payload"
  else
    curl -s -X "$method" "$BASE_URL$path"
  fi
}

echo "1) Create user"
USER_BODY="$(request POST /users/ '{"first_name":"Curl","last_name":"Tester","email":"curl.tester@example.com"}')"
echo "$USER_BODY"
USER_ID="$(printf '%s' "$USER_BODY" | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')"

echo "2) Invalid user (bad email)"
request POST /users/ '{"first_name":"Bad","last_name":"Email","email":"bad-email"}'
echo

echo "3) Create amenity"
AMENITY_BODY="$(request POST /amenities/ '{"name":"Wi-Fi"}')"
echo "$AMENITY_BODY"
AMENITY_ID="$(printf '%s' "$AMENITY_BODY" | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')"

echo "4) Create place"
PLACE_BODY="$(request POST /places/ "{\"title\":\"Curl Place\",\"description\":\"CLI test\",\"price\":120,\"latitude\":10.1,\"longitude\":20.2,\"owner_id\":\"$USER_ID\",\"amenities\":[\"$AMENITY_ID\"]}")"
echo "$PLACE_BODY"
PLACE_ID="$(printf '%s' "$PLACE_BODY" | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')"

echo "5) Update place"
request PUT "/places/$PLACE_ID" '{"title":"Curl Place Updated","price":130}'
echo

echo "6) Create review"
REVIEW_BODY="$(request POST /reviews/ "{\"text\":\"Very good\",\"rating\":5,\"user_id\":\"$USER_ID\",\"place_id\":\"$PLACE_ID\"}")"
echo "$REVIEW_BODY"
REVIEW_ID="$(printf '%s' "$REVIEW_BODY" | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')"

echo "7) Get reviews by place"
request GET "/places/$PLACE_ID/reviews"
echo

echo "8) Invalid review update (rating out of range)"
request PUT "/reviews/$REVIEW_ID" '{"rating":0}'
echo

echo "9) Delete review and verify"
request DELETE "/reviews/$REVIEW_ID"
echo
request GET "/reviews/$REVIEW_ID"
echo
