from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from chat.models import Game, Player
from chat.utils import TicTacToe


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.game_room, created = Game.objects.get_or_create(u_name=self.room_name)
        self.username = self.scope.get('user', '')
        self.player = None
        if self.username and self.username.is_authenticated:
            self.player = Player.objects.get(user=self.username)
            self.username = self.username.username
        else:
            self.username = self.scope['session']['username']
        if self.username not in (self.game_room.player_1, self.game_room.player_2):
            if self.game_room.status == "w":
                if self.game_room.player_1 is None:
                    self.game_room.player_1 = self.username
                    self.game_room.profile_1 = self.player
                    self.game_room.turn = self.username
                    self.game_room.save()
                    self.p = "X"
                elif self.game_room.status == "w":
                    self.game_room.status = "p"
                    self.game_room.player_2 = self.username
                    self.game_room.profile_2 = self.player
                    self.game_room.save()
                    self.p = "O"

                self.lobby_message()

                async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
                self.accept()
            else:
                self.accept()
                self.chat_message({
                    'text': {"chart": self.game_room.chart, "winner": None, "player": None},
                    'player_1': self.game_room.player_1,
                    'player_2': self.game_room.player_2
                })
        else:
            self.accept()
            self.p = "X" if self.game_room.player_1 == self.username else "O"
            async_to_sync(self.channel_layer.group_send)(self.room_name, {
                'type': 'chat.message',
                'text': {"chart": self.game_room.chart, "winner": None, "player": self.p},
                'player_1': self.game_room.player_1,
                'player_2': self.game_room.player_2
            })

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
        try:
            self.game_room.refresh_from_db()
        except ObjectDoesNotExist:
            return

        if self.game_room.status == "p":
            winner = self.game_room.player_2 if "X" == self.p else self.game_room.player_1
            self.print_winner(winner)
            async_to_sync(self.channel_layer.group_send)(self.room_name, {
                'type': 'chat.message',
                'text': {"chart": self.game_room.chart, "winner": winner, "player": self.p}
            })
        self.game_room.delete()
        self.lobby_message()

    def receive(self, text_data=None, bytes_data=None):
        self.game_room.refresh_from_db()
        try:
            self.fetch_errors()
            self.game_room.chart, res = TicTacToe.next_step(self.game_room.chart, json.loads(text_data)['move'], self.p)
        except ValueError as e:
            return self.send(text_data=json.dumps({
                "error": str(e),
                "player": self.p
            }))

        self.game_room.turn = self.game_room.player_2 if self.game_room.player_1 == self.username else self.game_room.player_1

        if res:
            winner = self.game_room.player_1 if "X" == self.p else self.game_room.player_2
            self.game_room.status = "f"
            self.print_winner(winner)
            self.lobby_message()
        elif '.' not in self.game_room.chart:
            winner = "Tie"
            self.game_room.status = "f"
            self.print_winner(winner)
            self.lobby_message()
        else:
            winner = None
        self.game_room.save()
        async_to_sync(self.channel_layer.group_send)(self.room_name, {
            'type': 'chat.message',
            'text': {"chart": self.game_room.chart, "winner": winner, "player": None}
        })

    def chat_message(self, event):
        if self.username in (self.game_room.player_1, self.game_room.player_2):
            event["text"]["player"] = self.p
        self.send(text_data=json.dumps(event['text']))

    def lobby_message(self):
        data = serializers.serialize("json", Game.objects.all(), fields=('u_name', 'status'))
        async_to_sync(self.channel_layer.group_send)("users", {
            'type': 'lobby_smessage',
            'text': data
        })

    def fetch_errors(self):
        if self.username not in (self.game_room.player_2, self.game_room.player_1):
            raise ValueError("You cannot play here. You are spectator!")

        if self.game_room.status == "f":
            raise ValueError("Game already finished!")

        if not self.game_room.player_2:
            raise ValueError("Wait for other players")

        if self.game_room.turn != self.username:
            raise ValueError("Not your turn!")

    def print_winner(self, winner):
        if self.game_room.profile_1:
            if winner == "Tie":
                self.game_room.profile_1.draws += 1
            elif winner == self.game_room.player_1:
                self.game_room.profile_1.winnings += 1
            else:
                self.game_room.profile_1.losses += 1
            self.game_room.profile_1.save()
        if self.game_room.profile_2:
            if winner == "Tie":
                self.game_room.profile_2.draws += 1
            elif winner == self.game_room.player_1:
                self.game_room.profile_2.losses += 1
            else:
                self.game_room.profile_2.winnings += 1
            self.game_room.profile_2.save()


class LobbyConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("users", self.channel_name)
        data = serializers.serialize("json", Game.objects.all(), fields=('u_name', 'status'))
        async_to_sync(self.channel_layer.group_send)("users", {
            'type': 'lobby_smessage',
            'text': data
        })
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)("users", self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        pass

    def lobby_smessage(self, event):
        self.send(text_data=event['text'])
