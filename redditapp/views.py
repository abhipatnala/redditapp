# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import get_object_or_404, render, redirect

from redditapp.models import Question, Comment, CommentForm, QuestionForm, Vote


@login_required
def home(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
            'latest_question_list': latest_question_list,
            }
    return render(request, 'redditapp/home.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question,
        'is_voted': question.is_voted(request.user),
        'total_vote_count': question.vote_set.count(),
    }
    return render(request, 'redditapp/detail.html', context)


def comment(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            c_text = comment_form.cleaned_data['comments']
            Comment.objects.create(
                question_id=question,
                comment_text=c_text,
                auth_user=request.user
            )
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


def add_question(request):
    if request.method == "POST":
        question_form = QuestionForm(request.POST)

        if question_form.is_valid():
            q_text = question_form.cleaned_data['new_question']
            Question.objects.create(question_text=q_text, author=request.user)

    return redirect('home')


def ask_question(request):
    return render(request, 'redditapp/ask_question.html')


def add_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if not question.is_voted(request.user):
        Vote.objects.create(question_id=question, voter=request.user)
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











