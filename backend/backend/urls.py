from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# import settings, static, media stuff


urlpatterns = [
    path('admin/', admin.site.urls),
    # Login, Logout, Password Change, etc.
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/',
         include('dj_rest_auth.registration.urls')),  # Signup
    path('api/v1/campaigns/', include('campaigns.urls')),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
