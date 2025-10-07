from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_username',
            'title',
            'content',
            'created_at',
            'updated_at',
            'is_author'
        ]
        read_only_fields = ['author']

    def get_is_author(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.author == request.user
        return False

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = [
            'id', 
            'author',
            'author_username', 
            'content', 
            'created_at',
        ]
        read_only_fields = ['author']