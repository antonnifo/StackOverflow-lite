"""Tests for validators run with pytest"""
import unittest
from app.api.validators import validate_string, validate_email,validate_password    


class ValidatorsTestCase(unittest.TestCase):


    def test_for_strings(self):
        with self.assertRaises(ValueError):
            validate_string("@##$$Hello")

    def test_for_email(self):
        with self.assertRaises(ValueError):
            validate_email("antonnifogmail.com")

    def test_for_password(self):
        with self.assertRaises(ValueError):
            validate_password(" ")
