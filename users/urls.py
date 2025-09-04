from django.urls import path
from .views import SignupView

urlpatterns = [
    # POST /api/users/signup/ 요청을 SignupView 가 처리하도록 설정하려고 함
    path('signup/', SignupView.as_view(), name='signup')
]