"""Models for questions"""

import re

import psycopg2.extras
from flask import request
from flask_restful import reqparse

from app.api.db_config import DATABASE_URL as url
from app.api.db_config import connection
from app.api.validators import parser


class QuestionsModel:
    """Class with methods to perform CRUD operations on the DB"""

    def __init__(self):
        self.db = connection(url)

    def save(self, user_id):
        parser.parse_args()
        data = {
            'user_id': user_id,
            'title': request.json.get('title'),
            'question': request.json.get('question')
        }

        query = """INSERT INTO questions (user_id ,title, question) VALUES({0},'{1}','{2}');""".format(
             data['user_id'], data['title'], data['question'])
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return data

    def find_all(self):
        """method to find all questions"""
        query = """SELECT * from questions"""
        conn = self.db
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        questions = cursor.fetchall()
        return questions

    def find_quiz_by_id(self,question_id):
        """method to a question by ID"""
        query = """SELECT * from questions WHERE  question_id={0} """.format(question_id)
        conn = self.db
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        question = cursor.fetchone()
        if not question:
            return None
        return question

    def find_quiz_answers(self, question_id):
        """method to find a specific quiz and its answers"""
        query = """SELECT questions.title, questions.question, questions.date_created, answers.answer, answers.date_created, answers.user_preferred
                   FROM questions
                   INNER JOIN answers ON questions.question_id=answers.question_id"""
        conn = self.db
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        questions = cursor.fetchall()
        return questions

    def delete(self, question_id):
        "Method to delete question and all its answers"
        delete_quiz = """DELETE FROM questions WHERE question_id={0}""".format(
            question_id)
        
        delete_answers = """DELETE FROM answers WHERE question_id={0}""".format(
            question_id)
        queries = [delete_quiz, delete_answers]

        conn = self.db
        cursor = conn.cursor()

        for query in queries:
            cursor.execute(query)
            conn.commit()
            return 'deleted'
