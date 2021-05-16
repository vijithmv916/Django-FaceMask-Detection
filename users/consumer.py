from channels.generic.websocket import AsyncWebsocketConsumer

# from asgiref.sync import async_to_sync
# import json


class my_data(AsyncWebsocketConsumer):

    # ws://localhost:8000/ws/mydata/mycoderoom -> mycoderoom is the code name for connecting
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print(f"room-name -> {self.room_name} and groupname ->{self.room_group_name}")
        await self.accept() 

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # print (text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "clientNotification",
                "value": text_data,
            },
        )

    async def clientNotification(self, event):
        print(event["value"])
        await self.send(event["value"])
