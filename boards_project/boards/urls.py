from django.urls import path
from .views import BoardDetailsView, UserProfileView, ListCreateBoardsView
from .models import Board


urlpatterns = [
    path('boards/', ListCreateBoardsView.as_view(), name='boards'),
    path("boards/details/<int:pk>/", BoardDetailsView.as_view(), name='board_details'),
    path("profile/", UserProfileView.as_view(), name='user_profile'),
]
