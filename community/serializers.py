from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # author 필드를 읽기 전용으로 설정하고, 사용자의 username 을 보여주도록 합니다.
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        # API에 포함될 필드를 지정합니다.
        fields = ['id', 'author_username', 'title', 'content', 'created_at', 'updated_at']
        # author 필드는 API 를 통해 직접 받지 않고, 요청한 사용자(로그인된 사용자)를 기반으로 자동 설정할 것이라 fields 에 미포함