import json

from channels import Group
from channels.sessions import channel_session

from .models import Room


@channel_session
def ws_connect(message):
    _, label = message['path'].strip(b'/').split(b'/')
    room = Room.objects.get(label=label)
    Group(b'chat-' + label).add(message.reply_channel)
    message.channel_session['room'] = room.label


@channel_session
def ws_receive(message):
    label = message.channel_session['room']
    room = Room.objects.get(label=label)
    data = json.loads(message['text'])
    msg = room.message_set.create(
        handle=data['handle'],
        message=data['message'],
    )
    Group(b'chat-' + str.encode(label)).send({
        'text': json.dumps(msg.as_dict())
    })


@channel_session
def ws_disconnect(message):
    label = message.channel_session['room']
    Group(b'chat-' + str.encode(label)).discard(message.reply_channel)
