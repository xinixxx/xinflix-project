from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer

class SignupView(APIView):
    def post(self, request):
        #request.data 를 UserSerializer 로 전달하여 유효성검사를 합니다.
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() # 유효하면 저장 (내부적으로 create 메서드 호출)
            return Response({'message': '회원가입이 성공적으로 완료되었습니다.'}, status=status.HTTP_201_CREATED)
        # 유효하지 않으면 에러 메시지를 반환합니다.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)