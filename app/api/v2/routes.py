"""all for version 2 routes"""
from flask import Blueprint
from flask_restful import Api

from .users.views import UserSignUp, UserSignIn

VERSION_DOS = Blueprint('apiv2', __name__, url_prefix='/api/v2')
API = Api(VERSION_DOS)

API.add_resource(UserSignUp, '/auth/signup')
API.add_resource(UserSignIn, '/auth/signin')