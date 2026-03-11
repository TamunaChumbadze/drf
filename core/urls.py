# core/urls.py
# core/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from snippets.views import HomeView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Django auth (login/logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # DRF browsable API login
    path('api-auth/', include('rest_framework.urls')),

    # JWT token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Home page
    path('', HomeView.as_view(), name='home'),

    # Snippets app URLs (API & Web)
    path('snippets/', include('snippets.urls')),
]