from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fetch/', views.fetch_video_info, name='fetch_video_info'),
]
