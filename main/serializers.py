
from rest_framework import serializers
from .models import *

#===================================================================================================
class AnswerListSerializer(serializers.ModelSerializer):
    question_content = serializers.CharField(source='question.content', read_only=True)
    class Meta:
        model = Answer
        fields = ['id', 'to_user', 'writer', 'content', 'question', 'question_content', 'created_at']

class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
#===================================================================================================
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
#===================================================================================================
# 이건 은호가 해서 필요없을듯
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'