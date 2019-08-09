from rest_framework import permissions


class IsBoardMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()


class IsCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        return request.user == obj
