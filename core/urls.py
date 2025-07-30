from django.urls import path
from .views import TranscriptionView, title_suggestion

urlpatterns = [
    path('transcribe/', TranscriptionView.as_view(), name='transcribe-audio'),
    path('suggest-title/', title_suggestion, name='suggest-title'),
]
