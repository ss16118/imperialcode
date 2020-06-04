import time

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

# class User(models.Model):
#     uname = models.CharField(max_length=30)
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    desc = models.TextField(default="")
    slug = models.SlugField(max_length=255, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    # for using slug
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = slugify(self.title) + '-' + time.strftime("%Y%m%d%H%M%S")
            super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    forum = models.ForeignKey(Post, on_delete=models.CASCADE)
    desc = models.TextField(default="")
    upvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.desc

    def get_absolute_url(self):
        return reverse('forum-list')
