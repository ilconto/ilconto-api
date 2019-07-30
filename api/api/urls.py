from django.contrib import admin
from django.urls import path, include
from boards.views import BoardList
from boards.models import Board
from rest_framework import routers

urlpatterns = [
    path("boards/", BoardList.as_view()),
    path('admin/', admin.site.urls),
]
