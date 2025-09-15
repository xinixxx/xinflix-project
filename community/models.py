from django.db import models
from django.conf import settings
# Post 모델을 import 합니다
from videos.models import Video

class Post(models.Model):
    # settings.AUTH_USER_MODEL 은 Django 가 인식하는 User 모델을 가리킨다.
    # on_delete=models.CASCADE 는 사용자가 삭제되면 그 사용자가 쓴 글도 모두 삭제된다는 의미
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    # auto_now_add = True 는 객체가 처음 생성될 때만 현재 날짜와 시간을 저장함
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now = True 는 객체가 저장될 때마다 현재 날짜와 시간으로 업데이트 됨
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Create your models here.
class Comment(models.Model):
    # 어떤 동영상에 달릴 댓글인지 (Video와 관계 설정)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    # 작정자 (Users 와 관계설정)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 댓글 내용
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.content[:10]}'