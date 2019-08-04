from rest_framework import serializers
from .models import Board, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')


class BoardSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)

    class Meta:
        model = Board
        fields = ['title', 'id', "members"]
