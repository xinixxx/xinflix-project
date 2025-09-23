from rest_framework import serializers
from django.urls import reverse # day 16 추가
from .models import Video, Like

class VideoSerializer(serializers.ModelSerializer):
    # uploader 필드를 읽기 전용으로 설정, 그리고 업로드한 사람의 username 을 보여준다
    uploader_username = serializers.ReadOnlyField(source='uploader.username')

    # 좋아요 개수를 계산해서 보내줄 필드
    like_count = serializers.SerializerMethodField()
    # 현재 요청을 보낸 사용자가 좋아요를 눌렀는지 여부를 보내줄 필드
    is_liked = serializers.SerializerMethodField()
    # 스트리밍 URL 을 위한 필드를 추가
    stream_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        # API를 통해 보여줄 필드 지정
        fields = [
            'id',
            'title',
            'description',
            'stream_url',
            'video_file',
            'thumbnail',
            'uploader_username',
            'created_at',
            'like_count',
            'is_liked',
            'view_count',
        ]
        # uploader 는 직접 입력받는 것이 아니라, 로그인한 사용자 외래키 지정됨
    # SerializerMethodField('like_count')의 값을 계산하는 메서드
    def get_like_count(self, obj):
        return obj.likes.count()


    # SerializerMethodField('is_liked')의 값을 계산하는 메서드
    def get_is_liked(self, obj):
        # self.context['request'].user 는 현재 요청을 보낸 사용자입니다.
        user = self.context['request'].user
        if user.is_authenticated:
            # 사용자가 로그인 한 경우, 현재 비디오(obj)에 대해 해당 사용자가 누른 '좋아요' 가 있는지 확인
            return Like.objects.filter(video=obj, user=user).exists()
        return False
    
    # stream_url 필드의 값을 만들어주는 메서드
    def get_stream_url(self, obj):
        request = self.context.get('request')
        # 'video-stream' 이라는 이름의 URL 패턴을 찾아서 전체 URL을 생성합니다
        # obj.pk는 현재 비디오의 id
        return request.build_absolute_uri(reverse('video-stream', kwargs={'pk': obj.pk}))
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'