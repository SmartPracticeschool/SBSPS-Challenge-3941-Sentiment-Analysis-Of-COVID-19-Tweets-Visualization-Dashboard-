
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('page2/', views.page2, name="page2"),

]
