from django.urls import path
from .views import SignupView, LoginView, TestTokenView

urlpatterns = [
    path("register/", SignupView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("test/", TestTokenView.as_view(), name="test"),
]
