"""Tests for questions in v2 run with pytest"""
import datetime
import json
import os
import unittest

import jwt

from ... import create_app
from app.api.db_config import create_tables, super_user, destroy_tables
from app.tests.v2.test_data import test_user, question_data

secret = os.getenv('SECRET_KEY')

class QuestionsTestCase(unittest.TestCase):
    """
    This class represents the questions test cases
    """

    def setUp(self):
        APP = create_app(config_name="testing")
        APP.testing = True
        self.app = APP.test_client()
        create_tables()
        super_user()

        self.test_user = test_user

        payload = {
            "user_name": self.test_user['user_name'],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }

        token = jwt.encode(
            payload=payload, key=secret, algorithm='HS256')

        self.headers = {'Content-Type': 'application/json',
                        'token': token
                        }

        self.headers_invalid = {
            'Content-Type': 'application/json', 'token': 'Tokenmbaya'}
        self.question = question_data

    def test_get_all_questions(self):
        """Test all questions and answers if any"""
        response = self.app.get("/api/v2/questions", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_all_questions_no_token(self):
        """method to test get all questions with no token"""
        response = self.app.get("/api/v2/questions")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], "Token is missing")            

    def test_get_specific_question(self):
        """Test get a specific question"""
        self.app.post("/api/v2/questions", headers=self.headers,
                      data=json.dumps(self.question))
        response = self.app.get("/api/v2/questions/1", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_post_question(self):
        """Test post a question"""
        response = self.app.post(
            "/api/v2/questions", headers=self.headers, data=json.dumps(self.question))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['status'], 201)

    def test_update_quiz_of_non_existent_question(self):
        """Test update quiz body of a nonexistant question"""       
        response = self.app.patch(
            "/api/v2/questions/12971/questions", headers=self.headers, data=json.dumps({"question": "hello world"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['error'], 'question does not exist')

    def test_update_quiz_of_question(self):
        """Test update quiz body of a specific question"""
        self.app.post(
            "/api/v2/questions", headers=self.headers, data=json.dumps(self.question))        
        response = self.app.patch(
            "/api/v2/questions/1/questions", headers=self.headers, data=json.dumps({"question": "hello quiz"}))
        json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        

    def test_delete_specific_question(self):
        """Test delete a specific question"""
        self.app.post("/api/v2/questions", headers=self.headers,
                      data=json.dumps(self.question))
        response = self.app.delete("/api/v2/questions/1", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_question_withiout_token(self):
        """method to test if one can delete a question withiout token"""
        self.app.post("/api/v2/questions",
                      data=json.dumps(self.question))
        response = self.app.delete("/api/v2/questions/1")
        json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        destroy_tables()                                         