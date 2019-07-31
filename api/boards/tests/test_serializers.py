from django.test import TestCase
from datetime import datetime
from ..models import Member, User, Board
from ..serializers import BoardSerializer


class TestBoardSerializer(TestCase):

    def test_serializes_board_with_members(self):
        board = Board(title="test")
        board.save()
        user1 = User.objects.create_user(
            username="paul", email="test@example.com", password="test")
        member1 = Member(user=user1, board=board, last_reset=datetime.now())
        member1.save()
        user2 = User.objects.create_user(
            username="maxence", email="test2@example.com", password="test2")
        member2 = Member(user=user2, board=board, last_reset=datetime.now())
        member2.save()
        serialized_board = BoardSerializer(board)
        self.assertIn("members", serialized_board.data)
        members = serialized_board.data["members"]
        boards_users = [member["user"]["username"] for member in members]
        self.assertIn("paul", boards_users)
        self.assertIn("maxence", boards_users)
