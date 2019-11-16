# Core imports
import datetime
import uuid

# Django dependencies
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class AppUser(AbstractUser):
    """
    Basic User class for boards extending the original django User class 
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=256, unique=True)
    username = models.CharField(max_length=54, unique=True)
    email_verified = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=True)
    activation_hash = models.CharField(editable=False, max_length=20, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ('username',)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.email}"


class BoardMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=32)
    score = models.IntegerField()    # score = last time in UTC seconds
    user = models.ForeignKey('boards.AppUser', on_delete=models.CASCADE, related_name='memberships')
    board = models.ForeignKey('boards.Board', on_delete=models.CASCADE, related_name='members')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username} ({self.user.email})'


class Board(models.Model):
    """
    Model representing a board.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_member(self, member_username, user_id, score=None):
        user = AppUser.objects.get(id=user_id)

        if self.members.filter(user=user).exists():
            raise Exception(f'User {user} already exists in this board')

        if score is None:
            score = int(datetime.datetime.utcnow().timestamp())
        
        member = BoardMember.objects.create(
            username = member_username,
            score = score,
            user = user,
            board = self
        )
        self.members.add(member)
        return member

    def remove_member(self, member_id):
        member = self.members.get(id=member_id)
        id = member.id
        member.delete()
        return id

    def reset_score(self, member_id, score=None):
        member = self.members.get(id=member_id)
        if score is None:
            score = int(datetime.datetime.utcnow().timestamp())
        member.score = score
        member.save()
        return member

    def __str__(self):
        return "-".join([self.title, str(self.id)])
