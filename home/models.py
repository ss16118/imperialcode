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

class Code_Segment(models.Model):
    index = models.IntegerField()
    code = models.TextField()
    paper = models.ForeignKey(PastPaper, on_delete= models.CASCADE)

    def __str__(self):
        return str(self.paper) + "question" + self.index 


class Question(models.Model):
    question_desc = models.TextField()
    question_index = models.IntegerField(default=0)
    code_segment = models.ForeignKey(Code_Segment, on_delete=models.CASCADE, default="") 
    test_script = models.TextField(default="")
    paper = models.ForeignKey(PastPaper, on_delete= models.CASCADE, default="")

    def __str__(self):
        return self.question_desc


