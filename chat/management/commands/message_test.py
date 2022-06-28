import time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        for i in range(10):
            async_to_sync(channel_layer.group_send)(
                'users',
                {
                    'type': 'lobby.message',
                    'text': f"Message outside {i}",
                    'sender': 'server'
                }
            )
            time.sleep(5)
