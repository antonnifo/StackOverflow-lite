"""all for version 2 routes"""
from flask import Blueprint
from flask_restful import Api

from app.api.v2.users.views import UserSignUp, UserSignIn
from app.api.v2.questions.views import Questions, Question,UpdateQuestion
from app.api.v2.answers.views import Answers, UpdateAnswer

VERSION_DOS = Blueprint('apiv2', __name__, url_prefix='/api/v2')
API = Api(VERSION_DOS)

API.add_resource(UserSignUp, '/auth/signup')
API.add_resource(UserSignIn, '/auth/signin')
API.add_resource(Questions, '/questions')
API.add_resource(Answers, '/questions/<int:question_id>/answers')
API.add_resource(Question, '/questions/<int:question_id>')
API.add_resource(UpdateQuestion,
'/questions/<int:question_id>/question')
API.add_resource(UpdateAnswer,
'/answers/<int:answer_id>/answer')
