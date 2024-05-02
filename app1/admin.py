from django.contrib import admin
from .models import Venue
from .models import event
from .models import MyClubuser

# admin.site.register(Venue)  #uses to register in admin
# admin.site.register(event)  #uses to register in admin
admin.site.register(MyClubuser)  # uses to register in admin


@admin.register(Venue)  # uses to register in admin
class VenueAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "address",
        "phone",
    )  # which are all the fields we need show up on display name is default including that adrees and phone number
    ordering = ("name",)  # ordering i.e a-z,A-Z
    search_fields = (
        "name",
        "address",
    )  # by which are all the fields it suppose to be search


@admin.register(
    event
)  # OR admin.site.register(event eventAdmin) both are same  #uses to register in admin
class evntAdmin(admin.ModelAdmin):
    fields = (
        ("name", "venue"),
        "event_date",
        "description",
        "manager",
        "attendes",
        "approved",
    )  # again we are mentioning which are all the fields we are require on admin pannel even if we mentioned in models according to reqirement we can select fields
    list_display = ("name", "event_date", "venue")
    ordering = ("event_date",)
    list_filter = ("event_date", "venue")  # filtered by date and venues
