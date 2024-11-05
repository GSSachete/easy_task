from django.shortcuts import render, redirect
from .models import ChatRoom
from .forms import ChatRoomForm

def room_list(request):
    rooms = ChatRoom.objects.all()
    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = ChatRoomForm()

    return render(request, 'room_list.html', {'rooms': rooms, 'form': form})

def chat_room(request, room_name):
    return render(request, 'chat.html', {'room_name': room_name})
