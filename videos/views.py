from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser # 파일 파서 import
from .models import Video, Like, ViewCount
from .serializers import VideoSerializer, LikeSerializer

from django.http import FileResponse, HttpResponse, Http404
import os
import re

from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.db.models import Count, F
from rest_framework.generics import ListAPIView


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # parser_classes 설정: MultiPartParser 와 FormParser 를 추가하여 동영상, 이미지같은 multi-part form data 를 처리할 수 있도록 함
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # 게시판에서 했던 것처럼, 현재 로그인한 사용자를 uploader로 자동 설정
        serializer.save(uploader=self.request.user)
    
    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):

        """
        특정 동영상과 관련된 동영상 목록을 반환합니다.
        (현재 단순히 현재 동영상을 제외한 나머지 동영상 5개를 반환)
        """
        # 현재 보고있는 동영상 객체를 가져옵니다
        current_video = self.get_object()

        # 현재 동영상을 제외(execlude) 한 나머지 동영삳을을 최신순으로 정렬하고, 최대 5개까지만 가져온다
        related_videos = Video.objects.exclude(pk=current_video.pk).order_by('-created_at')[:5]

        # 가져온 동영상 목록을 직렬화(serialize) 합니다
        # many=True 는 여러개의 객체를 직력화 할 때 필요합니다
        serializer = self.get_serializer(related_videos, many=True)

        return Response(serializer.data)


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

class IncrementViewCountView(APIView):
    def post(self, request, video_pk):
        try:
            video = Video.objects.get(pk=video_pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # 언제 조회되었는지 기록
        ViewCount.objects.create(video=video)
        # Video 모델의 전체 조회수 1 증가(F() 표현식으로 동시성 문제 방지)
        Video.objects.filter(pk=video_pk).update(view_count=F('view_count')+1)
        return Response(status=status.HTTP_200_OK)

class WeeklyPopularVideosView(APIView):
    # 이 View는 인증이 필요 없으므로 permission_classes를 설정하지 않습니다.
    def get(self, request):
        seven_days_ago = timezone.now() - timedelta(days=7)
        
        queryset = Video.objects.annotate(
            weekly_views=Count('view_counts', filter=models.Q(view_counts__viewed_at__gte=seven_days_ago))
        ).order_by('-weekly_views')[:4]
        
        # queryset을 직접 직렬화(serialize)하여 반환합니다.
        # context={'request': request}는 SerializerMethodField에서 request 객체를 사용하기 위해 필요합니다.
        serializer = VideoSerializer(queryset, many=True, context={'request': request})
        
        return Response(serializer.data)


# 파일 크기를 쪼갤 단위 (예: 1MB)
CHUNK_SIZE = 1024 * 1024

def stream_video(request, pk):
    try:
        video = Video.objects.get(pk=pk)
    except Video.DoesNotExist:
        raise Http404
    
    # 동영상 파일의 정보를 가져옵니다.
    video_path = video.video_file.path
    file_size = os.path.getsize(video_path)

    # 요청 헤더에서 Range 정보를 읽어온다
    range_header = request.headers.get('range')
    if not range_header:
        # Range 헤더가 없으면, 파일 전체를 일반적인 방식으로 응답합니다.
        return FileResponse(open(video_path, 'rb'), content_type='video/mp4')

    # Range 헤더 파싱: "bytes=start-end"
    range_match = re.search(r'bytes=(\d+)-(\d*)', range_header)
    if not range_match:
        return HttpResponse("유효하지 않은 레인지 헤더입니다", status=400)
    
    start_byte, end_byte = range_match.groups()
    start_byte = int(start_byte)

    if end_byte:
        end_byte = int(end_byte)
    else:
        # 끝 바이트가 명시되지 않았다면 파일의 끌까지를 의미함
        end_byte = file_size - 1
    
    # 브라우저가 요청한 청크 크기만큼만 파일을 읽습니다.
    content_length = end_byte - start_byte + 1

    response = HttpResponse(status=206) # 206 Partial Content 상태 코드
    response['Content-Type'] = 'video/mp4'
    response['Content-Length'] = str(content_length)
    response['Accept-Ranges'] = 'bytes'
    response['Content-Range'] = f'bytes {start_byte}-{end_byte}/{file_size}'

    # FileResponse 를 사용하여 파일을 스트리밍합니다
    response.content = open(video_path, 'rb').read()[start_byte:end_byte+1]

    return response