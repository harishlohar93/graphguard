import json
from channels.generic.websocket import AsyncWebsocketConsumer


class AlertConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            self.group_name = "alerts"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            await self.send(text_data=json.dumps({
                "type": "connection_established",
                "message": "Connected to GraphGuard alert stream"
            }))
        except Exception as e:
            print(f"WebSocket connect error: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        except Exception as e:
            print(f"WebSocket disconnect error: {str(e)}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "alert_message",
                    "message": data
                }
            )
        except Exception as e:
            print(f"WebSocket receive error: {str(e)}")

    async def alert_message(self, event):
        try:
            await self.send(text_data=json.dumps(event["message"]))
        except Exception as e:
            print(f"WebSocket send error: {str(e)}")