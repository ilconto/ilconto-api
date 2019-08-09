from django.urls import path
from .views import BoardDetails, UserProfile
from .models import Board


urlpatterns = [
    path("boards/<pk>", BoardDetails.as_view()),
    path("profile", UserProfile.as_view())
]
