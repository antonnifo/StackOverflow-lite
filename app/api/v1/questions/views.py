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

        
class Question(Resource):
    """docstring of a single question"""

    def __init__(self):
        """initiliase the Redflag class"""
        self.db = QuestionModel()

    def get(self, question_id):
        """docstring for getting a specific question"""
        question = self.db.find(question_id)
        if question == "question does not exist":
               return non_existance_question()
       
        return jsonify({
            "status": 200,
            "data": question
        })

    def delete(self, question_id):
        """docstring for deleting a question"""
        question = self.db.find(question_id)
        if question == "question does not exist":
            return non_existance_question()
        delete_status = self.db.delete(question)
        if delete_status == "deleted":
            return jsonify({
                "status": 200,
                "message": 'question record has been deleted'
            })
