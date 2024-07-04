from django.urls import path
from . import views

urlpatterns = [
    path('record/', views.home, name='home'),
    path('', views.record, name='record'),
    path('save_speech_text/', views.save_speech_text, name='save_speech_text'),
    path('song/', views.display_text, name='song'),
]

handler404 = 'home.views.custom_404'