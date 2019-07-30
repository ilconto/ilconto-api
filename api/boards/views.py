from rest_framework.views import APIView
from .models import Board
from .serializers import BoardSerializer
from rest_framework.response import Response


class BoardList(APIView):

    def get(self, request):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self):
        pass
