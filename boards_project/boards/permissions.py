from rest_framework import permissions
from boards.models import Board, BoardMember


class IsBoardMember(permissions.BasePermission):

    def has_permission(self, request, view):
        board_id = request.parser_context['kwargs']['board_id']
        user_id = request.user.id
        board = Board.objects.get(id=board_id)
        return user_id in [member.user.id for member in board.members.all()]

    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'DELETE'):
            print(request.user, obj.user)
            return request.user == obj.user
        return True


class IsActivated(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_activated


class HasEmailVerified(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.email_verified