"""Views for users"""
import datetime

from flask import jsonify,request
from flask_restful import Resource
from .models import UserModel

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
