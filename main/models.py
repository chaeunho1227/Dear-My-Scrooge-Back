from django.db import models
from users.models import User
# Create your models here.
class Question(models.Model):
    CATEGORY_LIST = (
        ('Past', 'Past'),
        ('Present', 'Present'),
        ('Future', 'Future'),
    )
    id = models.AutoField(primary_key=True)
    content = models.CharField(null=False, blank=False, max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_LIST, blank=False, null=False)
    
    def __str__(self):
        return str(self.id) + "번 '" + self.category + "' 질문 : " + self.content

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    writer = models.CharField(null=False, blank=False, max_length=30)
    content = models.TextField(null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.question.id) + "번 질문 답변 : " + self.content + "by" + self.writer