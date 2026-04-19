from werkzeug.exceptions import NotFound, BadRequest, Conflict, UnprocessableEntity
from flask import jsonify, Blueprint, current_app

errors_bp = Blueprint("errrors", __name__)


@errors_bp.app_errorhandler(NotFound)
def not_found(e):
    return jsonify({
        "ERROR": str(e)
    }), 404


@errors_bp.app_errorhandler(BadRequest)
def bad_request(e):
    return jsonify({
        "ERROR": str(e)
    }), 400


@errors_bp.app_errorhandler(UnprocessableEntity)
def empty_strings(e):
    return jsonify({
        "ERROR": str(e)
    }), 422


@errors_bp.app_errorhandler(Exception)
def unexpected_error(e):
    current_app.logger.exception("Unhandled exception: %s", e)
    return jsonify({
        "ERROR": "500 Internal Server Error: an unexpected error occurred"
    }), 500