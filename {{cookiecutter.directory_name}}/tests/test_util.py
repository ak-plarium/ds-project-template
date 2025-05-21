from unittest import TestCase
from {{cookiecutter.project_slug}}.util import hello_world

class TestUtil(TestCase):
    """test classes must start with 'Test'"""

    def test_hello_world(self):
        """test methods must start with 'test_{test_description}'"""
        self.assertEqual(hello_world(), "Hello world!")
        