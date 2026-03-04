
# Import and register namespaces
from flask import Flask
from flask_restx import Api
from flask_restx.model import ModelBase
# Import Bcrypt extension
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
# Initialize Bcrypt instance

# implemented in task 5
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#---------------
bcrypt = Bcrypt()
# Initialize JWTManager
jwt = JWTManager()

_ORIGINAL_RESTX_MODEL_VALIDATE = ModelBase.validate


def _patch_restx_registry_compat():
    """Handle jsonschema/flask-restx registry argument mismatches safely."""
    if getattr(ModelBase.validate, "_registry_compat_patched", False):
        return

    def _validate_with_registry_fallback(self, data, resolver=None, format_checker=None):
        try:
            return _ORIGINAL_RESTX_MODEL_VALIDATE(
                self, data, resolver=resolver, format_checker=format_checker
            )
        except TypeError as exc:
            if "unexpected keyword argument 'registry'" not in str(exc):
                raise
            # Older jsonschema validators do not accept "registry"; retry without resolver.
            return _ORIGINAL_RESTX_MODEL_VALIDATE(
                self, data, resolver=None, format_checker=format_checker
            )

    _validate_with_registry_fallback._registry_compat_patched = True
    ModelBase.validate = _validate_with_registry_fallback


def create_app(config_class="config.DevelopmentConfig"):
    """
    Update the app factory to receive the settings object.
    """


    # 1 -------------------------
    app = Flask(__name__)
    # Loading settings from the passed object (e.g., DevelopmentConfig)
    app.config.from_object(config_class)
    # Setup Bcrypt with app version
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    _patch_restx_registry_compat()
    # 2 ----------------------------
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.auth import api as auth_ns
    # 3 ------------------------------------------
    # doc='/api/v1/' sets the Swagger UI location
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    # Register the users namespace
    # 4 -- This makes endpoints available at /api/v1/users/...
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    
    return app
