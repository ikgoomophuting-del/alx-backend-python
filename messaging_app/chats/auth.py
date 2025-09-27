# messaging_app/chats/auth.py
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Optional custom JWT auth class.
    Can override authenticate() if you need custom behavior.
    """
    def authenticate(self, request):
        return super().authenticate(request)
