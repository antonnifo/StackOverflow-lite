"""views for questions"""
from flask import jsonify, request
from flask_restful import Resource

from .models import QuestionModel
from app.api.validators import non_existance_question

class Questions(Resource):
    """docstring for Questions class"""

    def __init__(self):
        """initiliase the Questions class"""
        self.db = QuestionModel()

    def post(self):
        """docstring for saving a Question"""
        question_id = self.db.save()

        return jsonify({
            "status": 201,
            "data": {
                "id": question_id,
                "message": "Created a question record"
            }
        })
