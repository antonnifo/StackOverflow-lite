"""Views for posting questions"""
from flask import jsonify, request
from flask_restful import Resource

from app.api.v2.questions.models import QuestionsModel
from app.api.v2.token_decorator import require_token
from app.api.v2.users.models import UserModel
from app.api.validators import (
    non_existance_question, only_creater_can_delete, only_creater_can_edit)


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
            "question": questions
        })

    @require_token
    def delete(current_user, self, question_id):
        """view method for deleting a quiz and all its answers"""
        question = self.db.find_quiz_by_id(question_id)
        if question is None:
            return non_existance_question()

        if current_user["user_id"] != question["user_id"]:
            return only_creater_can_delete()

        if self.db.delete(question_id) == "deleted":
            return jsonify({
                "status": 200,
                "message": 'you have deleted your question'
            })

class UpdateQuestion(Resource):
    """view class for updating a quiz"""

    def __init__(self):
        """
        executes when the class is being initiated
        used to assign values to object properties
        self parameter is a reference to tha class instance itself & is used 
        to access variables that belong to that class
        """
        self.db = QuestionsModel()

    @require_token
    def patch(current_user, self, question_id):
        """method to update a question"""
        question = self.db.find_quiz_by_id(
            question_id)
        if question is None:
            return non_existance_question()

        if current_user["user_id"] != question['user_id']:
            return only_creater_can_edit()

        edit_status = self.db.update_quiz(
            question_id)

        if edit_status == "quiz updated":
            return jsonify({
                "status": 200,
                "data": {
                    "id": question_id,
                    "message": "Updated your question"
                }
            })
