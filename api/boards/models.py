from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import HStoreField


class User(AbstractUser):
    """
    Basic User class for boards extending the original django User class 
    """
    class Meta(object):
        unique_together = ('email',)



    """
    See usage in docs from Board model
    """

    def create_board(self, title, members):
        return self.user.username + " - " + self.board.title


class Board(models.Model):
    """
    Model representing a board
    """
    title = models.CharField(max_length=20)
    scores = HStoreField()

    def __str__(self):
        return self.title
