from django.urls import path, include
from rest_framework import routers
from .views import *


# default_router = routers.SimpleRouter(trailing_slash=False)
# default_router.register('answer', AnswerViewSet)

# questoin_router = routers.SimpleRouter(trailing_slash=False)
# questoin_router.register('question', QuestionViewSet)


# urlpatterns = [
#     path('', include(default_router.urls)),
#     path('{user_id}/{question_id}/', include(answer_router.urls)),
# ]
