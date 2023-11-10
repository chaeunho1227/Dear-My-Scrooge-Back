from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'main'

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register('answer', AnswerListViewSet)

answer_router = routers.SimpleRouter(trailing_slash=False)
answer_router.register('answer', AnswerCreateViewSet)

question_router = routers.SimpleRouter(trailing_slash=False)
question_router.register('question', QuestionViewSet)


urlpatterns = [
    path('', include(default_router.urls)),
    path('', include(question_router.urls)),
    path('username/<int:id>', include(answer_router.urls)),
]
