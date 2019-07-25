from django.contrib import admin

from .models import Board, Member, User

admin.site.register(Board)
admin.site.register(Member)
admin.site.register(User)