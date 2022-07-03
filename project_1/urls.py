from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path, include

from chat.views import game

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tictactoe/', game, name='main'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
]
