from django.test import TestCase
from datetime import datetime
import pytz
from ..models import Member, User, Board
from django.db.utils import IntegrityError


class TestUserModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(
            username='hello', email='test@test.com', password='oups')
        u.save()

    def test_user_is_created(self):
        self.assertEqual(User.objects.count(), 1)
        u = User.objects.first()
        self.assertEqual(u.username, 'hello')
        self.assertEqual(u.email, 'test@test.com')
        self.assertTrue(u.check_password('oups'))

    def test_cannot_create_with_same_email(self):
        with self.assertRaises(IntegrityError):
            duplicated_user = User.objects.create_user(
                username="goodbye", email='test@test.com', password="test")

    def test_can_change_username(self):
        u = User.objects.first()
        self.assertEqual(u.username, 'hello')
        u.username = 'hello2'
        u.save()
        self.assertEqual(User.objects.first().username, 'hello2')
        u.username = 'hello'
        u.save()

    def test_can_delete_user(self):
        u = User.objects.create_user(
            username='hello2', email='test2@test.com', password='oups')
        u.save()


class TestBoardModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.board_title = 'hello board'
        b = Board(title=cls.board_title)
        b.save()

    def test_board_is_created(self):
        self.assertEqual(Board.objects.count(), 1)
        b = Board.objects.first()
        self.assertEqual(b.title, self.board_title)

    def test_board_title_is_modified(self):
        b = Board.objects.first()
        self.assertEqual(b.title, self.board_title)
        b.title = 'goodbye board'
        b.save()
        del b
        b = Board.objects.first()
        self.assertEqual(b.title, 'goodbye board')
        b.title = self.board_title
        b.save()

    # def test_adds_member_to_board(self):
    #     pass
