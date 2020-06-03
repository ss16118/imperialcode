from django.contrib import admin
from .models import Post, Comment
# Register your models here.


class CommentInLine(admin.StackedInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'desc', 'created_at']
    inlines = [CommentInLine]

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['forum', 'user', 'desc', 'created_at']

admin.site.register(Comment, CommentAdmin)



