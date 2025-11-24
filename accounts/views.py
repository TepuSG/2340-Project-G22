from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import requests
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()
from django.conf import settings


@login_required
def logout(request):
    auth_logout(request)
    return redirect("home.index")


# If using social-auth-app-django
def google_oauth_redirect(request):
    # Optional: store role selection in session if you need it
    # request.session['role'] = request.GET.get('role', 'seeker')

    # Redirect to the social auth "begin" URL for Google
    return redirect(reverse("social:begin", args=["google-oauth2"]))


def github_oauth_redirect(request):
    return redirect(reverse("social:begin", args=["github"]))


def login(request):
    template_data = {}
    template_data["title"] = "Login"
    if request.method == "GET":
        return render(request, "accounts/login.html", {"template_data": template_data})
    elif request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            template_data["error"] = "The username or password is incorrect."
            return render(
                request, "accounts/login.html", {"template_data": template_data}
            )
        else:
            auth_login(request, user)
            return redirect("home.index")


def signup(request):
    template_data = {}
    template_data["title"] = "Sign Up"
    print("sing up")
    if request.method == "POST":
        print("posted")
        # Pass the custom error class when instantiating the form on POST
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            print("form valid")
            form.save()  # This now correctly saves the user and their role
            # You might want to add a success message here
            return redirect("accounts.login")
        else:
            template_data["form"] = form
    else:  # This handles the GET request
        template_data["form"] = CustomUserCreationForm(error_class=CustomErrorList)
    print("rendering the form", template_data)
    return render(request, "accounts/signup.html", {"template_data": template_data})


@login_required
def recruiter_notifications(request):
    """View all recruiter notifications."""
    # Only allow recruiters to view this page
    if not getattr(request.user, "is_recruiter", False):
        return redirect("home.index")

    notifications = request.user.notifications.all()
    template_data = {"title": "Notifications"}
    return render(
        request,
        "accounts/notifications.html",
        {"template_data": template_data, "notifications": notifications},
    )


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
        return redirect("profiles:detail", username=notification.profile.user.username)
    else:
        return redirect("accounts.notifications")


def google_oauth_start_login(request):
    request.session["auth_status"] = "login"
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
        "&access_type=offline"
        "&prompt=select_account"
    )
    return redirect(auth_url)


def google_oauth_start(request):
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
        "&access_type=offline"
        "&prompt=select_account"
    )
    return redirect(auth_url)


# accounts/views.py
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from .models import CustomUser, SeekerProfile, RecruiterProfile

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
import requests
from django.conf import settings
from .models import CustomUser, SeekerProfile, RecruiterProfile


def google_oauth_callback(request):
    # 1️⃣ Check session for role
    role = request.session.get("selected_role")
    status = request.session.get("auth_status")
    print("makign request with the role", role)
    if not role and not status:
        messages.error(request, "Please select a role first.")
        return redirect("role_selection")
    print("valid role ")
    code = request.GET.get("code")
    if not code:
        messages.error(request, "Google login failed. No code returned.")
        return redirect("accounts.login")

    # 2️⃣ Exchange code for access token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    r = requests.post(token_url, data=data)
    token_data = r.json()
    access_token = token_data.get("access_token")

    if not access_token:
        messages.error(request, "Failed to obtain access token from Google.")
        return redirect("accounts.login")

    # 3️⃣ Fetch user info
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(user_info_url, headers=headers)
    user_info = r.json()

    google_email = user_info.get("email")
    google_name = user_info.get("name")

    if not google_email:
        messages.error(request, "Google login failed. Email is required.")
        return redirect("accounts.login")

    # 4️⃣ Fallback for username
    if google_name:
        username = google_name.replace(" ", "_").lower()[:30]  # max_length=150
    else:
        username = google_email.split("@")[0]

    if not username:
        messages.error(request, "Google login failed. Username is required.")
        return redirect("accounts.login")

    # 5️⃣ Ensure username is unique
    counter = 1
    base_username = username
    while CustomUser.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    # 6️⃣ Get or create user
    user, created = CustomUser.objects.get_or_create(
        email=google_email, defaults={"username": username, "role": role}
    )

    if created:
        return redirect("role_selection")

    # 7️⃣ Update role if user exists but role is None
    if not user.is_seeker and not user.is_recruiter:
        print("saving to the role of ", role)
        if role == "seeker":
            user.role = CustomUser.Roles.SEEKER
        elif role == "recruiter":
            user.role = CustomUser.Roles.RECRUITER
        user.save()

    from profiles.models import Profile

    Profile.objects.get_or_create(user=user)

    # 8️⃣ Ensure proper profile exists
    if user.role == CustomUser.Roles.SEEKER:
        SeekerProfile.objects.get_or_create(user=user)
    elif user.role == CustomUser.Roles.RECRUITER:
        RecruiterProfile.objects.get_or_create(user=user)

    # 9️⃣ Log the user in
    auth_login(request, user)

    # 🔟 Redirect to dashboard
    if user.is_seeker:
        return redirect("jobs.index")
    elif user.is_recruiter:
        return redirect("job.index")
    else:
        messages.error(request, "Role not properly set.")
        return redirect("role_selection")


User = get_user_model()


def role_selection(request):
    print("reqeust is made")
    if request.method == "POST":
        role = request.POST.get("role")
        if role not in ["seeker", "recruiter"]:
            return render(
                request,
                "accounts/role_selection.html",
                {"error": "Please select a valid role."},
            )
        request.session["selected_role"] = role  # store role in session
        print("set the role", request.session["selected_role"])
        return redirect("google_oauth_start")  # then start OAuth
    print("rednering the page")
    return render(request, "accounts/role_selection.html")
