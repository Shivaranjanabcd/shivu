from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime

# importing from models.py event class!
from .models import event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin

from django.http import HttpResponseRedirect, HttpResponse, FileResponse


# Create your views here.
def home(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    # dynamic datetime "year=datetime.now().year,month=datetime.now().strftime('%B')"
    name = "SHIVU"

    # converting month_number
    month = month.capitalize()
    month_num = list(calendar.month_name).index(month)
    month_num = int(month_num)

    EventList = event.objects.filter(
        event_date__year=year, event_date__month=month_num
    )  # you want to filter them based on the "year" of the "event_date" feild in model

    # creating html calender
    cal = HTMLCalendar().formatmonth(year, month_num)

    # current year and time
    now = datetime.now()
    current_year = now.year
    time = now.strftime("%I:%M:%S %p")
    return render(
        request,
        "home.html",
        {
            "name": name,
            "year": year,
            "month": month,
            "month_num": month_num,
            "cal": cal,
            "current_year": current_year,
            "time": time,
            "EventList": EventList,
        },
    )


def index(request):
    return render(request, "base.html", {})


def all_events(request):
    event_list = event.objects.all().order_by(
        "name"
    )  # from event library import all objects from event class from models.py
    return render(request, "event_list.html", {"event_list": event_list})


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(
            request.POST, request.FILES
        )  # When a form is submitted with a file input field (<input type="file">), the file data is included in request.FILES
        if form.is_valid():
            venue = form.save(
                commit=False
            )  # commit = flase is nothing but dont save it yet wait for until ."save()"
            venue.owner = request.user.id
            venue.save()  # we are saving here similar to "form.save" but insted form we assigned form to venue above so "venue.save()"
            # form.save()
            return HttpResponseRedirect("/add_venue?submitted=True")
    else:
        form = VenueForm
        if "submitted" in request.GET:
            submitted = True

    return render(request, "add_venue.html", {"form": form, "submitted": submitted})


from django.core.paginator import Paginator


def list_venue(request):
    # venue_list = Venue.objects.all().order_by('?')   to display in random order
    venue_list = Venue.objects.all()

    # pagination!!!!!!!!
    # set up pagination
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get(
        "page"
    )  # ex http://example.com/some-path/?page=3 GET method has a data passed through url so page =3 here in this example we r trying to retreving value of page here if its note intially it passes "None"!
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages
    return render(
        request,
        "venue.html",
        {"venue_list": venue_list, "venues": venues, "nums": nums},
    )


def show_venue(
    request, venue_id
):  # here venue_id is an " keyward argument" in urls.py <venu_id> is a case sensitive keyward argument check the venue.html
    id_venue = Venue.objects.get(
        pk=venue_id
    )  # in models "id_venue=Venue.objects.get(pk=listOfVenues numerics i.e=mumbaicity=1,bolrecity=2,etc  so by the numerics its fetch the individual venue now "id_venue" contains the name of the venue )
    owner = User.objects.get(
        pk=id_venue.owner
    )  # users=1-admin,2-tina,3-tom,4-punk..so pk=venue(owner)-->owner was a numeric get a user among all by venue numerics..

    return render(request, "show_venue.html", {"id_venue": id_venue, "owner": owner})


def search_venues(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        venues = Venue.objects.filter(
            name__contains=searched
        )  # it specifies that you want to filter events where the name field contains the value specified by the variable searched.
        return render(
            request, "search_venues.html", {"searched": searched, "venues": venues}
        )
    else:
        return render(request, "search_venues.html", {})


def update_venue(request, venue_id):
    id_venue = Venue.objects.get(pk=venue_id)
    if request.method == "POST":
        form = VenueForm(
            request.POST or None, request.FILES or None, instance=id_venue
        )  # or none i.e form = VenueForm(None)in some cases, you might need to initialize a form without any data  such as when you are rendering an empty form for the user to fill out.
        if form.is_valid():
            form.save()
            return redirect("list_venue")
    else:
        form = VenueForm(instance=id_venue)
    return render(request, "update_venue.html", {"id_venue": id_venue, "form": form})


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/add_event?submitted=True")
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                eevent = form.save(commit=False)
                eevent.manager = request.user
                form = eevent
                eevent.save()
                return HttpResponseRedirect("/add_event?submitted=True")
    else:
        if request.user.is_superuser:
            form = EventFormAdmin
            if "submitted" in request.GET:
                submitted = True
        else:
            form = EventForm
            if "submitted" in request.GET:
                submitted = True  # after the form submitted if we reolde the page also its show form submiited sucessfully! orelse its show new form even after submiited the form

    return render(request, "add_event.html", {"form": form, "submitted": submitted})


def update_event(request, event_id):
    Event = event.objects.get(id=event_id)
    form = EventForm(request.POST or None, instance=Event)
    if form.is_valid():
        form.save()
        return redirect("list-events")

    return render(request, "update_event.html", {"form": form, "Event": Event})


def delete_event(request, event_id):
    Event = event.objects.get(pk=event_id)
    if Event.manager == request.user:
        Event.delete()
        return redirect("list-events")


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect("list_venue")


def text_venue(reuest):
    response = HttpResponse(content_type="text\plane")
    response["Content-Disposition"] = "attachment; filename=venue.txt"
    venues = Venue.objects.all()
    lines = []
    for venue in venues:
        lines.append(
            f"{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n"
        )
    response.writelines(lines)
    return response


import csv


def csv_venue(reuest):
    response = HttpResponse(content_type="text\csv")
    response["Content-Disposition"] = "attachment; filename=venue.csv"
    venues = Venue.objects.all()
    # creating a csv writer!!!
    writer = csv.writer(response)
    # crating a header !!actually it is a first row!!!
    writer.writerow(
        [
            "venue name".upper().center(
                20
            ),  # 20 is width of venue name i.e how much space need leave from beging
            "address".upper().center(30),
            "zip-code".upper().center(50),
            "phone".upper().center(20),
            "web".upper().center(10),
            "email-address".upper().center(30),
        ]
    )
    for venue in venues:
        writer.writerow(
            [
                venue.name,
                venue.address,
                venue.zip_code,
                venue.phone,
                venue.web,
                venue.email_address,
            ]
        )

    return response


# to generate pdf file to downlode

from django.http import FileResponse
import io  # input output
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


def pdf_venue(request):
    # create a bytesteam buffer
    buf = io.BytesIO()

    # craeting a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # creating a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # add some lines of text
    lines = []

    venues = Venue.objects.all()
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")
    print(lines)
    for line in lines:
        textob.textLine(line)

    # finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="venue.pdf")


from django.contrib import messages


def search_event(request):
    if request.method == "POST":
        searched = request.POST["searchedd"]
        events = event.objects.filter(
            name__contains=searched
        )  # it specifies that you want to filter or select events where the "name field" contains the value specified by the variable searched.
        return render(
            request, "event_list.html", {"searched": searched, "events": events}
        )

    else:
        messages.success(
            request, ("Their was a an error in search! plaese try again..")
        )
    return render(request, "event_list.html", {})


def event_approval(request):
    event_list = event.objects.all().order_by("name")

    venue_list = Venue.objects.all()

    event_count = event.objects.all().filter(approved=True).count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist("boxes")

            # unchecke all events first
            event_list.update(approved=False)

            # update the database
            for x in id_list:
                event.objects.filter(pk=int(x)).update(approved=True)
                # OR
                """eve_list=event.objects.filter(pk=int(x))
                eve_list.update(approved=True)"""

            messages.success(request, ("aprroval sucessful."))
            return redirect("home")

        else:
            return render(
                request,
                "event_approval.html",
                {
                    "event_list": event_list,
                    "event_count": event_count,
                    "venue_count": venue_count,
                    "user_count": user_count,
                    "venue_list": venue_list,
                },
            )
    else:
        messages.success(request, ("your not allowed to view!"))


def event_venue(request, venue_id):
    venue = Venue.objects.get(id=venue_id)

    events = venue.event_set.all()

    if events:
        return render(request, "event-venue.html", {"events": events})
    else:
        messages.success(request, ("you don't have an events!"))
        return redirect("event_approval")

def list_of_event(request,event_id):
    Eve = event.objects.get(id=event_id)
    #ven = Eve.venue_set.all()
    return render(request,'list_of_event.html',{"Eve":Eve})