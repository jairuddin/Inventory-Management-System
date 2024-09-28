from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')

        if token is None:
            return None  # No token found in cookies, Django handles auth failure

        try:
            validated_token = self.get_validated_token(token)  # Validate the JWT token
            return self.get_user(validated_token), validated_token
        except AuthenticationFailed:
            return None  # Invalid token
