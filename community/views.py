from rest_framework import viewsets
# IsAuthenticatedOrReadOnly: 인증된 사용자는 모든 요청(쓰기 포함) 가능, 비인증 사용자는 읽기만 가능
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # 이 ViewSet 에 관한 접근 관한 설정
    permission_classes = [IsAuthenticatedOrReadOnly]

    # perform_create는 ModelViewSet 에서 객체를 생성할 때 호출되는 메서드
    # 이 메서드를 오버라이드하여 'author' 필드를 현재 로그인한 사용자로 자동 설정
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Create your views here.
