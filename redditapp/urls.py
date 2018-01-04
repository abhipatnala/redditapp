from django.urls import path

from . import views

app_name = 'redditapp'

urlpatterns = [
        path('<int:question_id>/', views.detail, name='detail'),
        path('<int:question_id>/comment/', views.comment, name='comment'),
        path('ask_question', views.ask_question, name='ask_question'),
        path('add_question', views.add_question, name='add_question'),

        path('<int:question_id>/add_vote/', views.add_vote, name='add_vote'),
        ]
