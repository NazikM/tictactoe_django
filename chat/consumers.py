from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import SyncConsumer
import json
from django.core import serializers

from chat.models import Game
from chat.utils import TicTacToe, generate_name


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.game_room, created = Game.objects.get_or_create(u_name=self.room_name)
        username = self.scope['session']['username']
        if username not in (self.game_room.player_1, self.game_room.player_2):
            if self.game_room.status == "w":
                if self.game_room.player_1 is None:
                    self.game_room.player_1 = username
                    self.game_room.turn = username
                    self.game_room.save()
                elif self.game_room.status == "w":
                    self.game_room.status = "p"
                    self.game_room.player_2 = username
                    self.game_room.save()

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
            p = "X" if self.game_room.player_1 == username else "O"
            self.chat_message({
                'text': {"chart": self.game_room.chart, "winner": None, "player": p},
                'player_1': self.game_room.player_1,
                'player_2': self.game_room.player_2
            })


    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)



    def receive(self, text_data=None, bytes_data=None):
        # print(dict(self.scope['session']))
        username = self.scope['session']['username']
        self.game_room.refresh_from_db()
        errors = []

        if username not in (self.game_room.player_2, self.game_room.player_1):
            errors.append("You cannot play here. You are spectator!")
            return self.send(text_data=json.dumps({
                "errors": tuple(errors)
            }))

        if self.game_room.status == "f":
            errors.append("Game already finished!")
            return self.send(text_data=json.dumps({
                "errors": tuple(errors)
            }))

        if not self.game_room.player_2:
            errors.append("Wait for other players")
            return self.send(text_data=json.dumps({
                "errors": tuple(errors)
            }))

        if self.game_room.turn != username:
            errors.append("Not your turn!")
            return self.send(text_data=json.dumps({
                "errors": tuple(errors)
            }))

        if self.game_room.player_1 == username:
            self.game_room.turn = self.game_room.player_2
            p = "X"
        else:
            self.game_room.turn = self.game_room.player_1
            p = "O"
        try:
            self.game_room.chart, res = TicTacToe.next_step(self.game_room.chart, json.loads(text_data)['move'], p)
        except ValueError as e:
            errors.append(str(e))
            return self.send(text_data=json.dumps({
                "errors": tuple(errors)
            }))
        if res or '.' not in self.game_room.chart:
            self.game_room.status = "f"
            self.lobby_message()
        self.game_room.save()

        winner = ('winner: ' + p) if res else None
        if not winner and '.' not in self.game_room.chart:
            winner = "Tie"
        async_to_sync(self.channel_layer.group_send)(self.room_name, {
            'type': 'chat.message',
            'text': {"chart": self.game_room.chart, "winner": winner, "player": None},
            'player_1': self.game_room.player_1,
            'player_2': self.game_room.player_2
        })

    def chat_message(self, event):
        username = self.scope['session']['username']
        if event['player_1'] == username:
            event["text"]["player"] = "X"
        elif event['player_2'] == username:
            event["text"]["player"] = "O"
        self.send(text_data=json.dumps(event['text']))

    def lobby_message(self):
        data = serializers.serialize("json", Game.objects.all(), fields=('u_name', 'status'))
        async_to_sync(self.channel_layer.group_send)("users", {
            'type': 'lobby_smessage',
            'text': data
        })


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
