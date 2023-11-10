from django.shortcuts import render

# Create your views here.

# QuestionViewSet : 질문을 db에서 랜덤으로 불러와서 보여주는 view set. GET 요청만 받음.
# AnswerViewSet : 답변을 db에 저장하는 view set. POST 요청만 받음.

from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.http import Http404
from rest_framework.decorators import action
# 필터 전용 import
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from random import choice


# 욕설 필터링 관련 import
from django.conf import settings
import os
#===================================================================================================
# 질문 필터링 class
class QuestionFilter(filters.FilterSet):
    # category별로 필터링 
    category = filters.ChoiceFilter(choices=Question.CATEGORY_LIST)
    class Meta:
        model = Question
        fields = ['category']

#===================================================================================================
# 욕설 필터링 관련 함수
def load_swears(file_name):
    file_path = os.path.join(settings.BASE_DIR, 'static', file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        swears = file.read().splitlines()
    return swears
SWEARS = load_swears('fword_list.txt')

def censor_content(content):
    is_abused = False
    
    for swear in SWEARS:
        if swear in content:
            content = content.replace(swear, '*' * len(swear))
            is_abused = True
            
    return content, is_abused
#===================================================================================================
class QuestionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    # api/question으로 GET 요청을 받을 시, 질문을 랜덤으로 반환함
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=False, methods=['GET'], url_path='past')
    def past(self, request, *args, **kwargs):
        queryset = Question.objects.filter(category = 'Past').order_by('?')[:1]
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], url_path='present')
    def present(self, request, *args, **kwargs):
        queryset = Question.objects.filter(category = 'Present').order_by('?')[:1]
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], url_path='future')
    def future(self, request, *args, **kwargs):
        queryset = Question.objects.filter(category = 'Future').order_by('?')[:1]
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#===================================================================================================
# 답변 list, create view set
class QuestionAnswerListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = QuestionAnswerSerializer

    def get_queryset(self):
        to_user_id = self.kwargs['id']
        queryset = Question.objects.filter(answer__to_user_id=to_user_id).distinct()
        return queryset

    @action(detail=False, methods=['GET'], url_path='past')
    def past(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(category='Past')
        serializer = self.serializer_class(queryset, many=True, context={'view': self})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='present')
    def present(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(category='Present')
        serializer = self.serializer_class(queryset, many=True, context={'view': self})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='future')
    def future(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(category='Future')
        serializer = self.serializer_class(queryset, many=True, context={'view': self})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerCreateViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    # api/answer로 POST 요청을 받을 시, 답변을 생성함
    queryset = Answer.objects.all()
    serializer_class = AnswerCreateSerializer

    # censor_content를 이용한 욕설 필터링. 욕설이 포함되어 있으면 _ 가 True로 반환됨
    def create(self, request, *args, **kwargs):
        serializer = AnswerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.validated_data['content']
        content, _ = censor_content(content)

        serializer.validated_data['content'] = content
        return Response(serializer.data, status=status.HTTP_201_CREATED)
#===================================================================================================