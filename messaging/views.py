from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.conf import settings
from .models import Message
from .forms import MessageForm, EmailForm

User = get_user_model()

@login_required
def inbox(request):
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).order_by('-timestamp')
    
    conversations = {}
    for message in messages:
        other_user = message.recipient if message.sender == request.user else message.sender
        if other_user not in conversations:
            conversations[other_user] = message
            
    conversation_list = []
    for user, last_message in conversations.items():
        conversation_list.append({
            'user': user,
            'last_message': last_message,
            'unread': not last_message.is_read and last_message.recipient == request.user
        })
        
    return render(request, 'messaging/inbox.html', {'conversations': conversation_list})

@login_required
def conversation(request, username):
    other_user = get_object_or_404(User, username=username)
    
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=other_user) |
        Q(sender=other_user, recipient=request.user)
    ).order_by('timestamp')
    
    # Mark as read
    messages.filter(recipient=request.user, is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = other_user
            message.save()
            return redirect('messaging:conversation', username=username)
    else:
        form = MessageForm()
        
    return render(request, 'messaging/conversation.html', {
        'other_user': other_user,
        'messages': messages,
        'form': form
    })

@login_required
def send_email(request, username):
    recipient = get_object_or_404(User, username=username)
    
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            try:
                email = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER, # From the system account (your Gmail)
                    [recipient.email], # To the candidate
                    reply_to=[request.user.email] # Reply to the recruiter
                )
                email.send(fail_silently=False)
                
                messages.success(request, f"Email sent to {recipient.username} successfully.")
                return redirect('profiles:detail', username=username)
            except Exception as e:
                messages.error(request, f"Failed to send email: {str(e)}")
    else:
        form = EmailForm()
        
    return render(request, 'messaging/send_email.html', {
        'recipient': recipient,
        'form': form
    })
