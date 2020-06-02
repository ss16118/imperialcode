from django.contrib import admin
from home.models import PastPaper, Question
from forum.models import Post, Comment

# Register your models here.
admin.site.register(PastPaper)
admin.site.register(Question)
admin.site.register(Post)
admin.site.register(Comment)
