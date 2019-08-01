from django.contrib import admin
from django.urls import path, include
from boards.views import BoardView
from boards.models import Board
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path("boards/<pk>", BoardView.as_view()),
    path('admin/', admin.site.urls),
    path('auth/', obtain_jwt_token)
]
