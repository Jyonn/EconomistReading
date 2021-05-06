from django.urls import path

from utils.views import GrabView

urlpatterns = [
    path('grab-news', GrabView.as_view()),
]
