from django.contrib import admin
from home.models import Problem, Question, CodeSegment, UserProgress, QuestionComment, UserVotes


# Register your models here.
@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'year', 'desc', 'difficulty']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id",'question_desc', "question_index",'code_segment', 'test_script']


@admin.register(CodeSegment)
class CodeSegmentAdmin(admin.ModelAdmin):
    list_display = ["id",'index', 'code', 'problem']


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "problem", "stopped_at", "progress"]


@admin.register(QuestionComment)
class QuestionCommentAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "parent_comment","user" , "upvotes", "created_at"]

@admin.register(UserVotes)
class UserVotesAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "problem", "vote"]

