from django.contrib import admin
from django.urls import path

from chat.views import game

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tictactoe/', game, name='main')
]
