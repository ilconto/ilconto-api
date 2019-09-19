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
from .permissions import IsBoardMember


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
            board_ids = [
                item.board_id for item in self.request.user.memberships.all()]
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
        # Retrieves the board where the new member is to be added
        board_id = self.kwargs['board_id']
        board = get_object_or_404(Board.objects.all(), id=board_id)

        # Retrieves user infos
        user_email = request.data['email']
        user = AppUser.objects.get(email=user_email)
        username = request.data.get('username', user.username)
        score = request.data.get('score', None)

        member = board.add_member(username, user.id, score)
        return Response(MemberSerializer(member).data)


class RetrieveUpdateDeleteBoardMembersView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view deals with retrieving a member infos, updating it's score, or deleting it
    """
    permission_classes = (IsBoardMember,)
    serializer_class = MemberSerializer

    def get_queryset(self):
        board_id = self.kwargs['board_id']
        board = get_object_or_404(Board.objects.all(), id=board_id)
        return board.members.all()

    def get_object(self):
        queryset = self.get_queryset()
        member_id = self.kwargs['member_id']
        member = get_object_or_404(queryset, id=member_id)
        return member

    def update(self, request, board_id, member_id):
        member = self.get_object()

        if 'score' in request.data:
            member.score = request.data['score']

        if 'username' in request.data:
            member.username = request.data['username']

        member.save()
        return Response(MemberSerializer(member).data)

    def delete(self, request, board_id, member_id):
        board = Board.objects.get(id=board_id)
        id = board.remove_member(member_id)
        return Response(f'Succesfully deleted member {id}')


""" ==============================================
============ Account confirmation views ==========
============================================== """

from allauth.account.signals import email_confirmed
from django.dispatch import receiver

@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    user.email_verified = True
    user.save()