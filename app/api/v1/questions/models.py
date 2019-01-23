"""model for view for questions"""
import datetime

from flask import jsonify,request
from flask_restful import Resource
from app.api.validators import parser,parser_edit_question,parser_edit_title

questions = []


class QuestionModel():
    """Class with methods to perform CRUD operations on the list data structure"""

    def __init__(self):
        self.db = questions

        if len(questions) == 0:
            self.id = 1
        else:
            self.id = questions[-1]['id'] + 1
        self.id = len(questions) + 1

    def save(self):
        parser.parse_args()
        data = {
            'id': self.id,
            'createdOn': datetime.datetime.utcnow(),
            'createdBy': request.json.get('createdBy'),
            'title': request.json.get('title'),
            'question': request.json.get('question')
        }

        self.db.append(data)
        return self.id

    def get_all(self):
        if not self.db:
            return None
        return self.db

    def find(self, question_id):
        for question in self.db:
            if question['id'] == question_id:
                return question

        return "question does not exist"

    def delete(self, question):
        self.db.remove(question)
        return "deleted"

    def edit_question_title(self, question):
        "Method to edit a questions title"
        parser_edit_title.parse_args()
        question['title'] = request.json.get('title')
        return "updated"

    def edit_question(self, question):
        "Method to edit a questions"
        parser_edit_question.parse_args()
        question['question'] = request.json.get('question')
        return "updated"        