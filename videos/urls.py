from django.urls import path, include
from rest_framework_nested import routers
from .views import VideoViewSet, LikeToggleView, stream_video
# community 앱의 CommentViewSet을 여기서 import 해야 합니다.
from community.views import CommentViewSet

# 1. 최상위 라우터를 생성합니다.
router = routers.SimpleRouter()
router.register(r'videos', VideoViewSet, basename='video')

# 2. 'videos' 라우터 아래에 중첩될 댓글 라우터를 생성합니다.
comments_router = routers.NestedDefaultRouter(router, r'videos', lookup='video')
comments_router.register(r'comments', CommentViewSet, basename='video-comments')

# 3. 두 라우터의 URL을 모두 urlpatterns에 포함시킵니다.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls)),
    path('videos/<int:video_pk>/like/', LikeToggleView.as_view(), name='like-toggle'),
    path('stream/<int:pk>/', stream_video, name='video-stream'),
]