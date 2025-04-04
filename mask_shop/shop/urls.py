from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import QualificationViewSet

router = DefaultRouter()
router.register(r'spec', QualificationViewSet, basename='qualification')

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('author/', views.author, name='author'),    
    path('', include(router.urls)),
]