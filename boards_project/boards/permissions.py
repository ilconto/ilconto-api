from rest_framework import permissions
from boards.models import Board, BoardMember

class IsBoardMember(permissions.BasePermission):

    def has_permission(self, request, view):
        board_id = request.parser_context['kwargs']['board_id']
        member_id = request.parser_context['kwargs']['member_id']
        board = Board.objects.get(id=board_id)
        return member_id in [member.id for member in board.members.all()]

    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'DELETE'):
            print(request.user, obj.user)
            return request.user == obj.user
        return True