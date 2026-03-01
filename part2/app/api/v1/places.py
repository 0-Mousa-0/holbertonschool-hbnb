"""Place API endpoints."""

from flask_restx import Namespace, Resource, fields

from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model(
    'PlaceAmenity',
    {
        'id': fields.String(description='Amenity ID'),
        'name': fields.String(description='Name of the amenity'),
    },
)

user_model = api.model(
    'PlaceUser',
    {
        'id': fields.String(description='User ID'),
        'first_name': fields.String(description='First name of the owner'),
        'last_name': fields.String(description='Last name of the owner'),
        'email': fields.String(description='Email of the owner'),
    },
)

review_model = api.model(
    'PlaceReview',
    {
        'id': fields.String(description='Review ID'),
        'text': fields.String(description='Review text'),
        'rating': fields.Integer(description='Review rating'),
        'user_id': fields.String(description='Review author user ID'),
    },
)

place_create_model = api.model(
    'PlaceCreate',
    {
        'title': fields.String(required=True, description='Title of the place'),
        'description': fields.String(required=False, description='Description of the place'),
        'price': fields.Float(required=True, description='Price per night'),
        'latitude': fields.Float(required=True, description='Latitude (-90 to 90)'),
        'longitude': fields.Float(required=True, description='Longitude (-180 to 180)'),
        'owner_id': fields.String(required=True, description='ID of the owner'),
        'amenities': fields.List(fields.String, required=False, description="List of amenity IDs"),
    },
)

place_update_model = api.model(
    'PlaceUpdate',
    {
        'title': fields.String(required=False, description='Title of the place'),
        'description': fields.String(required=False, description='Description of the place'),
        'price': fields.Float(required=False, description='Price per night'),
        'latitude': fields.Float(required=False, description='Latitude (-90 to 90)'),
        'longitude': fields.Float(required=False, description='Longitude (-180 to 180)'),
    },
)


def _serialize_place_summary(place):
    return {
        'id': place.id,
        'title': place.title,
        'latitude': place.latitude,
        'longitude': place.longitude,
    }


def _serialize_place(place):
    return {
        'id': place.id,
        'title': place.title,
        'description': place.description,
        'price': place.price,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'owner_id': place.owner_id,
        'owner': {
            'id': place.owner.id,
            'first_name': place.owner.first_name,
            'last_name': place.owner.last_name,
            'email': place.owner.email,
        },
        'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in place.amenities],
        'reviews': [
            {'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user_id}
            for review in place.reviews
        ],
        'created_at': place.created_at.isoformat(),
        'updated_at': place.updated_at.isoformat(),
    }


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_create_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        try:
            new_place = facade.create_place(api.payload)
            return _serialize_place(new_place), 201
        except ValueError as exc:
            return {'error': str(exc)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve all places (summary)"""
        places = facade.get_all_places()
        return [_serialize_place_summary(place) for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details including owner and amenities"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return _serialize_place(place), 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        try:
            updated_place = facade.update_place(place_id, api.payload)
            if not updated_place:
                return {'error': 'Place not found'}, 404
            return _serialize_place(updated_place), 200
        except ValueError as exc:
            return {'error': str(exc)}, 400

