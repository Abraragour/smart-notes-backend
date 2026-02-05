"""
URL configuration for smart_notes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import NoteListApi, NoteDetailApi, RegisterApi, LoginApi

urlpatterns = [

    path('notes/', NoteListApi.as_view(), name='note-list'),
    
    
    path('notes/<int:pk>/', NoteDetailApi.as_view(), name='note-detail'),
    
    
    path('register/', RegisterApi.as_view(), name='register'),
    path('login/', LoginApi.as_view(), name='login'),
]