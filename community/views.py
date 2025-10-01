from rest_framework import viewsets, permissions
# IsAuthenticatedOrReadOnly: 인증된 사용자는 모든 요청(쓰기 포함) 가능, 비인증 사용자는 읽기만 가능
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    # 이 ViewSet 에 관한 접근 관한 설정
    permission_classes = [IsAuthorOrReadOnly]

    # perform_create는 ModelViewSet 에서 객체를 생성할 때 호출되는 메서드
    # 이 메서드를 오버라이드하여 'author' 필드를 현재 로그인한 사용자로 자동 설정
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Create your views here.
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        
        video_id = self.kwargs.get('video_pk')
        serializer.save(
            author=self.request.user,
            video_id=video_id
        )
    
    # get_queryset 을 오버라이드하여 특정 영상에 달린 댓글만 필터링
    def get_queryset(self):
        # url로부터 vudeo_id 값을 가져와서, 해당 video 에 달린 댓글만 조회한다
        video_id = self.kwargs.get('video_pk')
        return super().get_queryset().filter(video_id=video_id)