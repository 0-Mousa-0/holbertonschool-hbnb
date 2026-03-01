"""Review API endpoints."""

from flask_restx import Namespace, Resource, fields

from app.services import facade

api = Namespace('reviews', description='Review operations')

review_create_model = api.model(
    'ReviewCreate',
    {
        'text': fields.String(required=True, description='Text of the review'),
        'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
        'user_id': fields.String(required=True, description='ID of the user'),
        'place_id': fields.String(required=True, description='ID of the place'),
    },
)

review_update_model = api.model(
    'ReviewUpdate',
    {
        'text': fields.String(required=False, description='Text of the review'),
        'rating': fields.Integer(required=False, description='Rating of the place (1-5)'),
    },
)


def _serialize_review(review):
    return {
        'id': review.id,
        'text': review.text,
        'rating': review.rating,
        'user_id': review.user_id,
        'place_id': review.place_id,
        'created_at': review.created_at.isoformat(),
        'updated_at': review.updated_at.isoformat(),
    }


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_create_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            new_review = facade.create_review(api.payload)
            return _serialize_review(new_review), 201
        except ValueError as exc:
            return {'error': str(exc)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {'id': review.id, 'text': review.text, 'rating': review.rating}
            for review in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return _serialize_review(review), 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        try:
            updated_review = facade.update_review(review_id, api.payload)
            if not updated_review:
                return {'error': 'Review not found'}, 404
            return _serialize_review(updated_review), 200
        except ValueError as exc:
            return {'error': str(exc)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        if not facade.delete_review(review_id):
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200
