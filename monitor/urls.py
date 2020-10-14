# encoding: utf-8

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from monitor import views


router = DefaultRouter()
router.register(r'tokens', views.TokenViewSet)
router.register(r'leakages', views.LeakageViewSet)
router.register(r'tasks', views.TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
