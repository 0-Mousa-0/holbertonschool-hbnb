# Importing required modules from flask_restx and the service facade layer
from flask_restx import Namespace, Resource, fields
from app.services import facade

# Defining the API namespace for 'users' with a description
api = Namespace('users', description='User operations')

# Defining the data model for User validation and documentation
user_model = api.model('User', {
    'firstName': fields.String(required=True, description='First name of the user'),
    'lastName': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

# Resource class for handling the collection of users (List/Create)


@api.route('/')
class UserList(Resource):
    # GET endpoint to retrieve all users
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        # Fetch all users from the service layer
        users = facade.get_all_users()
        # Map user objects to a list of dictionaries for JSON response
        return [
            {
                'id': u.id,
                'firstName': u.firstName,
                'lastName': u.lastName,
                'email': u.email
            } for u in users
        ], 200

    # POST endpoint to create a new user
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input')
    def post(self):
        """Register a new user"""
        # Get the JSON payload from the request
        user_data = api.payload

        # Check if a user with the provided email already exists
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Create user via Facade (Ensure your Facade handles the missing fields like admin/password)
        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'firstName': new_user.firstName,
            'lastName': new_user.lastName,
            'email': new_user.email
        }, 201

# Resource class for handling individual user operations (Get/Update by ID)


@api.route('/<user_id>')
class UserResource(Resource):
    # GET endpoint to retrieve a specific user by ID
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        # Fetch user from the service layer using the ID
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email
        }, 200

    # PUT endpoint to update an existing user
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user information"""
        # Get the updated data from the request payload
        user_data = api.payload

        # Update user via Facade logic
        updated_user = facade.update_user(user_id, user_data)

        if not updated_user:
            return {'error': 'User not found'}, 404

        return {
            'id': updated_user.id,
            'firstName': updated_user.firstName,
            'lastName': updated_user.lastName,
            'email': updated_user.email
        }, 200
