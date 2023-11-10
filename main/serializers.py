
from rest_framework import serializers
from .models import *

#===================================================================================================
# class AnswerListSerializer(serializers.ModelSerializer):
#     question_content = serializers.CharField(source='question.content', read_only=True)
#     class Meta:
#         model = Answer
#         fields = ['id', 'to_user', 'writer', 'content', 'question', 'question_content', 'created_at']

class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    answer_id = serializers.IntegerField(source='id') # 'id' -> 'answer_id'로 이름 변경

    class Meta:
        model = Answer
        fields = ['answer_id', 'writer', 'content', 'created_at']
#===================================================================================================

class QuestionAnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(source='id') # 'id' ->  'question_id'로 이름 변경
    answers = serializers.SerializerMethodField() # answer들을 표시하기 위한 시리얼라이저

    class Meta:
        model = Question
        fields = ['question_id', 'content', 'answers']
        
    def get_answers(self, obj):
        answers = Answer.objects.filter(question=obj, to_user__id=self.context['view'].kwargs['id'])
        #연결된 view에서 id를 가져와 answers를 받는겨
        return AnswerSerializer(answers, many=True).data
    
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