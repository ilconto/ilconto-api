from django.test import TestCase
from datetime import datetime
from ..models import User, Board
from ..serializers import UserSerializer, BoardSerializer


class TestUserSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User(username="testuser", password="pass123",
                    email="test@example.com")
        user.save()

    def test_serializes_user(self):
        user = User.objects.first()
        serialized_user = UserSerializer(user)
        self.assertDictContainsSubset({
            "username": "testuser", "email": "test@example.com"}, serialized_user.data)
        self.assertNotIn("password", serialized_user.data.keys())
