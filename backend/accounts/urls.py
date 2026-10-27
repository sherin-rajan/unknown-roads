from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", views.current_user, name="current-user"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.customer_profile, name="customer-profile"),
    path("change-password/", views.change_password, name="change-password"),
    path("favorites/", views.customer_favorites, name="customer-favorites"),
    path("favorites/<int:favorite_id>/", views.remove_favorite, name="remove-favorite",),
]
