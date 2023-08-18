from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Room
import json
from user.models import User
from asgiref.sync import sync_to_async
from .serializer import MessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(self.room_name, "room")
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            # Parse the incoming message as JSON
            data = json.loads(text_data)
            message = data.get('content')
            author = data.get('author')
            room_id = data.get('room_id')

            if not (message and author and room_id):
                raise ValueError('Invalid message data')

            # Save the message to the database
            new_message = await self.create_message(message,author,room_id)
            
            serializer = MessageSerializer(new_message)
            print(serializer.data['content'], serializer.data['timestamp'], 'serialized')
            await self.channel_layer.group_send(
                
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'id': serializer.data['id'],
                    'content': serializer.data['content'],
                    'author': serializer.data['author'],
                    'timestamp': serializer.data['timestamp']
                }
            )

        except (json.JSONDecodeError, ValueError) as e:
            # Handle invalid JSON or missing fields
            error_message = {'error': str(e)}
            await self.send(text_data=json.dumps(error_message))

    @sync_to_async
    def create_message(self, message, author, room_id):
        print(self, message, author, room_id, 'data  i got')
        user = User.objects.get(pk=author)
        room = Room.objects.get(pk=room_id)
        new_message = Message.objects.create(
           content = message,
           author = user,
           room_id = room_id
         )
        print('new:' , new_message)
        return new_message

    async def chat_message(self, event):
        id = event.get('id')
        message = event.get('content')
        author = event.get('author')
        timestamp = event.get('timestamp')


        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'id': id,
            'content': message,
            'author': author,
            'timestamp': timestamp
        }))