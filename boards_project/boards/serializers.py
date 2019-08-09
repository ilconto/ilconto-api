from datetime import datetime

from rest_framework import serializers
from .models import Board, User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=256, required=False)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'id')


class BoardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    scores = serializers.JSONField()
    members = UserSerializer(many=True)

    class Meta:
        model = Board
        fields = ('id', 'title', 'scores', 'members',)

    def create(self, validated_data):
        print(validated_data)
        members_data = validated_data.pop('members')
        board = Board.objects.create(**validated_data)

        if self.context['request'].user not in members_data:
            user = self.context['request'].user
            board.members.add(user)
            board.scores[user.email] = validated_data['scores'].get(user.email, datetime.now().timestamp())

        for member in members_data:
            try:
                user = User.objects.get(email=member)
                board.members.add(user)
                board.scores[member] = validated_data['scores'].get(member, datetime.now())
            except User.DoesNotExist:
                pass
        
        board.save()

        return board


class UserSerializerWithBoards(serializers.ModelSerializer):
    boards = BoardSerializer(many=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'boards')
