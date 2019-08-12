from django.test import TestCase
import datetime
import pytz
from ..models import User, Board
from django.db.utils import IntegrityError


class TestUserModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            'username': 'testeur',
            'email': 'test@test.com',
            'password': 'testpassword123'
        }
        cls.superuser_data = {
            'username': 'supertesteur',
            'email': 'supertest@test.com',
            'password': 'testpassword123'
        }
        u = User.objects.create_user(**cls.user_data)
        u.save()
        super_u = User.objects.create_superuser(**cls.superuser_data)
        super_u.save()

    def test_user_is_created(self):
        u = User.objects.get(email=self.user_data['email'])
        self.assertEqual(u.username, self.user_data['username'])
        self.assertEqual(u.email, self.user_data['email'])
        self.assertFalse(u.check_password('wrong password'))
        self.assertTrue(u.check_password(self.user_data['password']))
        self.assertFalse(u.is_staff)
        self.assertFalse(u.is_superuser)
    
    def test_superuser_is_created(self):
        super_u = User.objects.get(email=self.superuser_data['email'])
        self.assertEqual(super_u.username, self.superuser_data['username'])
        self.assertEqual(super_u.email, self.superuser_data['email'])
        self.assertFalse(super_u.check_password('wrong password'))
        self.assertTrue(super_u.check_password(self.superuser_data['password']))
        self.assertTrue(super_u.is_superuser)

    def test_cannot_create_with_same_email(self):
        with self.assertRaises(IntegrityError):
            _ = User.objects.create_user(
                username="Unexisting",
                email='test@test.com',
                password="testpassword123"
            )

    def test_can_change_username(self):
        new_username = self.user_data['username'] + ' changed'
        u = User.objects.get(email=self.user_data['email'])
        self.assertEqual(u.username, self.user_data['username'])
        u.username = new_username
        u.save()
        self.assertEqual(User.objects.get(email=self.user_data['email']).username, new_username)
        u.username = self.user_data['username']
        u.save()

    def test_can_change_password(self):
        new_password = 'testpassword456'
        u = User.objects.get(email=self.user_data['email'])
        self.assertTrue(u.check_password(self.user_data['password']))
        u.set_password(new_password)
        u.save()
        self.assertTrue(User.objects.get(email=self.user_data['email']).check_password(new_password))
        u.set_password(self.user_data['password'])
        u.save()

    def test_can_delete_user(self):
        data = {
            'username': 'testeur2',
            'email': 'test2@test.com',
            'password': 'testpassword123'
        }
        u = User.objects.create_user(**data)
        u.save()
        u = User.objects.get(email=data['email'])
        u.delete()
        with self.assertRaises(User.DoesNotExist):
            u = User.objects.get(email=data['email'])


class TestBoardModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Creates an empty board and 2 users
        """
        cls.board_title = 'hello board'
        cls.user_data1 = {
            'username': 'testeur',
            'email': 'test@test.com',
            'password': 'testpassword123'
        }
        cls.user_data2 = {
            'username': 'testeur2',
            'email': 'test2@test.com',
            'password': 'testpassword123'
        }
        user1 = User.objects.create_user(**cls.user_data1)
        user1.save()
        user2 = User.objects.create_user(**cls.user_data2)
        user2.save()
        board = Board(title=cls.board_title)
        cls.board_id = board.id
        board.save()

    def test_board_is_created(self):
        b = Board.objects.get(id=self.board_id)
        self.assertEqual(b.title, self.board_title)

    def test_member_is_added(self):
        """
        Adds a member to the board, checks if it is in the members list and scores
        Then, deletes it to reset state
        """
        board = Board.objects.get(id=self.board_id)
        user1 = User.objects.get(email=self.user_data1['email'])
        self.assertEqual(0, board.members.count())
        board.add_member(user1)
        self.assertEqual(1, board.members.count())
        self.assertIn(user1.email, board.scores.keys())
        board.remove_member(user1)

    def test_cannot_add_same_member_twice(self):
        """
        Adds a member to the board, checks if adding him a second time raises a ValueError
        Then, deletes it to reset state
        """
        board = Board.objects.get(id=self.board_id)
        user1 = User.objects.get(email=self.user_data1['email'])
        self.assertEqual(0, board.members.count())
        board.add_member(user1)
        with self.assertRaises(ValueError):
            board.add_member(user1)
        board.remove_member(user1)

    def test_member_is_removed(self):
        """
        Add a member to the board, removes it, then checks if it is removed from members list and scores
        """
        board = Board.objects.get(id=self.board_id)
        user1 = User.objects.get(email=self.user_data1['email'])
        board.add_member(user1)
        self.assertEqual(1, board.members.count())
        board.remove_member(user1)
        self.assertEqual(0, board.members.count())
        self.assertNotIn(user1.email, board.scores.keys())

    def test_cannot_remove_unexitsting_member(self):
        """
        Checkf if removing a member not registered as board member raises a ValueError
        """
        board = Board.objects.get(id=self.board_id)
        user1 = User.objects.get(email=self.user_data1['email'])
        with self.assertRaises(ValueError):
            board.remove_member(user1)

    def test_member_is_removed(self):
        """
        Add a member to the board, removes it, then checks if it is removed from members list and scores
        """
        board = Board.objects.get(id=self.board_id)
        user1 = User.objects.get(email=self.user_data1['email'])
        board.add_member(user1)
        self.assertEqual(1, board.members.count())
        board.remove_member(user1)
        self.assertEqual(0, board.members.count())
        self.assertNotIn(user1.email, board.scores.keys())

    def test_member_is_resetted(self):
        """
        Adds a member to the board, resets it's score with 10 minutes ago, then checks if scores match
        """
        board = Board.objects.get(id=self.board_id)
        user1 = User.objects.get(email=self.user_data1['email'])
        board.add_member(user1)
        t = datetime.datetime.now() - datetime.timedelta(minutes = 10)
        board.reset_score(user1.email, t)
        self.assertEqual(board.scores[user1.email], t)

    def test_board_title_is_modified(self):
        new_board_title = 'goodby board'
        board = Board.objects.get(id=self.board_id)
        self.assertEqual(board.title, self.board_title)
        board.title = new_board_title
        board.save()
        del board
        board = Board.objects.get(id=self.board_id)
        self.assertEqual(board.title, new_board_title)
        board.title = self.board_title
        board.save()