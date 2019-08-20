from datetime import datetime
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import HStoreField


class User(AbstractUser):
    """
    Basic User class for boards extending the original django User class 
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=256, unique=True)
    username = models.CharField(max_length=54, unique=True)

    def __str__(self):
        return f"{self.email}"

    REQUIRED_FIELDS = ('username',)
    USERNAME_FIELD = 'email'


class Board(models.Model):
    """
    Model representing a board. Uses a manager for creation of instances. 
    To create new board, use: Board.objects.create_board(title, members)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=20)
    members = models.ManyToManyField('boards.User', related_name='boards')
    scores = HStoreField(default=dict, null=True, blank=True)

    def add_member(self, user):
        if user in self.members.all():
            raise ValueError(f'Member {user.email} already exists')
        self.members.add(user)
        self.scores[user.email] = datetime.now()
        self.save()

    def remove_member(self, user):
        if user not in self.members.all():
            raise ValueError(f'Member {user.email} does not belong to this board')
        self.members.remove(user)
        del self.scores[user.email]
        self.save()

    def reset_score(self, email, last_time=None):
        if last_time is None:
            last_time = datetime.now()
        self.scores[email] = last_time
        self.save()

    def __str__(self):
        return "-".join([self.title, str(self.id)])
