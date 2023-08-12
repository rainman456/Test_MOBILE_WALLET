from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
#from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

api_info=openapi.Info(
title="Vail API",
default_version='v1',
description="Test ",
)

schema_view = get_schema_view(

public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('transactions.urls')),
    path('', include('userwallets.urls')),
    path('', include('payments_app.urls')),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   
   
   # YOUR PATTERNS
    #path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    #path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    #path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
