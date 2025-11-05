from django.urls import path

from user.views import UserCreateView, UserProfileView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="user-register"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
]
