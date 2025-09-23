from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from users.views import SignupView
from community.views import PostViewSet, CommentViewSet
from videos.views import (
    VideoViewSet, 
    LikeToggleView, 
    stream_video, 
    IncrementViewCountView, 
    WeeklyPopularVideosView
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'videos', VideoViewSet, basename='video')

videos_router = routers.NestedDefaultRouter(router, r'videos', lookup='video')
videos_router.register(r'comments', CommentViewSet, basename='video-comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/videos/weekly-popular/', WeeklyPopularVideosView.as_view(), name='weekly-popular'),
    path('api/videos/<int:video_pk>/like/', LikeToggleView.as_view(), name='like-toggle'),
    path('api/videos/<int:video_pk>/view/', IncrementViewCountView.as_view(), name='increment-view-count'),
    path('api/', include(router.urls)),
    path('api/', include(videos_router.urls)),
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('stream/<int:pk>/', stream_video, name='video-stream'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)