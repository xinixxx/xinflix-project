from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser # 파일 파서 import
from .models import Video
from .serializers import VideoSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # parser_classes 설정: MultiPartParser 와 FormParser 를 추가하여 동영상, 이미지같은 multi-part form data 를 처리할 수 있도록 함
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # 게시판에서 했던 것처럼, 현재 로그인한 사용자를 uploader로 자동 설정
        serializer.save(uploader=self.request.user)