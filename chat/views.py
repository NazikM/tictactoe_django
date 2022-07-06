from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render

from chat.models import Player
from chat.utils import generate_name


def game(request):
    url = request.build_absolute_uri().split('/')[2]
    user, player = request.user, None
    if request.user is not AnonymousUser and request.user.is_authenticated:
        player = Player.objects.get_or_create(user=user)[0]
    elif not request.session.get('username'):
        request.session['username'] = generate_name()
        request.session.modified = True

    room_name = request.GET.get("room", "")
    if room_name:
        return render(request, "tictactoe/game.html", context={"room_name": room_name,
                                                               'username': request.session['username'],
                                                               'url': url,
                                                               'player': player})
    return render(request, "tictactoe/main.html", context={'username': request.session['username'],
                                                           'url': url,
                                                           'player': player})
