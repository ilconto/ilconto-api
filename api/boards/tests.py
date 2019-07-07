from django.test import TestCase

from .models import Member, User, Board 


class EntryModelTest(TestCase):

    def test_create_board(self):
        b = Board(title='hello board')
        self.assertEqual(b.title, 'hello board')
