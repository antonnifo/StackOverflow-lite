"""all routes"""
from flask import Blueprint
from flask_restful import Api

from .questions.views import Questions

VERSION_UNO = Blueprint('api', __name__, url_prefix='/api/v1')
API = Api(VERSION_UNO)
API.add_resource(Questions, '/questions')
