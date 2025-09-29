from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = "requests.log"

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"

        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        # ✅ File will be created automatically if it doesn't exist
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

        response = self.get_response(request)
        return response
                  
