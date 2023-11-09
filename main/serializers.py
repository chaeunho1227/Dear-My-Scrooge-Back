
from rest_framework import serializers
from .models import *

class AnswerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'