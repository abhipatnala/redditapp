# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect

from .models import Question,Comment,CommentForm,QuestionForm,Vote
from django.urls import reverse
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout

import pdb


from django.shortcuts import get_object_or_404, render,redirect
@login_required
def home(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
            'latest_question_list': latest_question_list,
            }
    return render(request, 'redditapp/home.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    is_voted = True if Vote.objects.filter(question_id=question, voter=request.user).count() > 0 else False

    total_vote_count =  Vote.objects.filter(question_id=question).count()
    context = {
            'question':question,
            'is_voted':is_voted,
            'total_vote_count':total_vote_count,
            }
    return render(request, 'redditapp/detail.html', context)

def comment(request,question_id):
    question = Question.objects.get(pk= question_id)

    if request.method == "POST":
      MyCommentForm = CommentForm(request.POST)

      if MyCommentForm.is_valid():
         c_text = MyCommentForm.cleaned_data['comments']
         new_comment = Comment(question_id=question, comment_text = c_text,auth_user= request.user)
         new_comment.save()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

def add_question(request):

    if request.method == "POST":
        MyQuestionForm =  QuestionForm(request.POST)

    if MyQuestionForm.is_valid():
        q_text = MyQuestionForm.cleaned_data['new_question']
        new_ques = Question(question_text = q_text,author = request.user)
        new_ques.save()
    return redirect('home')

def ask_question(request):

    return render(request,'redditapp/ask_question.html')

def add_vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    new_vote = Vote(question_id = question,voter = request.user)
    new_vote.save()
    next = request.POST.get('next', '/')

    return HttpResponseRedirect(next)

def custom_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    else:
        return login(request)

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/login')











