from django.contrib import admin
from django import forms

from .models import Board, AppUser, BoardMember


"""=========================================
=========== Board Administration ===========
========================================="""

class BoardMemberInline(admin.TabularInline):
  model = BoardMember
  fields = ('id', 'username', 'user', 'score',)
  readonly_fields = ('id', 'user')

  def has_add_permission(self, request, obj):
    return False

  def get_extra(self, request, obj=None, **kwargs):
    return 0


class BoardAdmin(admin.ModelAdmin):
  list_display = ['id', 'title', 'created_at']
  fields = ('id', 'title', 'created_at')
  readonly_fields = ['id', 'created_at']
  inlines = [BoardMemberInline]

admin.site.register(Board, BoardAdmin)


"""=========================================
=========== Member Administration ==========
========================================="""

@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
  list_display = ['id', 'username', 'user', 'board']
  fields = ('id', 'board', 'user', 'username', 'score')
  readonly_fields = ['id', 'user', 'board']


"""=========================================
=========== User Administration ============
========================================="""

class MembershipsInline(admin.TabularInline):
  model = BoardMember
  fields = ('id', 'board', 'username', 'score')
  readonly_fields = ('id', 'board')
  can_delete = True

  def has_add_permission(self, request, obj):
    return False

  def get_extra(self, request, obj=None, **kwargs):
    return 0
    

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
  list_display = ['username', 'email', 'email_verified', 'is_activated', 'created_at', 'id']
  fields = ('id', 'username', 'email', 'email_verified', 'is_activated', 'activation_hash', 'created_at',)
  readonly_fields = ['id', 'email', 'is_activated', 'activation_hash', 'created_at']
  inlines = [MembershipsInline]
