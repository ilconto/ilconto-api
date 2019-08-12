from django.test import TestCase
import datetime
from ..models import User, Board
from ..serializers import(
    UserSerializer, 
    BoardSerializer,
    UserSerializerWithBoards,
)


class TestUserSerializers(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            'username': 'testeur',
            'email': 'test@test.com',
            'password': 'testpassword123'
        }
        cls.board_data = {
            'title': 'hello board'
        }
        cls.user = User.objects.create_user(**cls.user_data)
        cls.user.save()
        cls.board = Board.objects.create(**cls.board_data)
        cls.board.save()
        cls.board.add_member(cls.user)
        cls.serialized_user = UserSerializer(cls.user)
        cls.serialized_user_with_boards = UserSerializerWithBoards(cls.user)

    def test_serializes_user_with_full_data(self):
        """
        Checks if the serializer will only return the correct fields
        """
        serialized_from_user_data = UserSerializer(data=self.user_data)
        self.assertTrue(serialized_from_user_data.is_valid())
        self.assertDictContainsSubset({
            "username": self.user_data['username'],
            "email": self.user_data['email']
        }, self.serialized_user.data)
        self.assertNotIn("password", self.serialized_user.data.keys())

    def test_serializes_user_without_username(self):
        data = dict((k, self.user_data[k]) for k in ['email', 'password'])
        self.assertTrue(UserSerializer(data=data).is_valid())

    def test_cannot_serialize_without_email(self):
        data = dict((k, self.user_data[k]) for k in ['username', 'password'])
        self.assertFalse(UserSerializer(data=data).is_valid())
    
    def test_cannot_serialize_without_password(self):
        data = dict((k, self.user_data[k]) for k in ['email', 'username'])
        self.assertFalse(UserSerializer(data=data).is_valid())

    def test_serializes_user_with_board(self):
        """
        Checks if the representation of a board is the user board details matches the UserSerializer
        """
        boards_list = self.serialized_user_with_boards.data['boards']
        board_members = boards_list[0]['members']

        # Check if the "boards" field has the expected number of boards (1)
        # and if the "members" field of this board serialization has 1 member
        self.assertEqual(len(boards_list), 1)
        self.assertEqual(len(board_members), 1)

        # Check if the user within the board members list is correctly represented
        for label in ['username', 'email']:
            self.assertIn(label, board_members[0])
            self.assertEqual(self.user_data[label], board_members[0][label])
        self.assertIn('id', board_members[0])


class TestBoardSerializer(TestCase):
    """
    Aucune idée de comment tester ça
    """
    pass
        