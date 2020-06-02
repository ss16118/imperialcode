from django.urls import path

from . import views
from .views import ForumCreate

urlpatterns = [
    path('add/', ForumCreate.as_view(), name='forum-add'),
    path('', views.home , name='home')
]
