from django.urls import path

from user.views import LoginView, LogoutView, UserCreateView, UserProfileView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="user-register"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("login/", LoginView.as_view(), name="user-login"),
    path("logout/", LogoutView.as_view(), name="user-logout"),
]
