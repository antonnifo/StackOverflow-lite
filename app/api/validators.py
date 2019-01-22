"""for fields validations purposes"""
import re

from flask import jsonify, request
from flask_restful import reqparse

def validate_string(value):
    """method to check that the field takes only letters"""
    if not re.match(r"[A-Za-z1-9]+", value):
        raise ValueError("Pattern not matched")


def validate_password(value):
    """method to check if password contains more than 8 characters"""
    if not re.match(r"^[A-Za-z0-9!@#$%^&+*=]{8,}$", value):
        raise ValueError("Password should be at least 8 characters")


def validate_email(value):
    """method to check for valid email"""
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", value):
        raise ValueError("write a proper Email")


parser = reqparse.RequestParser(bundle_errors=True)
parser_edit_question = reqparse.RequestParser(bundle_errors=True)
parser_edit_title = reqparse.RequestParser(bundle_errors=True)


parser.add_argument('title',
                    type=validate_string,
                    required=True,
                    trim=True,
                    nullable=False,
                    help="This field cannot be left blank or improperly formated"
                    )

parser_edit_title.add_argument('title',
                                type=validate_string,
                                required=True,
                                trim=True,
                                nullable=False,
                                help="This field cannot be left blank or should be properly formated"
                                )

parser.add_argument('question',
                    type=validate_string,
                    required=True,
                    trim=True,
                    nullable=False,
                    help="This field cannot be left blank or improperly formated"
                    )

parser_edit_question.add_argument('question',
                                 type=validate_string,
                                 required=True,
                                 trim=True,
                                 nullable=False,
                                 help="This field cannot be left blank or should be properly formated"
                                 )

def non_existance_question():
    '''return message for a question  that does not exist'''
    return jsonify({
        "status": 404,
        "error": "question does not exist"
    })
