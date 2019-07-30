from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Basic User class for boards extending the original django User class 
    """
    class Meta(object):
        unique_together = ('email',)


class Member(models.Model):
    """
    Model representing the member of a board. Linked to a user object
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    last_reset = models.DateTimeField()
    board = models.ForeignKey(
        'boards.Board', related_name="members", on_delete=models.CASCADE)


class Board(models.Model):
    """
    Model representing a board
    """
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title
