from rest_framework import permissions

class IsUploaderOrReadOnly(permissions.BasePermission):
    # 객체의 uploader 만 수정/삭제를 허용하고 그 외에는 읽기만 허용하는 커스텀 권한
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        # 쓰기 요청(PUT, DELETE 등)은 객체의 uploader와 요청을 보낸 user가 동일할 때만 허용
        return obj.uploader == request.user