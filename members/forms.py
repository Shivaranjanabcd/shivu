from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    # so we are making first_name max length is 20 "over-righting" the model fields!!
    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs) #it calls the __init__ of UserCreationForm super class

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
