from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import HStoreField


class User(AbstractUser):
    """
    Basic User class for boards extending the original django User class 
    """
    email = models.EmailField(max_length=256, unique=True)
    username = models.CharField(max_length=54, unique=True)

    def __str__(self):
        return f"{self.email}"

    REQUIRED_FIELDS = ('username',)
    USERNAME_FIELD = 'email'


class BoardManager(models.Manager):
    """
    See usage in docs from Board model
    """

    def create_board(self, title, members):
        board = self.create(title=title)
        for member in members:
            board.scores[str(member.username)] = str(datetime.now())
            board.members.add(member)
        return board


class Board(models.Model):
    """
    Model representing a board. Uses a manager for creation of instances. 
    To create new board, use: Board.objects.create_board(title, members)
    """
    title = models.CharField(max_length=20)
    members = models.ManyToManyField('boards.User', related_name='boards')
    scores = HStoreField(default=dict, null=True, blank=True)
    objects = BoardManager()

    def add_member(self, user):
        self.members.add(user)
        self.scores[user.username] = datetime.now()
        self.save()

    def reset_score(self, username, last_time=None):
        if not last_time:
            last_time = datetime.now()
        self.scores[username] = last_time
        self.save()

    def __str__(self):
        return self.title
