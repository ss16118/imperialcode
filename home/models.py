from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver


class Problem(models.Model):
    class Category:
        NONE = "None"
        RECURSION = "Recursion"
        DP = "Dynamic Programming"
        CONTROL_FLOW = "Control Flow"
        DIVIDE_AND_CONQUER = "Divide and Conquer"
        TREE = "Tree"
        OPTIONS = (
            (NONE, "None"),
            (RECURSION, "Recursion"),
            (DP, "Dynamic programming"),
            (CONTROL_FLOW, "Control Flow"),
            (DIVIDE_AND_CONQUER, "Divide and Conquer"),
            (TREE, "Tree")
        )

    class Type:
        NONE = "None"
        EXAM = "Exam"
        USER_PROVIDED = "User Provided"
        TUTORIAL = "Tutorial"
        UNASSESSED = "Unassessed Exercise"
        OPTIONS = (
            (NONE, "None"),
            (EXAM, "Exam"),
            (USER_PROVIDED, "User Provided"),
            (TUTORIAL, "Tutorial"),
            (UNASSESSED, "Unassessed Exercise")
        )

    title = models.CharField(max_length=100)
    language = models.CharField(max_length=32)
    spec_path = models.CharField(max_length=300)
    desc = models.TextField(default="")
    year = models.IntegerField()
    difficulty = models.IntegerField(validators=[
        MaxValueValidator(3),
        MinValueValidator(1)
    ])
    category = models.CharField(max_length=50, choices=Category.OPTIONS, default=Category.NONE)
    type = models.CharField(max_length=50, choices=Type.OPTIONS, default=Type.NONE)
    upvotes = models.IntegerField()

    def __str__(self):
        return self.title


class CodeSegment(models.Model):
    index = models.IntegerField()
    code = models.TextField()
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Question(models.Model):
    question_desc = models.TextField()
    question_index = models.IntegerField(default=0)
    code_segment = models.ForeignKey(CodeSegment, on_delete=models.CASCADE, default="")
    test_script = models.TextField(default="")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.question_desc


class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    stopped_at = models.PositiveIntegerField(default=0)
    progress = ArrayField(models.PositiveIntegerField())
    last_modified = models.DateTimeField(auto_now=True)


class QuestionComment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="")
    desc = models.TextField(default="")
    upvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.desc


class UserVotes(models.Model):
    UP = 1
    NO_VOTE = 0
    DOWN = -1
    VOTE_OPTIONS = (
        (UP, 1),
        (NO_VOTE, 0),
        (DOWN, -1)
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    vote = models.IntegerField(default=NO_VOTE, choices=VOTE_OPTIONS)

'''
class ActionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
'''
