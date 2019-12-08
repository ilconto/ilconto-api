from django.contrib import admin
from django.urls import path, include

from rest_auth.registration.views import VerifyEmailView, RegisterView


urlpatterns = [
    path("api/v1/", include('boards.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/v1/rest-auth/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('api/v1/rest-auth/account-confirm-email/<key>/', VerifyEmailView.as_view(), name='account_confirm_email'),
]
