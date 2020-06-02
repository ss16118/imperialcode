from django.db import models
from django.conf import settings

# Create your models here.

# class User(models.Model):
#     uname = models.CharField(max_length=30)
class Forum(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    desc = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    desc = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

class PastPaper(models.Model):
    title = models.CharField(max_length=100)
    language = models.CharField(max_length=32)
    spec_path = models.CharField(max_length=32)
    desc = models.TextField(default="")
    year = models.IntegerField() 
    difficulty = models.IntegerField() 
    upvotes = models.IntegerField()

class Question(models.Model):
    question_desc = models.TextField()
    question_code =  models.TextField()
    paper = models.ForeignKey(PastPaper, on_delete=models.CASCADE)