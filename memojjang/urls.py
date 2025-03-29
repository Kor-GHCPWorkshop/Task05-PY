"""
URL configuration for memojjang project.

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
from django.contrib import admin
from django.urls import path
from .apps.memos import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("memos/", views.memo_list, name="memo_list"),
    path("memos/create/", views.memo_create, name="memo_create"),
    path("memos/<int:pk>/", views.memo_detail, name="memo_detail"),
    path("memos/<int:pk>/edit/", views.memo_edit, name="memo_edit"),
    path("memos/<int:pk>/delete/", views.memo_delete, name="memo_delete"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
]


