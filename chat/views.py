from django.shortcuts import render


def game(request):
    room_name = request.GET.get("room", "")
    if room_name:
        return render(request, "tictactoe/game.html", context={"room_name": room_name})
    return render(request, "tictactoe/main.html")
