from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User



class TaskForm(forms.ModelForm):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Write yout task here...'
    }))
    class Meta:
        model = Task
        fields = ['name']
    
    def clean_name(self):
        taskname = self.cleaned_data.get("name")
        if taskname.isalnum():
            return taskname
        else:
            raise forms.ValidationError('a task name can only be alphanumeric!')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Email'
    }))
    username = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'username'
    }))
    password1 = forms.CharField(label="", max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'password'
    }))
    password2 = forms.CharField(label="", max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'confirm password'
    }))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'First name'
    }))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Last name'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Email'
    }))
    username = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'username'
    }))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'First name'
    }))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Last name'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class RestPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="", max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'your new password'
    }))
    new_password2= forms.CharField(label="", max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'confirm password'
    }))
    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')