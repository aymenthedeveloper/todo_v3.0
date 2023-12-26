from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm, SignUpForm, UserEditForm, RestPasswordForm
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
            username = request.POST.get('username').lower()
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'an error occured! please try again!')
                return redirect('login_user')
    return render(request, 'main/login.html', {})


def activate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(id=uid)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login_user')
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect('signup_user')
    
def reset_pw(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(id=uid)
    if user and account_activation_token.check_token(user, token):
        form = RestPasswordForm(user)
        if request.method == 'POST':
            form = RestPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'your password was changed successfully :)')
                return redirect('home')
            else:
                for err in list(form.errors.values()):
                    messages.error(request, f'{err}')
                return redirect('reset_pw')
        return render(request, 'main/password_reset.html', {'form':form})


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("main/template_activate_account.html", {
        'username': user.username,
        "protocol": 'https' if request.is_secure() else 'http',
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, check your email {to_email} inbox and click on received activation link to confirm and complete the registration.\nNote: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def resetEmail(request, user, to_email):
    mail_subject = "password reset"
    message = render_to_string("main/template_email_reset_password.html", {
        'username': user.username,
        "protocol": 'https' if request.is_secure() else 'http',
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, check your email {to_email} inbox and click on received reset link to confirm and complete the registration.\nNote: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def signup_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')
        else:
            messages.error(request, 'an error occured! please try again!')
            return redirect('signup_user')
    return render(request, 'main/signup_user.html', {'form': form})



def password_reset(request):
    user = request.user
    if user.is_authenticated:
        form = RestPasswordForm(user)
        if request.method == 'POST':
            form = RestPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'your password was changed successfully')
                return redirect('home')
            else:
                for err in list(form.errors.values()):
                    messages.error(request, f'{err}')
                return redirect('password_reset')
        return render(request, 'main/password_reset.html', {'form':form})
    else:
        if request.method == 'POST':
            user_email = request.POST.get("email")
            user = User.objects.filter(email=user_email).first()
            if user:
                resetEmail(request, user, user_email)
                return redirect('home')
            else:
                messages.error(request, f"there are no user with this email: {user_email}")
                return redirect('password_reset')
        return render(request, 'main/pw_reset_email.html', {})





def logout_user(request):
    logout(request)
    return redirect('login_user')





def regroup(quaryset):
    output = {}
    for obj in quaryset:
        key = obj.date
        if key not in output:
            output[key] = []
        output[key].append(obj)
    return output
        

@login_required(login_url='login_user')
def home_updated(request):
    state = request.GET.get('state')
    q = request.GET.get('q') if request.GET.get('q') else ''
    current_user = request.user
    if state:
        tasks = Task.objects.filter(user=current_user, completed=state)
    else:
        tasks = Task.objects.filter(user=current_user, name__icontains=q)
    tasks = regroup(tasks)
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = current_user
            form.save()
            return redirect('home')
        else:
            for err in list(form.errors.values()):
                messages.error(request, f'{err}')
            return redirect('home')
    context = {'tasks': tasks, 'form':form, "state":state}
    return render(request, 'main/index.html', context)


@login_required(login_url='login_user')
def user_profile(request):
    user = request.user
    context = {'user':user}
    return render(request, 'main/user_profile.html', context)


@login_required(login_url='login_user')
def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('home')


@login_required(login_url='login_user')
def complete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.completed = not task.completed
    task.save()
    return redirect('home')


@login_required(login_url='login_user')
def edit_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        task = TaskForm(request.POST, instance=task)
        if task.is_valid():
            task.save()
            return redirect('home')
    return render(request, 'main/edit.html', {'form':form})


@login_required(login_url='login_user')
def update_user(request):
    form = UserEditForm(instance=request.user)
    if request.method == 'POST':
        form = UserEditForm(request.POST ,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    return render(request, 'main/edit_user.html', {'form':form})


