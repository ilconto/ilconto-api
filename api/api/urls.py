from django.contrib import admin
from django.urls import path, include
from boards.views import BoardView
from boards.models import Board
from rest_framework import routers

router = routers.DefaultRouter()
router.register('boards', BoardView)

# admin.site.register(Board)

urlpatterns = [
    path("", include(router.urls)),
    path('admin/', admin.site.urls),
]
