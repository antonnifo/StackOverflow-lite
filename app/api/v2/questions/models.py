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
            'createdBy': user_id,
            'title': request.json.get('title'),
            'description': request.json.get('description')
        }

        query = """INSERT INTO questions (createdby,title, description) VALUES({0},'{1}','{2}');""".format(
             data['createdBy'], data['title'], data['description'])
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return data
