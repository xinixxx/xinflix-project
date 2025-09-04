from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model() # settings.py 에서 설정한 AUTH_USER_MODEL 을 가져오기

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','email', 'nickname')
        extra_kwargs = {'password':{'write_only':True}} # 비밀번호는 응답에 포함되지 않도록 함

    def create(self, validated_data):
        # validated_data 에 있는 값들을 사용해서 새로운 User 인스턴스를 생성하려고 함
        # create_user 메서드는 비밀번호를 자동으로 해싱(암호화) 해줌
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            nickname=validated_data.get('nickname', ''),
            password=validated_data['password']
        )
        return user