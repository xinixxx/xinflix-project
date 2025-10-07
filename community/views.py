from rest_framework import viewsets, permissions
# IsAuthenticatedOrReadOnly: 인증된 사용자는 모든 요청(쓰기 포함) 가능, 비인증 사용자는 읽기만 가능
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from videos.models import Video

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    # 이 ViewSet 에 관한 접근 관한 설정
    permission_classes = [IsAuthenticatedOrReadOnly]

    # perform_create는 ModelViewSet 에서 객체를 생성할 때 호출되는 메서드
    # 이 메서드를 오버라이드하여 'author' 필드를 현재 로그인한 사용자로 자동 설정
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Create your views here.
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        # URL에 video_pk가 있으면 비디오 댓글을, post_pk가 있으면 게시글 댓글을 필터링
        if 'video_pk' in self.kwargs:
            return self.queryset.filter(content_type__model='video', object_id=self.kwargs['video_pk'])
        elif 'post_pk' in self.kwargs:
            return self.queryset.filter(content_type__model='post', object_id=self.kwargs['post_pk'])
        return self.queryset.none() # 둘 다 없으면 빈 쿼리셋 반환

    def perform_create(self, serializer):
        content_object = None
        if 'video_pk' in self.kwargs:
            content_object = Video.objects.get(pk=self.kwargs['video_pk'])
        elif 'post_pk' in self.kwargs:
            content_object = Post.objects.get(pk=self.kwargs['post_pk'])
        
        serializer.save(author=self.request.user, content_object=content_object)