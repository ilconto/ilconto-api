# from rest_framework.views import APIView, RetrieveUpdateDestroyAPIView
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Board
from .serializers import BoardSerializer
from .permissions import IsBoardMember


class BoardDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsBoardMember,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
