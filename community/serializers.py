from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    # author 필드를 읽기 전용으로 설정하고, 사용자의 username 을 보여주도록 합니다.
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        # API에 포함될 필드를 지정합니다.
        fields = ['id', 'author_username', 'title', 'content', 'created_at', 'updated_at']
        # author 필드는 API 를 통해 직접 받지 않고, 요청한 사용자(로그인된 사용자)를 기반으로 자동 설정할 것이라 fields 에 미포함

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author_username', 'content', 'created_at', 'video']

        # video 필드는 URL 을 통해 자동으로 주압될 예정으로 사용자가 직접 읽지 못하도록 readonly 설정 하기

        extra_kwargs = {
            'video' : {'read_only':True},
        }