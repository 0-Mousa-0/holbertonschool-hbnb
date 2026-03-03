"""User API endpoints."""

from flask_restx import Namespace, Resource, fields

from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

user_create_model = api.model(
    'UserCreate',
    {
        'first_name': fields.String(required=True, description='First name of the user'),
        'last_name': fields.String(required=True, description='Last name of the user'),
        'email': fields.String(required=True, description='Email of the user'),
        # Required for secure registration (handled via bcrypt hashing)
        'password': fields.String(required=True, description='Password of the user'),
        'is_admin': fields.Boolean(required=False, description='Admin flag'),
    },
)

user_update_model = api.model(
    'UserUpdate',
    {
        'first_name': fields.String(required=False, description='First name of the user'),
        'last_name': fields.String(required=False, description='Last name of the user'),
        # Note: email and password are removed from update model per requirements
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
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """Update user information"""
        try:
            current_user_id = get_jwt_identity()

            # 1. Ownership Validation: Check if user is updating their own profile
            if user_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            data = api.payload

            # 2. Block modification of email or password
            if 'email' in data or 'password' in data:
                return {'error': 'You cannot modify email or password'}, 400

            updated_user = facade.update_user(user_id, api.payload)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return _serialize_user(updated_user), 200
        except ValueError as exc:
            return {'error': str(exc)}, 400
