from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from .forms import EventForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def event_list(request):
    events = Event.objects.all()
    is_authenticated = request.user.is_authenticated
    return render(request, 'events/event_list.html', {'events': events, 'is_authenticated': is_authenticated})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


@login_required(login_url='users:login')
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user 
            event.save()
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


@login_required(login_url='users:login')
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if request.user != event.owner:
        messages.error(request, "You do not have permission to edit this event.")
        return redirect('events:event_detail', pk=event.pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/event_form.html', {'form': form})


@login_required(login_url='users:login')
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user != event.owner:
        messages.error(request, "You do not have permission to delete this event.")
        return redirect('events:event_detail', pk=event.pk)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect('events:event_list')
    
    return render(request, 'events/event_confirm_delete.html', {'event': event})


def user_logout(request):
    logout(request)
    return redirect('events:event_list')

@login_required
def attend_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user == event.owner:
        messages.info(request, "You cannot attend your own event.")
    elif request.user in event.attendees.all():
        messages.info(request, "You are already attending this event.")
    else:
        event.attendees.add(request.user)
        messages.success(request, "You are now attending this event.")
    
    return redirect('events:event_detail', pk=pk)


@login_required
def unattend_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user == event.owner:
        messages.info(request, "You cannot unattend your own event.")
    elif request.user in event.attendees.all():
        event.attendees.remove(request.user)
        messages.success(request, "You are no longer attending this event.")
    else:
        messages.info(request, "You are not attending this event.")

    return redirect('events:event_detail', pk=pk)
