from django.contrib import admin

from .models import Board, AppUser, BoardMember

admin.site.register(Board)
admin.site.register(BoardMember)
admin.site.register(AppUser)
