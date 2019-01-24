'''model for users view file'''

import datetime

import psycopg2.extras
from flask import request
from flask_restful import reqparse
from werkzeug.security import check_password_hash, generate_password_hash

from app.api.db_config import connection
from app.api.db_config import DATABASE_URL as url 

class UserModel:
    """class for manipulating user data"""

    def __init__(self):
        self.isAdmin = False
        self.db = connection(url)

    def set_password(self, password):
        '''salting the passwords '''
        return generate_password_hash(password)

    def check_passsword(self, password):
        return check_password_hash(self.pwdhash, password)

    def save(self):
        # parser.parse_args()
        data = {
            'user_name': request.json.get('user_name'),
            'first_name': request.json.get('first_name'),
            'last_name': request.json.get('last_name'),
            'email': request.json.get('email'),
            'password': self.set_password(request.json.get('password')),
            'isAdmin': self.isAdmin
        }

        user_by_username = self.find_user_by_username(data['user_name'])

        if user_by_username != None:
            return 'username already taken please try another one'
        query = """INSERT INTO users (user_name,first_name,last_name,email,password,isAdmin) VALUES('{0}','{1}','{2}','{3}','{4}','{5}');""".format(
            data['user_name'], data['first_name'], data['last_name'], data['email'], data['password'], data['isAdmin'])
        conn = self.db
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        conn.commit()
        return data

    def find_user_by_username(self, user_name):
        "Method to find a user by username"
        query = """SELECT * from users WHERE user_name='{0}'""".format(user_name)
        conn = self.db
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        row = cursor.fetchone()

        if cursor.rowcount == 0:
            return None
        return row
