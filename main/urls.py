from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'main'

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register('answers', QuestionAnswerListViewSet, basename='answers') #여기 basename 없으면 오류남 뷰셋에 queryset이 url 매개변수를 필요로 하기 떄문인 것 같은데 조사 더 필요함.

answer_router = routers.SimpleRouter(trailing_slash=False)
answer_router.register('answer', AnswerCreateViewSet)

question_router = routers.SimpleRouter(trailing_slash=False)
question_router.register('question', QuestionViewSet)


urlpatterns = [
    path('username/<int:id>/', include(default_router.urls)),
    path('', include(question_router.urls)),
    path('username/<int:id>/', include(answer_router.urls)),
]
