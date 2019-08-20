from datetime import datetime


from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from django.shortcuts import get_object_or_404


from .models import Board, User
from .serializers import (
    BoardSerializer,
    BoardPartialSerializer,
    UserSerializer,
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
            return self.request.user.boards.all()


class  RetrieveUpdateDeleteBoardsView(generics.RetrieveUpdateDestroyAPIView):
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
    This views deals with adding and listing board members
    """

    permission_classes = (IsBoardMember,)
    serializer_class = MemberSerializer
    
    def get_queryset(self):
        board_id = self.kwargs['board_id']
        board = get_object_or_404(Board.objects.all(), id=board_id)
        return board.members.all()


    def create(self, request, board_id):
        board = get_object_or_404(Board.objects.all(), id=board_id)
        board_members = board.members.all()

        serialized_user = UserSerializer(data=request.data['user'])
        score = request.data.get('scores', datetime.now())

        if serialized_user.is_valid():
            new_member = serialized_user.validated_data
            try:
                email = new_member['email']
                user = User.objects.get(email=email)
                board.add_member(user)
                board.reset_score(email, score)
            except User.DoesNotExist:
                # That's where we'll implement the email to non-existing members feature
                # @TODO: Implement it !
                pass
        else:
            pass

        return Response({
            "id": user.id,
            "email": user.email,
            "score": score
        })


class RetrieveUpdateDeleteBoardMembersView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view deals with retrieving a member infos, updating it's score, or deleting it
    """
    permission_classes = (IsBoardMember,)
    serializer_class = UserSerializer
    
    def retrieve(self, request, board_id, member_id):
        board = get_object_or_404(Board.objects.all(), id=board_id)
        board_member = get_object_or_404(board.members.all(), id=member_id)
        
        return Response({
            "member_details": MemberSerializer(board_member).data,
            "score": board.scores[board_member.email]
        })

    def update(self, request, board_id, member_id):
        board = get_object_or_404(Board.objects.all(), id=board_id)
        board_member = get_object_or_404(board.members.all(), id=member_id)

        ts = request.data.get('timestamp', datetime.timestamp(datetime.now()))
        score = datetime.fromtimestamp(ts)
        board.reset_score(board_member, score)

        return Response({
            "id": board_member.id,
            "email": board_member.email,
            "score": score
        })

    def delete(self, request, board_id, member_id):
        board = get_object_or_404(Board.objects.all(), id=board_id)
        board_member = get_object_or_404(board.members.all(), id=member_id)

        board.remove_member(board_member)

        return Response({
            "id": board_member.id
        })



class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return Response(UserSerializer(request.user).data)
