from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication


class UsernameAuthentication(BaseAuthentication):
    """X-USERNAME 헤더를 사용하여 사용자를 인증하는 클래스"""

    def authenticate(self, request):
        """
        X-USERNAME 헤더에서 username을 추출하여 사용자를 찾습니다.

        Returns:
            tuple: (user, None) - 사용자가 존재하는 경우
            None: 사용자가 없거나 헤더가 없는 경우
        """
        username = request.META.get("HTTP_X_USERNAME")

        if not username:
            return None

        try:
            user = User.objects.get(username=username)
            return (user, None)
        except User.DoesNotExist:
            return None
