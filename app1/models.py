from django.db import models
from django.contrib.auth.models import User # here we are importing user name i.e admin here
from datetime import date

class Venue(models.Model):
    name = models.CharField("Venue name", max_length=60)
    address = models.CharField(max_length=100)
    zip_code = models.CharField("zip code", max_length=50)
    phone = models.CharField("contact no", max_length=20)
    web = models.URLField("website")
    email_address = models.EmailField("email address")
    owner = models.IntegerField("Venue Owner", blank=False, default=1)
    image = models.ImageField(blank=True,null=True,upload_to="images/")

    def __str__(self):
        return self.name


class MyClubuser(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField("user Email")

    def __str__(self):
        return self.first_name + " " + self.last_name


class event(models.Model):
    name = models.CharField("Event name", max_length=60)
    event_date = models.DateTimeField("date time")
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    # venue = models.CharField(max_length=60)
    manager = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL
    )  # here foreign key is from User from imported User!!
    description = models.TextField(blank=True)
    attendes = models.ManyToManyField(MyClubuser, blank=True)
    approved = models.BooleanField('approve',default = False)

    def __str__(self):
        return self.name

    @property
    def days_till(self):
        today = date.today()
        event_day = self.event_date.date() - today
        day_time_strip = str(event_day).split(",",1)[0]
        return day_time_strip