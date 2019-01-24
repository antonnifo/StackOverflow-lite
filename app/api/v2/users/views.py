"""Views for users"""
import datetime

from flask import jsonify,request
from flask_restful import Resource
from .models import UserModel

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
            return jsonify({
                "status": 401,
                "message": "password or email is incorrect please try again"
            })

        return jsonify({
            "status": 200,
            "data": [
                {
                    "user": user,
                    "message": "You are now signed in you can post your question"
                }
            ]
        })