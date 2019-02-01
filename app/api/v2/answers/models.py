"""Models for questions"""

import re

import psycopg2.extras
from flask import request
from flask_restful import reqparse

from app.api.db_config import DATABASE_URL as url
from app.api.db_config import connection
from app.api.validators import parser_answer

class AnswerModel:
    """Class with methods to perform CRUD operations on the DB"""

    def __init__(self):
        self.db = connection(url)
        
    def post_answer(self, user_id, question_id):
        parser_answer.parse_args()
        data = {
            'user_id': user_id,
            'question_id':question_id,
            'answer': request.json.get('answer')
            
        }

        query = """INSERT INTO answers (user_id,question_id, answer) VALUES({0},'{1}','{2}');""".format(
             data['user_id'], data['question_id'], data['answer'])
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return data
        