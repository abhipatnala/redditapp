# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms


class CommentForm(forms.Form):
    comments = forms.CharField(max_length=100)


class QuestionForm(forms.Form):
    new_question = forms.CharField(max_length=400)


class Question(models.Model):
    question_text = models.CharField(max_length=400)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def is_voted(self, user):
        return self.vote_set.filter(voter=user).count() > 0


class Comment(models.Model):
    comment_text = models.CharField(max_length=100)
    auth_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)


class Vote(models.Model):
    voter = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    voted_date = models.DateTimeField('voted_date', auto_now_add=True)
