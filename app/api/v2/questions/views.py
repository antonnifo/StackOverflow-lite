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

    @require_token
    def get(current_user, self):
        """method for getting all the questions posted by users"""
        questions = self.db.find_all()
        return jsonify({
            "status": 200,
            "data": questions
        })        


class Question(Resource):
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
    def get(current_user,self, question_id):
        """method for getting a specific question and all its answers"""
        questions = self.db.find_quiz_answers(question_id)
        return jsonify({
            "status": 200,
            "data": questions
        })     