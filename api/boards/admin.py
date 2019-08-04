from django.contrib import admin

from .models import Board,  User

admin.site.register(Board)
# admin.site.register(Member)
admin.site.register(User)
