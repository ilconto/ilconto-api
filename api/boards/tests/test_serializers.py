from django.test import TestCase
from datetime import datetime
from ..models import Member, User, Board
from ..serializers import BoardSerializer


class TestBoardSerializer(TestCase):

    def test_serializes_board_with_members(self):
        board = Board(title="test")
        user = User.objects.create_user(
            username="paul", email="test@example.com", password="test")
        member = Member(user=user, board=board, last_reset=datetime.now())
        serialized_board = BoardSerializer(board)
        self.assertIn("members", serialized_board.data)
