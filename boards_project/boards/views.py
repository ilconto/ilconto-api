from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from .models import Board, User
from .serializers import BoardSerializer, UserSerializerWithBoards
from .permissions import IsBoardMember, IsCurrentUser


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


class BoardDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsBoardMember,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return Response(UserSerializerWithBoards(request.user).data)
