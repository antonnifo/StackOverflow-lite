"""Models for answers"""

import psycopg2.extras
from flask import request

from app.api.db_config import DATABASE_URL as url
from app.api.db_config import connection
from app.api.validators import parser_answer, parser_edit_answer, parser_user_preferred
from app.api.v2.questions.models import QuestionsModel

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

    def find_answer_by_id(self,answer_id):
        """method to find an answer by ID"""
        query = """SELECT * from answers WHERE  answer_id={0} """.format(answer_id)
        conn = self.db
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        answer = cursor.fetchone()
        if not answer:
            return None
        return answer

    def update_answer(self, answer_id):
        "Method to edit an answer"
        parser_edit_answer.parse_args()
        answer = request.json.get('answer')

        query = """UPDATE answers SET answer='{0}' WHERE answer_id={1}""".format(
            answer, answer_id)
        con = self.db
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        return 'answer updated'

    def get_quiz_author(self, answer_id):
        """method to get the author of a specific quiz"""
        answer = self.find_answer_by_id(answer_id)
        question_id = answer['question_id']
        question = QuestionsModel().find_quiz_by_id(question_id)
        quiz_author = question['user_id']
        return quiz_author

    def set_false(self, answer_id):
        """method to set user prefered to false before an owner of a quiz updates any
        of the answer.This allows the user to change his/her prefered answer and also to only 
        accept one answer"""
        user_preferred = False
        query = """UPDATE answers SET user_preferred={0}""".format(
            user_preferred)
        con = self.db
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        return True            

    def accept_answer(self, answer_id):
        """Method for the owner of the quiz to accept an answer"""
        user_preferred = request.json.get('user_preferred')

        self.set_false(answer_id)
        query = """UPDATE answers SET user_preferred={0} WHERE answer_id={1}""".format(
            user_preferred, answer_id)
        con = self.db
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        return 'answer accepted'

    def delete(self, answer_id):
        "Method to delete an answer specifically by the author of the answer"
        query = """DELETE FROM answers WHERE answer_id={0}""".format(
            answer_id)
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return "deleted"    
