from datetime import datetime
import json

from rest_framework import serializers
from .models import Board, User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=256, required=False)
    email = serializers.EmailField(max_length=256, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'boards')
        required_fields = ('email',)
        read_only_fields = ('id', 'boards', 'email',)


class UserCompactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=256, required=False)
    email = serializers.EmailField(max_length=256, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'id',)
        read_only_fields = ('id', 'email',)


class BoardSerializer(serializers.ModelSerializer):
    scores = serializers.JSONField(required=False)
    members = UserCompactSerializer(many=True, required=False)

    class Meta:
        model = Board
        fields = ('id', 'title', 'scores', 'members',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        """
        This function is triggered during access to the create view
        Classic attributes are set as usual (basically this is just the board's title)
        For members and scores:
        - The requesting user is added to the baord members by default
        !!! IMPORTANT !!! : This should be mentionned as a warning in the front applciation
        - The dates in the "scores" attribute of validated_data are used for members last reset
        initialization if provided. Otherwise the last reset time of a member is set to
        datetime.datetime.now().
        
        Additional possible feature : Something should happen if one the key in the scores dict does not
        match with any of the members email provided.
        """

        """

        This part should be using only a json for the members + scores combination, instead of
        separate data structures for members and scores. But I don't know how to orchestrate such
        a feature regarding django-rest-framework yet.

        """
        members_data = validated_data.pop('members', [])
        scores_data = validated_data.pop('scores', {})
        board = Board.objects.create(**validated_data)
        board.save()

        if self.context['request'].user not in members_data:
            user = self.context['request'].user
            board.add_member(user)
            board.reset_score(user.email, scores_data.get(user.email, datetime.now()))

        for member in members_data:
            try:
                email = member['email']
                user = User.objects.get(email=email)
                board.add_member(user)
                board.reset_score(email, scores_data.get(email, datetime.now()))
            except User.DoesNotExist:
                # That's where we'll implement the email to non-existing members feature
                # @TODO: Implement it !
                pass

        return board

    def update(self, instance, validated_data):
        """
        This function is triggered during access to the update view.
        Behaviours:
        - If there is only classic attributes that are updated -> the update is performed as usual
        - If the "members" attribute is different:
            - New members are added to the board
            - Deleted members are deleted from the board
        - For each members in the new "members" attribute:
            - If no last reset is provided -> the last_reset is set to the last value in the scores infos,
            or it is set to datetime.datetime.now() if it is a new member.
            - Otherwise, the value of last_reset is set to the value contained in the scores attributes if and
            only if the user requesting a modification matches the member email.
        
        Additional possible feature: Add a 403 response when trying to modify the score of another member
        """

        # Basic attribute modification
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        # Members management
        members_data = validated_data.get('members', instance.members.all())
        scores_data = validated_data.get('scores', {})

        for member in members_data:
            # Eventually update if member exists
            email = member['email']
            if instance.members.filter(email=email).exists():
                instance.reset_score(
                    email, 
                    scores_data.get(
                        email,
                        instance.scores[email]
                    )
                )
            # If user is not a member of the board yet, perform the add or register routine
            else:
                try:
                    user = User.objects.get(email=email)
                    instance.add_member(user)
                    instance.reset_score(email, scores_data.get(email, datetime.now()))
                except User.DoesNotExist:
                    # That's where we'll implement the email to non-existing members feature
                    # @TODO: Implement it !
                    pass

        return instance
