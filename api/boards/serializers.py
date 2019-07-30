from rest_framework import serializers
from .models import Board, User, Member


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')


class MemberSerializer(serializers.Serializer):
    user = UserSerializer()
    last_reset = serializers.DateTimeField()

    class Meta:
        model = Member
        fields = ("user", "last_reset")


class BoardSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    id = serializers.IntegerField()
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['title', 'id', "members"]
