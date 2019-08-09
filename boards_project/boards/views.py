from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


from .models import Board, User
from .serializers import BoardSerializer, UserSerializerWithBoards
from .permissions import IsBoardMember, IsCurrentUser


class BoardDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsBoardMember,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class UserProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return Response(UserSerializerWithBoards(request.user).data)
