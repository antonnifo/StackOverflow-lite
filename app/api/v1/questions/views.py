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

    def get(self):
        """docstring for getting all the questions posted"""
        data = self.db.get_all()
        if data is None:
            return jsonify({
                "status" : 200,
                "message" : "There are no questions at the moment"
        })

        return jsonify({
            "status": 200,
            "data": self.db.get_all()
        })
