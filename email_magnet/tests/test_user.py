from django.test import TestCase, Client
from django.urls import reverse
from django import stat

from http import HTTPStatus


CREATE_USER_URL = reverse('email_magnet:signup')

class UserTests(TestCase):
    """Test the users functionality: create & login"""

    def setUp(self):
        self.client = Client()

    def test_create_valid_user_success(self):
        """Test creating user is successful"""
        credentials = {
            'username': 'testname'
            'email': 'test@xemob.com'
            'password': 'Testpassword123'
        }
        res = self.client.post(CREATE_USER_URL, credentials)

        self.assertEqual(res.status_code, HTTPStatus.OK)