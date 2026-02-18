from flask_restx import Namespace, Resource
from app.services import facade


api = Namespace('The definition was created to be error-free.')


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # First check if the place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [{
            'id': r.id,
            'text': r.comment,
            'rating': r.rating
        } for r in reviews], 200
    