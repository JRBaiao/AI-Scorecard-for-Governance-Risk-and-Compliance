from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.home,              name='home'),
    path('evaluate/start/',         views.step1,             name='step1'),
    path('evaluate/step1/',         views.step1,             name='step1'),
    path('evaluate/step2/',         views.step2,             name='step2'),
    path('evaluate/step3/',         views.step3,             name='step3'),
    path('evaluate/step4/',         views.step4,             name='step4'),
    path('evaluate/restart/',       views.restart,           name='restart'),
    path('results/<int:pk>/',       views.results,           name='results'),
    path('history/',                views.history,           name='history'),
    path('delete/<int:pk>/',        views.delete_evaluation, name='delete_evaluation'),
    path('chat/',                   views.chat_api,          name='chat_api'),
]
