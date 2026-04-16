from werkzeug.exceptions import NotFound, BadRequest, Conflict, UnprocessableEntity
from flask import jsonify, Blueprint, current_app

# Blueprint that keeps API errors returning JSON instead of HTML.
errors_bp = Blueprint("errrors", __name__)


@errors_bp.app_errorhandler(NotFound)
def not_found(e):
    # Missing resources return a simple JSON error payload.
    return jsonify({
        "ERROR": str(e)
    }), 404


@errors_bp.app_errorhandler(BadRequest)
def bad_request(e):
    # Validation and malformed request errors land here.
    return jsonify({
        "ERROR": str(e)
    }), 400


@errors_bp.app_errorhandler(UnprocessableEntity)
def empty_strings(e):
    # Used when the request shape is valid but the value itself is unusable.
    return jsonify({
        "ERROR": str(e)
    }), 422


@errors_bp.app_errorhandler(Exception)
def unexpected_error(e):
    # Log unexpected failures and keep the response JSON-based for clients.
    current_app.logger.exception("Unhandled exception: %s", e)
    return jsonify({
        "ERROR": "500 Internal Server Error: an unexpected error occurred"
    }), 500