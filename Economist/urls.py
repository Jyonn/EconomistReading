from django.urls import path

from Economist.views import TodayView

urlpatterns = [
    path('today', TodayView.as_view()),
]