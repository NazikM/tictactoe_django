from django.shortcuts import render

from chat.utils import generate_name


def game(request):
    if not request.session.get('username'):
        request.session['username'] = generate_name()
        request.session.modified = True
    print(request.session['username'])
    room_name = request.GET.get("room", "")
    if room_name:
        return render(request, "tictactoe/game.html", context={"room_name": room_name, 'username': request.session['username']})
    return render(request, "tictactoe/main.html", context={'username': request.session['username']})
