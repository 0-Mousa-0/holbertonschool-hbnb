"""User API endpoints."""

from flask_restx import Namespace, Resource, fields

from app.services import facade

api = Namespace('users', description='User operations')

user_create_model = api.model(
    'UserCreate',
    {
        'first_name': fields.String(required=True, description='First name of the user'),
        'last_name': fields.String(required=True, description='Last name of the user'),
        'email': fields.String(required=True, description='Email of the user'),
        'is_admin': fields.Boolean(required=False, description='Admin flag'),
    },
)

user_update_model = api.model(
    'UserUpdate',
    {
        'first_name': fields.String(required=False, description='First name of the user'),
        'last_name': fields.String(required=False, description='Last name of the user'),
        'email': fields.String(required=False, description='Email of the user'),
        'is_admin': fields.Boolean(required=False, description='Admin flag'),
    },
)


def _serialize_user(user):
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_admin': user.is_admin,
    }


@api.route('/')
class UserList(Resource):
    @api.expect(user_create_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        try:
            new_user = facade.create_user(api.payload)
            return _serialize_user(new_user), 201
        except ValueError as exc:
            # Convert model/facade validation errors into API-friendly 400 responses.
            return {'error': str(exc)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [_serialize_user(user) for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return _serialize_user(user), 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user information"""
        try:
            updated_user = facade.update_user(user_id, api.payload)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return _serialize_user(updated_user), 200
        except ValueError as exc:
            return {'error': str(exc)}, 400
