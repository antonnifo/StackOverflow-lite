'''model for users view file'''

import datetime

import psycopg2.extras
from flask import request
from flask_restful import reqparse
from werkzeug.security import check_password_hash, generate_password_hash

from app.api.db_config import connection
from app.api.db_config import DATABASE_URL as url
from app.api.validators import validate_email, validate_string, validate_password

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('first_name',
                    type=validate_string,
                    required=True,
                    nullable=False,
                    trim=True,
                    help="This field cannot be left blank or should be properly formated"
                    )

parser.add_argument('last_name',
                    type=validate_string,
                    required=True,
                    nullable=False,
                    help="This field cannot be left blank or should be properly formated"
                    )

parser.add_argument('email',
                    type=validate_email,
                    required=True,
                    nullable=False,
                    trim=True,
                    help="This field cannot be left blank or should be properly formated"
                    )

parser.add_argument('user_name',
                    type=validate_string,
                    required=False,
                    trim=True,
                    nullable=True,
                    help="This field cannot be left blank or should be properly formated"
                    )

parser.add_argument('password',
                    type=validate_password,
                    required=True,
                    nullable=False,
                    help="This field cannot be left blank or should be properly formated and should contain atleast 8 characters"
                    )
class UserModel:
    """class for manipulating user data"""

    def __init__(self):
        self.isAdmin = False
        self.db = connection(url)

    def set_password(self, password):
        '''salting the passwords '''
        return generate_password_hash(password)

    def check_passsword(self, pwdhash, password):
        return check_password_hash(pwdhash, password)

    def save(self):
        parser.parse_args()
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

    def log_in(self):
        data = {
            'user_name': request.json.get('user_name'),
            'password': request.json.get('password')
        }
        user = self.find_user_by_username(data['user_name'])
        if user == None:
            return None
        if check_password_hash(user['password'], data['password']) == False:
            return 'incorrect password'
        return user['user_name']
