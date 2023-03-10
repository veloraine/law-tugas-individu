from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "auth"

urlpatterns = [
    path('register',register, name='register'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]