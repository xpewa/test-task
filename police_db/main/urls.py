from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'crimes', views.CrimeViewSet, basename='crime')

urlpatterns = [
     path('', include(router.urls)),
]
