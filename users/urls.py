from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from . import views

app_name = 'users'

urlpatterns = [
    # 로그인/회원가입
    path('', views.JWTLoginView.as_view()),
    path('signup', views.JWTSignupView.as_view()),

    path('refresh', views.JWTRefreshView.as_view(), name='token_refresh'),
]