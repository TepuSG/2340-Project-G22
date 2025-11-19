from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.decorators import login_required

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')


def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    print('sing up')
    if request.method == 'POST':
        print('posted')
        # Pass the custom error class when instantiating the form on POST
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            print('form valid')
            form.save() # This now correctly saves the user and their role
            # You might want to add a success message here
            return redirect('accounts.login')
        else:
            template_data['form'] = form
    else: # This handles the GET request
        template_data['form'] = CustomUserCreationForm(error_class=CustomErrorList)
    print('rendering the form', template_data)
    return render(request, 'accounts/signup.html', {'template_data': template_data})


@login_required
def recruiter_notifications(request):
    """View all recruiter notifications."""
    # Only allow recruiters to view this page
    if not getattr(request.user, 'is_recruiter', False):
        return redirect('home.index')

    notifications = request.user.notifications.all()
    template_data = {'title': 'Notifications'}
    return render(request, 'accounts/notifications.html', {'template_data': template_data, 'notifications': notifications})


@login_required
def mark_notification_read(request, pk):
    """Mark a notification as read and redirect to the profile if available."""
    from .models import Notification
    from django.http import HttpResponseForbidden
    
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
    except Notification.DoesNotExist:
        return HttpResponseForbidden()
    
    notification.is_read = True
    notification.save()
    
    # If notification has a profile, redirect to it; otherwise go to notifications list
    if notification.profile:
        return redirect('profiles:detail', username=notification.profile.user.username)
    else:
        return redirect('accounts.notifications')
