from django.urls import path
from .views import (
    ListCreateBoardsView,
    RetrieveUpdateDeleteBoardsView,
    ListCreateBoardMembersView,
    RetrieveUpdateDeleteBoardMembersView,
)
from rest_auth.views import UserDetailsView
from .models import Board


urlpatterns = [
    path('boards/', ListCreateBoardsView.as_view(), name='boards'),
    path("boards/<uuid:board_id>/", RetrieveUpdateDeleteBoardsView.as_view(), name='board_details'),
    path("boards/<uuid:board_id>/members/", ListCreateBoardMembersView.as_view(), name='board_members'),
    path("boards/<uuid:board_id>/members/<uuid:member_id>", RetrieveUpdateDeleteBoardMembersView.as_view(), name='board_member_details'),
    path("profile/", UserDetailsView.as_view(), name='user_profile'),
]
