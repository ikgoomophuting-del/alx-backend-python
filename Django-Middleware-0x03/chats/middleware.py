import logging
import time
from datetime import datetime
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from datetime import datetime


# Configure a file logger
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("requests.log")
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """
    Logs user requests with timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """
    Restricts access to the chat between 6PM and 9PM only.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Access allowed only between 18:00 (6 PM) and 21:00 (9 PM)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden(
                "Chat access is restricted between 6 PM and 9 PM only."
            )
        return self.get_response(request)


# In-memory request counter {ip: [timestamps]}
ip_requests = {}


class OffensiveLanguageMiddleware:
    """
    Limits chat message rate: 5 messages per minute per IP.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            current_time = time.time()
            time_window = 60  # 1 minute
            limit = 5  # messages per minute

            if ip not in ip_requests:
                ip_requests[ip] = []

            # Keep only recent timestamps (within 1 minute)
            ip_requests[ip] = [
                ts for ts in ip_requests[ip] if current_time - ts < time_window
            ]
            if len(ip_requests[ip]) >= limit:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Please wait before sending more messages."},
                    status=429
                )

            # Record this message
            ip_requests[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Retrieve the client IP address."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class RolePermissionMiddleware:
    """
    Restricts access to users who are 'admin' or 'moderator' only.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip check for unauthenticated users
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to access this section.")

        user_role = getattr(request.user, "role", None)

        if user_role not in ("admin", "moderator"):
            return HttpResponseForbidden("Access denied: insufficient permissions.")

        return self.get_response(request)

