from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	# Django 의 기본 User 모델 (AbstractUser)
	# 나중에 닉네임, 프로필 사진 등 서비스에서만 필요한 필드를 추가할 때 여기에 작성
	# 예시) nickname = models.CharField(max_length=50, unique=True, null=True)
	
	# 지금은 추가기능 없이 기본기능만 사용하기 위해 pass 사용
    nickname = models.CharField(max_length=50, unique=True, null=True)