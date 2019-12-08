from datetime import datetime


from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from django.shortcuts import get_object_or_404


from .models import Board, AppUser, BoardMember
from .serializers import (
    BoardSerializer,
    AppUserSerializer,
    MemberSerializer,
)
from .permissions import (
    IsBoardMember,
    IsActivated,
    HasEmailVerified,
    IsInOnboarding
)


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
    permission_classes = (IsAuthenticated, IsActivated,)
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
    permission_classes = (IsAuthenticated, IsActivated, IsBoardMember,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    
    def get_object(self):
        return get_object_or_404(Board.objects.all(), id=self.kwargs['board_id'])


class ListCreateBoardMembersView(generics.ListCreateAPIView):
    """
    This view deals with adding and listing board members
    """
    permission_classes = (IsAuthenticated, IsActivated, IsBoardMember,)
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
    permission_classes = (IsAuthenticated, IsActivated, IsBoardMember,)
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
        self.check_object_permissions(request, member)

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


from boards.forms import ActivateUserForm


class ActivateUserView(APIView):
    """
    This view is used when a user is added to a board without having an account on Ilconto
    Before he can access the content of the board, he has to go through a registration step
    - At the board's creation, an email is sent to the non-existing user
    - The email contains a link towards an activation page on the frontend
    - This page hits the api server with a POST request containing the missing data for
    creating his account, including the hash code provided in the email for checking his identity
    - Once the post request has been received, the view cannot be used anymore by this user, preventing
    account modification through this way.
    """
    permission_classes = (IsInOnboarding,)

    def permission_denied(self, request, message=None):
        # Do not check for authentication here
        raise exceptions.PermissionDenied(detail=message)

    def post(self, request, user_id):
        form = ActivateUserForm(request.data)
        
        if form.is_valid():
            user_id = self.kwargs['user_id']
            user = get_object_or_404(AppUser.objects.all(), id=user_id)

            user.username = form.data['username']
            user.set_password(form.data['password1'])
            user.is_activated = True
            user.email_verified = True
            user.save()

            return Response(AppUserSerializer(user).data)
        
        return Response(form.errors.as_json())