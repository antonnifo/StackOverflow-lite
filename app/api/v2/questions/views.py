"""Views for posting questions"""
from flask import jsonify, request
from flask_restful import Resource

from app.api.v2.questions.models import QuestionsModel
from app.api.v2.token_decorator import require_token
from app.api.v2.users.models import UserModel


class Questions(Resource):
    """This class deals with posting and reading questions"""

    def __init__(self):
        """
        executes when the class is being initiated
        used to assign values to object properties
        self parameter is a reference to tha class instance itself & is used 
        to access variables that belong to that class
        """
        self.db = QuestionsModel()

    @require_token
    def post(current_user, self):
        """method for posting a question"""
        question = self.db.save(
            current_user['user_id'])
        return jsonify({
            "status": 201,
            "data": question,
            "message": "Created a question"
        })
