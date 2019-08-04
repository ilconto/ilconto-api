from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path("api/v1/", include('boards.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('api/v1/rest-auth/registration/',
         include('rest_auth.registration.urls')),
]
