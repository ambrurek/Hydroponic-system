from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {"username": "testuser", "password": "testpassword"}

    def test_signup_and_login(self):
        """Test user signup, login, and token verification."""
        # User registration
        response_signup = self.client.post(
            "/user/register/", self.user_data, format="json"
        )
        self.assertEqual(response_signup.status_code, status.HTTP_201_CREATED)

        # User login with the newly registered user
        response_login = self.client.post("/user/login/", self.user_data, format="json")
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)

        # Verify if the obtained token is correct
        token_key = response_login.data["token"]
        token = Token.objects.get(key=token_key)
        self.assertEqual(token.user.username, self.user_data["username"])

    def test_invalid_login(self):
        """Test unsuccessful login attempt."""
        # Try to log in with incorrect credentials
        invalid_data = {"username": "nonexistentuser", "password": "wrongpassword"}
        response = self.client.post("/user/login/", invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_test_token_view(self):
        """Test the test-token view with a valid token."""
        # Register and log in a new user
        response_signup = self.client.post(
            "/user/register/", self.user_data, format="json"
        )
        self.assertEqual(response_signup.status_code, status.HTTP_201_CREATED)

        response_login = self.client.post("/user/login/", self.user_data, format="json")
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)

        # Check the test-token view using the correct token
        token_key = response_login.data["token"]
        response_test_token = self.client.get(
            "/user/test/", HTTP_AUTHORIZATION=f"Token {token_key}"
        )
        self.assertEqual(response_test_token.status_code, status.HTTP_200_OK)
        self.assertEqual(response_test_token.data, "Passed!")
