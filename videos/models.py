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



# Create your models here.
