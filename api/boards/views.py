from rest_framework.views import APIView
from .models import Board
from .serializers import BoardSerializer
from rest_framework.response import Response


class BoardView(APIView):

    def get(self, request, pk):
        board = Board.objects.get(pk=pk)
        serializer = BoardSerializer(board)
        response = Response(serializer.data)
        return response


class ProfileView(APIView):

    def get(self, request):
        pass
