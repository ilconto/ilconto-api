from django.urls import path
from .views import BoardDetails
from .models import Board


urlpatterns = [
    path("boards/<pk>", BoardDetails.as_view())
]
