from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet

router = DefaultRouter()
# 'videos'라는 URL prefix 에 VideoViewSet을 등록한다
router.register(r'', VideoViewSet, basename='video')

urlpatterns = [
    path('', include(router.urls)),
]