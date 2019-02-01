"""Views for posting questions"""
from flask import jsonify, request
from flask_restful import Resource

from app.api.v2.questions.models import QuestionsModel
from app.api.v2.token_decorator import require_token
from app.api.v2.users.models import UserModel
from app.api.v2.answers.models import AnswerModel
from app.api.v2.questions.models import QuestionsModel
from app.api.validators import non_existance_question


class Answers(Resource):
    """This class deals with posting answers to quizs"""

    def __init__(self):
        """
        executes when the class is being initiated
        used to assign values to object properties
        self parameter is a reference to tha class instance itself & is used 
        to access variables that belong to that class
        """
        self.db = AnswerModel()

    @require_token
    def post(current_user,self, question_id):
        """method for answering a question"""
        self.quiz = QuestionsModel().find_quiz_by_id(question_id)
        if self.quiz is None:
            return non_existance_question()

        answer = self.db.post_answer(
            current_user['user_id'], question_id)
        return jsonify({
            "status": 201,
            "data": answer
        })
