from rest_framework import permissions
from boards.models import Board, BoardMember, AppUser
from django.shortcuts import get_object_or_404


class IsBoardMember(permissions.BasePermission):

    def has_permission(self, request, view):
        board_id = request.parser_context['kwargs']['board_id']
        user_id = request.user.id
        board = Board.objects.get(id=board_id)
        return user_id in [member.user.id for member in board.members.all()]

    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'DELETE'):
            return request.user == obj.user
        return True


class IsActivated(permissions.BasePermission):
    
    def has_permission(self, request, view):
        self.message = f'The account {request.user.email} has not been activated yet'
        return request.user.is_activated


class HasEmailVerified(permissions.BasePermission):
    
    def has_permission(self, request, view):
        self.message = f'The email {request.user.email} has not been verified yet'
        return request.user.email_verified


class IsInOnboarding(permissions.BasePermission):
    message = 'test'

    def has_permission(self, request, view):
        activation_hash = request.data.get('activation_hash')
        user_id = request.parser_context['kwargs']['user_id']
        user = get_object_or_404(AppUser.objects.all(), id=user_id)

        if user.is_activated:
            self.message = f'User {user.email} has already been activated'
            return False

        if user.activation_hash != activation_hash:
            self.message = 'Invalid activation_hash'
            return False
        
        return True