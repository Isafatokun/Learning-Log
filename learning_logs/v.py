from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

import learning_logs
from .models import Topic,Entry
from .forms import TopicForm, EntryForm


def check_user(request):
    #check topic belongs to the current user
    if topic.owner != request.user:
        raise Http404

# Create your views here.
def index(request):
    """Home page"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Display our Topics"""
    topics = Topic.objects.order_by('date_added').filter(owner=request.user)
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context=context)

@login_required
def topic(request,topic_id):
    """Display our Topics"""
    topic = Topic.objects.get(id=topic_id)
    
    #check topic belongs to the current user
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context=context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST or None)
        if form.is_valid():

            # Add the current user as the owner
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request,topic_id):
    """Add a new Entry."""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST or None)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an exisiting entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    #check topic belongs to the current user
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; prefill from with current entry.
        form = EntryForm(instance=entry)
    else:
        # Change the data since its POST request
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id=topic.id)

    context = {'entry': entry,'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)