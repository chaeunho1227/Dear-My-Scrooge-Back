from django.shortcuts import render

# Create your views here.

# QuestionViewSet : 질문을 db에서 랜덤으로 불러와서 보여주는 view set. GET 요청만 받음.
# AnswerViewSet : 답변을 db에 저장하는 view set. POST 요청만 받음.

from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.http import Http404

class QuestionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    # api/questoin/으로 GET 요청을 받을 시, 랜덤 질문 1개를 반환함
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def list(self, request, *args, **kwargs):
        # 랜덤으로 질문 1개를 불러옴
        queryset = Question.objects.order_by('?')[:1]
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        # question id를 url에서 받아옴
        question_id = self.kwargs['pk']

        # question id에 해당하는 질문을 불러옴
        queryset = Question.objects.filter(id=question_id)
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AnswerListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    # api/answer/<user_id>로 GET 요청을 받을 시, 답변 목록을 반환함
    queryset = Answer.objects.all()
    serializer_class = AnswerListSerializer

    def list(self, request, *args, **kwargs):
        # user id를 url에서 받아옴
        user_id = self.kwargs['pk']

        # user id에 해당하는 답변 목록을 불러옴
        queryset = Answer.objects.filter(user_id=user_id)
        serializer = AnswerListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AnswerCreateViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    # api/answer로 POST 요청을 받을 시, 답변을 생성함
    queryset = Answer.objects.all()
    serializer_class = AnswerCreateSerializer

    def create(self, request, *args, **kwargs):
        # user id 없이 답변을 생성할 수 있도록 함
        serializer = AnswerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    