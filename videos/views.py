from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser # 파일 파서 import
from .models import Video, Like
from .serializers import VideoSerializer, LikeSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # parser_classes 설정: MultiPartParser 와 FormParser 를 추가하여 동영상, 이미지같은 multi-part form data 를 처리할 수 있도록 함
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # 게시판에서 했던 것처럼, 현재 로그인한 사용자를 uploader로 자동 설정
        serializer.save(uploader=self.request.user)

class LikeToggleView(APIView):
    # '좋아요' 기능은 반드시 로그인한 사용자만 이용할 수 있도록 설정
    permission_classes = [IsAuthenticated]

    def post(self, request, video_pk):
        # URL에서 video_pk를 받아 해당하는 Video 객체를 가져옵니다.
        try:
            video = Video.objects.get(pk=video_pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # 현재 로그인한 사용자와 해당 비디오로 '좋아요' 객체를 찾습니다.
        # get_or_create: 객체가 있으면 가져오고(get), 없으면 새로 만듭니다(create).
        # created는 객체가 새로 생성되었는지 여부를 boolean 값(True/False)으로 알려줍니다.
        like_obj, created = Like.objects.get_or_create(user=request.user, video=video)

        if created:
            # '좋아요' 객체가 새로 생성되었다면 (created=True), '좋아요'가 눌린 것입니다.
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
        else:
            # 이미 존재했다면 '좋아요'를 취소하기 위해 객체를 삭제합니다.
            like_obj.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_204_NO_CONTENT)