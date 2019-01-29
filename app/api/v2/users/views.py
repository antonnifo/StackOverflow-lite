"""Views for users"""
import os
import datetime

from flask import jsonify,request
from flask_restful import Resource
from .models import UserModel
import jwt
secret = os.getenv('SECRET_KEY')

def nonexistent_user():
    return jsonify({
        "status": 404,
        "message": "user does not exist"
    })

class UserSignUp(Resource):
    """Class with user signup post method"""

    def __init__(self):
        self.db = UserModel()

    def post(self):
        """method to post user details"""
        user = self.db.save()

        if user == "username already taken please try another one":
            return jsonify({
                "status": 400,
                "error": "username already taken please try another one"
            })
       

        user_details = {
            "name": user['user_name'],         
        }
        return jsonify({
            "status": 201,
            "data": [
                {
                    "account details": user_details,
                    "message": "You have created an account you can now sign in"
                }
            ]
        })


class UserSignIn(Resource):
    """Class containing user login method"""

    def __init__(self):
        self.db = UserModel()

    def post(self):
        """method to get a specific user"""
        user = self.db.log_in()
        if user is None:
            return nonexistent_user()

        if user == 'incorrect password':
            #returns json objects instead of html 
            return jsonify({
                "status": 401,
                "message": "password or email is incorrect please check your details"
            })

        payload = {
            "user_name": user,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }
        
        # An API endpoint is setup at /auth that accepts username
        # via JSON payload and returns access_token
        # which is the JSON Web Token 
        
        token = jwt.encode(payload=payload, key=secret, algorithm='HS256')
        #since p3 is being used the token needs to be decoded to a regular string
        return jsonify({
            "status": 200,
            "data": [
                {
                    "token": token.decode('UTF-8'),
                    "user": user,
                    "message": "You are now signed in you can post your question"
                }
            ]
        })
