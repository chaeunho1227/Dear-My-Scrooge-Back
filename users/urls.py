from django.urls import path, include
from rest_framework import routers
from . import views
from .views import UserNameViewSet
app_name = 'users'

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("username", UserNameViewSet, basename="username")

urlpatterns = [
    # 닉네임 반환
    path('', include(default_router.urls), name='get-username'),

    # 로그인/회원가입
    path('', views.JWTLoginView.as_view()),
    path('signup', views.JWTSignupView.as_view()),
    path('refresh', views.JWTRefreshView.as_view(), name='token_refresh'),
]