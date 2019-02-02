"""Views for posting questions"""
from flask import jsonify, request
from flask_restful import Resource

from app.api.v2.token_decorator import require_token
from app.api.v2.users.models import UserModel
from app.api.v2.answers.models import AnswerModel
from app.api.v2.questions.models import QuestionsModel
from app.api.validators import non_existance_question, only_creater_can_edit


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

class UpdateAnswer(Resource):
    """view class for updating an answer"""

    def __init__(self):
        """
        executes when the class is being initiated
        used to assign values to object properties
        self parameter is a reference to tha class instance itself & is used 
        to access variables that belong to that class
        """
        self.db = QuestionsModel()

    @require_token
    def patch(current_user, self, answer_id):
        """method to update an answer"""
        answer = self.db.find_answer_by_id(
            answer_id)
        if answer is None:
            return non_existance_question()

        if current_user["user_id"] != answer['user_id']:
            return only_creater_can_edit()

        edit_status = self.db.update_answer(
            answer_id)

        if edit_status == "answer updated":
            return jsonify({
                "status": 200,
                "data": {
                    "id": answer_id,
                    "message": "Updated your answer"
                }
            })


class AcceptAnswer(Resource):
    """view class for accepting an answer"""

    def __init__(self):
        """
        executes when the class is being initiated
        used to assign values to object properties
        self parameter is a reference to tha class instance itself & is used 
        to access variables that belong to that class
        """
        self.db = QuestionsModel()

    @require_token
    def patch(current_user, self, answer_id):
        """method to update an answer"""
        answer = self.db.find_answer_by_id(
            answer_id)
        if answer is None:
            return non_existance_question()

        if current_user["user_id"] != self.db.get_quiz_author(answer_id):
            return jsonify({
            "status": 401,
            "error": "sorry you can't accept me lol"
})

        edit_status = self.db.accept_answer(
            answer_id)

        if edit_status == "answer accepted":
            return jsonify({
                "status": 200,
                "data": {
                    "id": answer_id,
                    "message": "you accepted the above as your prefered answer"
                }
            })
