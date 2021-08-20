from django.urls import path
from quickstart import views

urlpatterns = [
    path('quickstart/predict', views.PredictAPI.as_view()),
    path('quickstart/publish', views.PublishAPI.as_view()),
]
