from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUsers

class CustomUserCreationForm(UserCreationForm):
    mobile_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = CustomUsers
        fields = ('username', 'mobile_number')