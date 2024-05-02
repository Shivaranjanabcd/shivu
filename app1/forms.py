from django import forms
from django.forms import ModelForm  # importing models.py content here
from .models import Venue, event


# craeting a venue form


class VenueForm(ModelForm):  # ModelForm is from above imported library
    class Meta:
        model = Venue  # model.py class
        """fields = (
            "__all__"  # here we are seeking for all the fields that we want froms Venue
        )"""
        exclude = ["owner"]  # this is for include all but except one i.e "owner"
        # what if we need accoring fields??? ('name','address','zip_code','phone') simple!!!!1

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Venue name"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "address"}
            ),
            "zip_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "zipcode"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "contact"}
            ),
            "web": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "web"}
            ),
            "email_address": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "mail"}
            ),
        }

        labels = {
            "name": "Enter your Name",
            "address": "Enter your Address",
            "zip_code": "Zip-Code",
            "phone": "Contact Number",
            "web": "WebAddress",
            "email_address": "Mail",
            "image":" ",
        }


# event admin form
class EventFormAdmin(ModelForm):
    class Meta:
        model = event
        fields = "__all__"

        labels = {
            "event_date": "yyyy-mm-dd hh:mm:ss",
        }

#event loged in user form!!!!
class EventForm(ModelForm):
    class Meta:
        model = event
        # fields = "__all__"
        exclude = ["manager"]
        labels = {
            "event_date": "yyyy-mm-dd hh:mm:ss",
        }
