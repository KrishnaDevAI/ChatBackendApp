"""
URL configuration for ChatApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from my_app.views import google_login, login_user, logout_user, register_user, run_task

urlpatterns = [
    path('run_task/', run_task, name='run_task'),
    path('api/auth/login/', login_user, name='api_login'),
    path('api/auth/logout/', logout_user, name='api_logout'),
    path('api/auth/register/', register_user, name='api_register'),
    path('api/auth/google/', google_login, name='api_google'),
]
