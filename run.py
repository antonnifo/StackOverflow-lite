import os
from app import create_app
from flask import jsonify

APP = create_app(os.getenv("FLASK_CONF") or 'default')

@APP.errorhandler(404)
def page_not_found(e):
    """error handler default method for error 404"""

    return jsonify(
            {"message": "Oops! not found, check you have "
             "the right url or correct input type", "status": 404}
        )
    