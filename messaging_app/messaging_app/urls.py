# messaging_app/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),         # conversations + nested messages
    path('api-auth/', include('rest_framework.urls')),  # for login/logout in DRF browsable API
]

# messaging_app/urls.py
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Existing app routes
    path('api/', include('chats.urls')),
    path('api/', include('listings.urls')),  # from Airbnb Clone API
]
