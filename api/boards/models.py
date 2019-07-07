from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Basic User class for boards extending the original django User class 
    """
    pass


class Member(models.Model):
    """
    Model representing the member of a board. Linked to a user object
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    last_rest = models.DateTimeField()


class Board(models.Model):
    """
    Model representing a board
    """
    title = models.CharField(max_length=20)
    members = models.ManyToManyField('boards.Member')