from django.test import TestCase
from datetime import datetime
import pytz
from .models import Member, User, Board
from django.db.utils import IntegrityError


class TestUserModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(username='hello', email='test@test.com', password='oups')
        u.save()
    
    def test_user_is_created(self):
        self.assertEqual(User.objects.count(), 1)
        u = User.objects.first()
        self.assertEqual(u.username, 'hello')
        self.assertEqual(u.email, 'test@test.com')
        self.assertTrue(u.check_password('oups'))

    def test_cannot_create_with_same_email(self):
        with self.assertRaises(IntegrityError) :
            duplicated_user = User.objects.create_user(username="goodbye", email='test@test.com', password="test")

    def test_can_change_username(self):
        u = User.objects.first()
        self.assertEqual(u.username, 'hello')
        u.username = 'hello2'
        u.save()
        self.assertEqual(User.objects.first().username, 'hello2')
        u.username = 'hello'
        u.save()

    def test_can_change_username(self):
        u = User.objects.first()
        u.set_password('hello2')
        u.save()
        self.assertTrue(User.objects.first().check_password('hello2'))
        u.password = 'oups'
        u.save()

    def test_can_delete_user(self):
        u = User.objects.create_user(username='hello2', email='test2@test.com', password='oups')
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

    def test_adds_member_to_board(self):
        user1 = User.objects.create_user(username="paul", email="test@example.com", password="test")  
        user1.save()
        user2 = User.objects.create_user(username="max", email="test2@example.com", password="test")
        user2.save()
        board = Board.objects.first()
        member1 = Member(user=user1, name=user1.username, last_reset=datetime.now(pytz.utc), board=board)
        member2 = Member(user=user2, name=user2.username, last_reset=datetime.now(pytz.utc), board=board)
        member1.save()
        member2.save()
        an_other_board = Board(title="an other board")
        an_other_board.save()
        member3 = Member(user = user1, name = user1.username, last_reset = datetime.now(pytz.utc), board = an_other_board)
        member3.save()
        self.assertEqual(Member.objects.filter(board=board).count(), 2)
        self.assertEqual(Member.objects.filter(board=an_other_board).count(), 1)

class TestMemberModel(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.board = Board(title="my board")
        cls.board.save()
        cls.user = User.objects.create_user(username = "john", email="test@example.com", password = "oups")
        cls.user.save()

    def test_creates_member(self):
        m = Member(user=self.user, name="john", last_reset=datetime.now(pytz.utc), board=self.board)
        m.save()
        self.assertEqual(Member.objects.count(), 1)

    def test_cannot_create_member_without_board(self):
        with self.assertRaises(IntegrityError) :
            m = Member(user=self.user, name="john", last_reset=datetime.now(pytz.utc))
            m.save()
        