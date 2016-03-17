import haikunator
from django.db import transaction
from django.shortcuts import render, redirect

from .models import Room


def about(request):
    return render(request, 'about.html')


def new_room(request):
    """
    Randomly create a new roomt
    """
    print("new room")
    new_room = None
    while not new_room:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)
    return redirect('chat:chat_room', label=label)


def chat_room(request, label):
    room, _ = Room.objects.get_or_create(label=label)
    messages = reversed(room.message_set.order_by("-timestamp")[:50])

    return render(request, "chat_room.html", {
        'room': room,
        'messages': messages,
    })
