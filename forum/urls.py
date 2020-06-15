from django.urls import path
from django.conf.urls import url
from . import views
from .views import ForumCreate, ForumListView, ForumUserListView, ForumDetailView,\
    ForumUpdateView, ForumDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView, VoteRegisterView, \
    SaveCommentView, DeleteCommentView

urlpatterns = [
    # Urls for ajax requests
    path('register_post_vote/', VoteRegisterView.as_view(), name='register_post_vote'),
    path('register_comment_vote/', VoteRegisterView.as_view(), name='register_comment_vote'),
    path('save_comment/', SaveCommentView.as_view(), name="save_comment"),
    path('delete_comment/', DeleteCommentView.as_view(), name="delete_comment"),
    path('', ForumListView.as_view(), name='forum-list'),
    path('add/', ForumCreate.as_view(), name='forum-add'),
    path('by/<username>/', ForumUserListView.as_view(), name='forum-by'),
    path('edit/<int:pk>', ForumUpdateView.as_view(), name='forum-edit'),
    path('delete/<int:pk>', ForumDeleteView.as_view(), name='forum-delete'),
    path('<slug:slug>/', ForumDetailView.as_view(), name='forum-detail'),
    # Comment path
    path('add-comment/<int:pk>', CommentCreateView.as_view(), name='add-comment'),
    path('edit-comment/<int:pk>', CommentUpdateView.as_view(), name='edit-comment'),
    path('delete-comment/<int:pk>', CommentDeleteView.as_view(), name='delete-comment'),
]
