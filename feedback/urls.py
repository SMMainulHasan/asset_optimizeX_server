from django.urls import path
from feedback.views import *

urlpatterns = [
    path('feedback/', FeedbackView.as_view(), name='feedback'),
]

