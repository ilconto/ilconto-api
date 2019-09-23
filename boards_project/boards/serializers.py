from datetime import datetime

from rest_framework import serializers
from .models import Board, AppUser, BoardMember

from django.core.mail import send_mail
from django.template import loader

from boards.utils import random_string
from decouple import config


class AppUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=256)
    email = serializers.EmailField(max_length=256)

    class Meta:
        model = AppUser
        fields = ('username', 'email', 'id', 'memberships', 'email_verified', 'is_activated')
        required_fields = ('username', 'email',)
        read_only_fields = ('id', 'memberships', 'email', 'email_verified', 'is_activated')
        depth = 1


class MemberAppUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=256)

    class Meta:
        model = AppUser
        fields = ('email', 'email_verified', 'is_activated')
        read_only_fields = ('email', 'email_verified', 'is_activated')


class MemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=256, required=False)
    score = serializers.IntegerField(required=False)
    user = MemberAppUserSerializer()
    
    class Meta:
        model = BoardMember
        fields = ('id', 'board', 'user', 'username', 'score')
        read_only_fields = ('id', 'board', 'user')
        depth = 1


class BoardSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)
    class Meta:
        model = Board
        fields = ('id', 'title', 'members')
        read_only_fields = ('id',)
        depth = 1

    def create(self, validated_data):
        """
        This function is triggered during access to the create view
        Classic attributes are set as usual (basically this is just the board's title)
        Then members are inserted with scores

        - The requesting user is added to the board members by default
        !!! IMPORTANT !!! : This should be mentionned as a warning in the front applciation
        
        Additional possible feature : Something should happen if one of the key in the scores dict does not
        match with any of the members email provided.
        """

        members_data = validated_data.pop('members')
        board = Board.objects.create(**validated_data)

        # By default, the requesting user is added to the board
        if self.context['request'].user not in members_data:
            # Retrieve user infos
            user = self.context['request'].user
            filtered_members_data = [item for item in members_data if item['user']['email'] == user.email]

            # Deals with the case where the request body does not provide information on it's score or username
            if len(filtered_members_data) == 0:
                member_username = user.username
                member_score = int(datetime.utcnow().timestamp())
            else:
                member_username = filtered_members_data[0].get('username', user.username)
                member_score = filtered_members_data[0].get('score', int(datetime.utcnow().timestamp()))
                
            # Add this user to the board
            member = board.add_member(member_username, user.id)
            board.reset_score(member.id, member_score)
        
        # Add the other members to the board
        for member_data in members_data:
            try:
                user = AppUser.objects.get(email=member_data['user']['email'])
                username = member_data.get('username', user.username)
                member = board.add_member(username, user.id)
                board.reset_score(member.id, member_data.get('score', int(datetime.utcnow().timestamp())))
            except AppUser.DoesNotExist:
                # That's where we'll implement the email to non-existing members feature
                # @TODO: Implement it !

                new_user = {
                    "email": member_data['user']['email'],
                    "username": member_data['user']['email'],
                    "is_activated": False,
                    "activation_hash": random_string()
                }
                created_user = AppUser.objects.create_user(**new_user)
                username = member_data.get('username', created_user.email)
                member = board.add_member(username, created_user.id)
                board.reset_score(member.id, member_data.get('score', int(datetime.utcnow().timestamp())))

                activation_url = f'{config("FRONT_APP_URL", default="localhost:8080")}/activate/{created_user.id}?hash={created_user.activation_hash}'
                html_message = loader.render_to_string(
                    '../templates/activate_email.html',
                    {
                        "board_title": board.title,
                        "sender_email": self.context['request'].user.email,
                        "activation_link": activation_url
                    }
                )
                send_mail(
                    f'You\'ve been invited to join the board {board.title}',
                    message="test email",
                    from_email='ilcontoapp@gmail.com',
                    recipient_list=["lecanu.maxence@gmail.com"],
                    html_message=html_message,
                    fail_silently=False,
                )
                pass

        return board