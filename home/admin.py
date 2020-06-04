from django.contrib import admin
from home.models import PastPaper, Question, CodeSegment
from forum.models import Post, Comment


# Register your models here.
@admin.register(PastPaper)
class PastPaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'year', 'desc', 'difficulty', 'upvotes']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id",'question_desc', "question_index",'code_segment', 'test_script']


@admin.register(CodeSegment)
class CodeSegmentAdmin(admin.ModelAdmin):
    list_display = ["id",'index', 'code', 'paper']
