from datetime import datetime


from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from django.shortcuts import get_object_or_404


from .models import Board, AppUser, BoardMember
from .serializers import (
    BoardSerializer,
    AppUserSerializer,
    MemberSerializer,
)
from .permissions import IsBoardMember, IsCurrentUser


""" ===============================
============ Board views ==========
=============================== """
class ListCreateBoardsView(generics.ListCreateAPIView):
    """
    This view extends the generic ListCreateAPIView, overriding it's get_queryset method
    User has to be authenticated. If the user is part of the staff group, he is able to see
    every boards.
    Otherwise, he can only get the boards which he is a member of.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BoardSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Board.objects.all()
        else:
            board_ids = [item.board_id for item in self.request.user.memberships.all()]
            return Board.objects.filter(id__in=board_ids)


class RetrieveUpdateDeleteBoardsView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view deals with retrieving a board and deleting it, as well as basic
    updates (title). For updating board members, a custom view is used.
    """
    permission_classes = (IsBoardMember,)
    queryset = Board.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ('PUT',):
            return BoardPartialSerializer
        else:
            return BoardSerializer


class ListCreateBoardMembersView(generics.ListCreateAPIView):
    """
    This view deals with adding and listing board members
    """

    permission_classes = (IsBoardMember,)
    serializer_class = MemberSerializer
    
    def get_queryset(self):
        board_id = self.kwargs['board_id']
        board = get_object_or_404(Board.objects.all(), id=board_id)
        return board.members.all()

    def create(self, request, board_id):
        pass


class RetrieveUpdateDeleteBoardMembersView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view deals with retrieving a member infos, updating it's score, or deleting it
    """
    permission_classes = (IsBoardMember,)
    serializer_class = AppUserSerializer
    
    def retrieve(self, request, board_id, member_id):
        pass

    def update(self, request, board_id, member_id):
        pass

    def delete(self, request, board_id, member_id):
        pass


class RetrieveAppUserView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AppUserSerializer
    queryset = AppUser.objects.all()