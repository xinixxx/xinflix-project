from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    # uploader 필드를 읽기 전용으로 설정, 그리고 업로드한 사람의 username 을 보여준다
    uploader_username = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = Video
        # API를 통해 보여줄 필드 지정
        fields = [
            'id',
            'title',
            'description',
            'video_file',
            'thumbnail',
            'uploader_username',
            'created_at'
        ]
        # uploader 는 직접 입력받는 것이 아니라, 로그인한 사용자 외래키 지정됨