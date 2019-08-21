from django.test import TestCase
import datetime
from ..models import AppUser, BoardMember, Board
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model


user_model = get_user_model()


class TestUserModel(TestCase):
    """
    WIP
    """
    pass


class TestBoardModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Creates an empty board and 2 users
        """
        cls.board_title = 'hello board'
        cls.users_data = [{
            'username': f'testeur_{i}',
            'email': f'test_{i}@test.com',
            'password': 'testpassword123'
        } for i in range(1, 6)]
        cls.users = [user_model.objects.create_user(**user_data) for user_data in cls.users_data]
        board = Board(title=cls.board_title)
        board.save()
        cls.board_id = board.id

    def test_board_is_created(self):
        b = Board.objects.get(id=self.board_id)
        self.assertEqual(b.title, self.board_title)

    def test_member_is_added_with_score(self):
        """
        Adds a member to the board, checks if it is in the members list with the right score
        Then, deletes it to reset state
        """
        # test data
        board = Board.objects.get(id=self.board_id)
        user = user_model.objects.get(email=self.users_data[0]['email'])

        # adds the member to the board and checks
        member = board.add_member('test_username', user.id, score=10)
        self.assertTrue(board.members.filter(id=member.id).exists())
        self.assertEqual(member.score, 10)

        # Cleans the board members field
        board.remove_member(member.id)

    def test_member_is_added_without_score(self):
        """
        Adds a member to the board without a score, checks if it is in the members list with the right score
        Then, deletes it to reset state
        """
        # test data
        board = Board.objects.get(id=self.board_id)
        user = user_model.objects.get(email=self.users_data[0]['email'])

        # adds the member to the board and checks
        member = board.add_member('test_username', user.id)
        self.assertTrue(board.members.filter(id=member.id).exists())
        self.assertEqual(member.score, board.members.get(id=member.id).score)

        # Cleans the board members field
        board.remove_member(member.id)

    def test_cannot_add_two_members_from_one_user(self):
        """
        Adds a member to the board, checks if adding him a second time raises a ValueError
        Then, deletes it to reset state
        """
        # test data
        board = Board.objects.get(id=self.board_id)
        user = user_model.objects.get(email=self.users_data[0]['email'])
        
        # Adds two members from the same user id
        member = board.add_member('test_username', user.id)
        with self.assertRaises(Exception):
            board.add_member('test_username_2', user.id)
        
        # cleans the board members field
        board.remove_member(member.id)

    def test_member_is_removed(self):
        """
        Add a member to the board, removes it, then checks if it is removed from members list and scores
        """
        # test data
        board = Board.objects.get(id=self.board_id)
        user = user_model.objects.get(email=self.users_data[0]['email'])

        # Add and then remove a member for the board. Checks each step of the process
        member = board.add_member('test_username', user.id)
        self.assertTrue(board.members.filter(id=member.id).exists())
        board.remove_member(member.id)
        self.assertFalse(board.members.filter(id=member.id).exists())

    def test_cannot_remove_unexitsting_member(self):
        """
        Check if removing a member not registered as board member raises a DoesNotExist error
        """
        board = Board.objects.get(id=self.board_id)
        with self.assertRaises(BoardMember.DoesNotExist):
            board.remove_member(board.id)

    def test_cannot_reset_unexitsting_member(self):
        """
        Check if removing a member not registered as board member raises a Board.DoesNotExist error
        """
        board = Board.objects.get(id=self.board_id)
        with self.assertRaises(BoardMember.DoesNotExist):
            board.reset_score(board.id)

    def test_member_is_resetted(self):
        """
        Adds a member to the board, resets it's score with 10 minutes ago, then checks if scores match
        """
        # test data
        board = Board.objects.get(id=self.board_id)
        user = user_model.objects.get(email=self.users_data[0]['email'])

        # Create a board and checks that current and resetted scores are different
        member = board.add_member('test_username', user.id)
        t = int((datetime.datetime.utcnow() - datetime.timedelta(minutes = 10)).timestamp())
        self.assertNotEqual(board.members.get(id=member.id).score, t)

        # Reset the member score and checks if it matches now
        board.reset_score(member.id, t)
        self.assertEqual(board.members.get(id=member.id).score, t)
        board.remove_member(member.id)


    def test_board_title_is_modified(self):
        # test data
        new_board_title = 'goodbye board'
        board = Board.objects.get(id=self.board_id)
        self.assertEqual(board.title, self.board_title)

        # update board title
        board.title = new_board_title
        board.save()
        del board
        
        # Checks if the update happened and reset board state afterwards
        board = Board.objects.get(id=self.board_id)
        self.assertEqual(board.title, new_board_title)
        board.title = self.board_title
        board.save()