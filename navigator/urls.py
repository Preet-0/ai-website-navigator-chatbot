from django.urls import path
from navigator import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chat/', views.chat, name='chat'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]