from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('login', views.LoginView, basename='login')

urlpatterns = [
    path('notification/', views.NotificationView.as_view()),
    path('emails/', views.EmailView.as_view()),
    path('signup/', views.SignupView.as_view()),
    path('', include(router.urls)),
]
