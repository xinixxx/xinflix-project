from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

# DefaultRouter 를 먼저 생성합니다
router = DefaultRouter()
# 'posts' 라는 URL prefix 에 PostViewSet을 등록합니다
# 이제 router가 /posts/, /posts/{id}/ 등의 URL 을 자동으로 만들어 줌
router.register('posts',PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]