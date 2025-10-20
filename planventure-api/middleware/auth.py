from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User

def auth_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def get_current_user():
    """Get current authenticated user from JWT token."""
    user_id = get_jwt_identity()
    return User.query.get(user_id)
