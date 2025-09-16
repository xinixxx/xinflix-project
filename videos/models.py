from django.db import models
from django.conf import settings

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    # FileFields 는 모든 파일을 업로드 할 수 있는 필드임
    # 'uploads/videos/' 는 파일이 저장될 하위 폴더 경로
    video_file = models.FileField(upload_to='uploads/videos/')

    # ImageField는 이미지 파일만 업로드 할 수 있는 필드
    thumbnail = models.ImageField(upload_to='uploads/thumbnails/')

    # uploader 는 업로드한 사람을 의미하며 user 모델과 연결됨
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    # 좋아요를 누른 사용자
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 좋아요를 받은 동영상
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    # Meta 클래스를 사용하여 제약 조건을 추가합니다.
    class Meta:
        # 'user'와 'video' 쌍이 항상 고유하도록(unique) 설정합니다.
        # 이렇게 하면 한 사용자가 같은 동영상에 여러 번 '좋아요'를 누르는 것을
        # 데이터베이스 수준에서 방지할 수 있습니다.
        unique_together = ('user', 'video')

# Create your models here.
