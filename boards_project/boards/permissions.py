from rest_framework import permissions
from boards.models import Board

class IsBoardMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        board = Board.objects.get(id=obj.board.id)
        return request.parser_context['kwargs']['member_id'] in board.members.all()