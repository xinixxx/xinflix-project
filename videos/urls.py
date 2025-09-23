from django.urls import path
from .views import LikeToggleView, stream_video, IncrementViewCountView, WeeklyPopularVideosView

urlpatterns = [
    path('<int:video_pk>/like/', LikeToggleView.as_view(), name='like-toggle'),
    path('<int:video_pk>/view/', IncrementViewCountView.as_view(), name='increment-view-count'),
    path('weekly-popular/', WeeklyPopularVideosView.as_view(), name='weekly-popular'),
    path('stream/<int:pk>/', stream_video, name='video-stream'),
]