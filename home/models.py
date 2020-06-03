from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.

# class User(models.Model):
#     uname = models.CharField(max_length=30)
class PastPaper(models.Model):
    title = models.CharField(max_length=100)
    language = models.CharField(max_length=32)
    spec_path = models.CharField(max_length=32)
    desc = models.TextField(default="")
    year = models.IntegerField()
    difficulty = models.IntegerField()
    upvotes = models.IntegerField()

    def __str__(self):
        return self.title


class Question(models.Model):
    question_desc = models.TextField()
    question_code = models.TextField()
    paper = models.ForeignKey(PastPaper, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_desc
