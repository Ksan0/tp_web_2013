from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.TextField(max_length=128)
    text = models.TextField(max_length=2048)
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    solved = models.BooleanField(default=False)
    rate = models.IntegerField(default=0)
    views = models.IntegerField(default=0)


class Answer(models.Model):
    text = models.TextField(max_length=2048)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    is_right = models.BooleanField(default=False)
    rate = models.IntegerField(default=0)


class question_like(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    voice = models.IntegerField()


class answer_like(models.Model):
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)
    voice = models.IntegerField(default=0)


class UserRate(models.Model):
    user = models.ForeignKey(User)
    rate = models.IntegerField(default=0)