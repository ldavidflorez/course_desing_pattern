from functools import wraps
from flask import request, jsonify, current_app
from dependency_injector.wiring import inject, Provide
from di_container import Container


def token_required(f):
    """Decorator that checks for valid authorization token."""
    @wraps(f)
    @inject
    def wrapper(auth_context: object = Provide[Container.auth_context], *args, **kwargs):
        # Skip authentication in testing mode
        if current_app.config.get('TESTING', False):
            return f(*args, **kwargs)

        token = request.headers.get("Authorization")
        if not auth_context.authenticate(token):
            return jsonify({"message": "Unauthorized invalid token"}), 401
        return f(*args, **kwargs)
    return wrapper