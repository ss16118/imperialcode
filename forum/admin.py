from django.contrib import admin
from .models import Post, Comment, PostVotes, PostCommentVotes
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


@admin.register(PostVotes)
class PostVotesAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post", "vote"]


@admin.register(PostCommentVotes)
class PostCommentVotesAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "comment", "vote"]