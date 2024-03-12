from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView

from .serializers import UserSerializer


class LoginView(APIView):
    """
    API view for handling user login.

    Accepts POST requests with 'username' and 'password'.
    Returns a JSON response with a user token on successful login.

    Returns:
        Response: JSON response with 'token' and 'user' details.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user login.

        Args:
            request (Request): The incoming request.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response with 'token' and 'user' details.
        """
        username = request.data.get("username")
        password = request.data.get("password")

        user = get_object_or_404(User, username=username)

        if not user.check_password(password):
            return Response("Missing user", status=status.HTTP_404_NOT_FOUND)

        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({"token": token.key, "user": serializer.data})


class SignupView(CreateAPIView):
    """
    API view for handling user registration.

    Accepts POST requests with user registration details.
    Returns a JSON response with user details and a token on successful registration.

    Returns:
        Response: JSON response with user details and 'token'.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Perform user registration.

        Args:
            serializer (UserSerializer): The serializer for user registration.

        Returns:
            Response: JSON response with user details and 'token'.
        """
        user = serializer.save()
        user.set_password(self.request.data.get("password"))
        user.save()
        token = Token.objects.create(user=user)
        serializer_data = serializer.data
        serializer_data["token"] = token.key
        return Response(serializer_data, status=status.HTTP_201_CREATED)


class TestTokenView(APIView):
    """
    API view to test user token authentication.

    Requires an authenticated user with a valid token.
    Returns a simple response confirming successful authentication.

    Returns:
        Response: A simple response confirming successful authentication.
    """

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for testing user token authentication.

        Args:
            request (Request): The incoming request.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A simple response confirming successful authentication.
        """
        return Response("Passed!")
