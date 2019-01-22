"""Tests for redflags run with pytest"""
import json
import unittest

from ... import create_app


class QuestionTestCase(unittest.TestCase):
    """
    This class represents the question test cases
    """

    def setUp(self):
        APP = create_app("testing")
        self.app = APP.test_client()

        self.question = {
            "created_By": 1,
            "title": "How to write tests",
            "question": "I was wondering  how do u write tests"

        }

    def test_get_all_questions_list_empty(self):
        """method to test get all questions endpoints"""
        response = self.app.get("/api/v1/questions")
        self.assertEqual(response.status_code, 200)

    def test_get_all_questions_list_not_empty(self):
        """method to test get all questions endpoints"""
        self.app.post("/api/v1/questions",
                      headers={'Content-Type': 'application/json'}, data=json.dumps(self.question))        
        response = self.app.get("/api/v1/questions")
        self.assertEqual(response.status_code, 200)

    def test_post_question(self):
        """method to test post a question endpoint"""
        response = self.app.post("/api/v1/questions",
                                 headers={'Content-Type': 'application/json'},data=json.dumps(self.question))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            result['data']['message'], "Created a question record")
        self.assertEqual(
            result['status'], 201)

    def test_get_specific_question(self):
        """method to test if one can get a specific question"""
        self.app.post("/api/v1/questions",
                      headers={'Content-Type': 'application/json'}, data=json.dumps(self.question))
        response = self.app.get("/api/v1/questions/1")
        json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_delete_specific_question(self):
        """method to test delete specific question endpoint"""
        self.app.post("/api/v1/questions",
                      headers={'Content-Type': 'application/json'}, data=json.dumps(self.question))
        response = self.app.delete("/api/v1/questions/1")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('question record has been deleted', str(result))
        self.assertEqual(
            result['status'], 200)

    def test_delete_non_existance_question(self):
        """method to test deletion of non existance question"""
        response = self.app.delete("/api/v1/questions/1")
        result = json.loads(response.data)
        print(result)
        self.assertEqual(response.status_code, 200)
        self.assertIn('question does not exist', str(result))
        self.assertEqual(
            result['status'], 404)

    def test_update_title_of_specific_question(self):
        """method to test edit title of a specific question endpoint"""
        self.app.post("/api/v1/questions/1/title",
                      headers={'Content-Type': 'application/json'}, data=json.dumps(self.question))
        response = self.app.patch("/api/v1/questions/1/title", headers={
                                  'Content-Type': 'application/json'}, data=json.dumps({"title": "How to use Pytest"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated question's title", str(result))
        self.assertEqual(
            result['status'], 200)

    def test_update_title_of_nonexistance_question(self):
        """method to test edit title of a specific question endpoint"""
        response = self.app.patch("/api/v1/questions/33748/title", headers={
                                  'Content-Type': 'application/json'}, data=json.dumps({"title": "How to use Pytest"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('question does not exist', str(result))
        self.assertEqual(
            result['status'], 404)

    def test_update_question(self):
        """method to test edit question endpoint"""
        self.app.post("/api/v1/questions/1/question",
                      headers={'Content-Type': 'application/json'}, data=json.dumps(self.question))
        response = self.app.patch("/api/v1/questions/1/question", headers={'Content-Type': 'application/json'},
                                  data=json.dumps({"question": "How do i start using pytest"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated question",
                      str(result))
        self.assertEqual(
            result['status'], 200)

    def test_update_nonexixstnce_question(self):
        """method to test edit of a question that does not exist"""
        response = self.app.patch("/api/v1/questions/17232/question", headers={'Content-Type': 'application/json'},
                                  data=json.dumps({"question": "How do i start using pytest"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('question does not exist', str(result))
        self.assertEqual(
            result['status'], 404)

    def test_question_not_found(self):
        """Test question not found"""
        response = self.app.get("/api/v1/questions/100")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            result['error'], "question does not exist")
        self.assertEqual(
            result['status'], 404)

    def test_wrong_question_key(self):
        """Test wrong question key while editing a question"""
        response = self.app.patch("/api/v1/questions/1/question", headers={'Content-Type': 'application/json'},
                                  data=json.dumps({"question1": "hello pac"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            result['message']['question'], "This field cannot be left blank or should be properly formated")

    def test_wrong_title_key(self):
        """Test wrong title key while editing a question title"""
        response = self.app.patch("/api/v1/questions/1/title", headers={'Content-Type': 'application/json'},
                                  data=json.dumps({"tito": "hello pac"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            result['message']['title'], "This field cannot be left blank or should be properly formated")
 