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
    slug = models.SlugField(unique=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # for using slug
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('home') # note: give a working redirect page


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    forum = models.ForeignKey(Post, on_delete=models.CASCADE)
    desc = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)


class PastPaper(models.Model):
    title = models.CharField(max_length=100)
    language = models.CharField(max_length=32)
    spec_path = models.CharField(max_length=32)
    desc = models.TextField(default="")
    year = models.PositiveIntegerField()
    difficulty = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    upvotes = models.IntegerField()


class Question(models.Model):
    question_desc = models.TextField()
    question_code = models.TextField()
    paper = models.ForeignKey(PastPaper, on_delete=models.CASCADE)
