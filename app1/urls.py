from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:year>/<str:month>/", views.home, name="home"),
    path("base/", views.index, name="index"),
    path("events/", views.all_events, name="list-events"),
    path("delete_event/<event_id>", views.delete_event, name="delete_event"),
    path("add_venue/", views.add_venue, name="add_venue"),
    path("list_venue/", views.list_venue, name="list_venue"),
    path("show_venue/<venue_id>", views.show_venue, name="show_venue"),
    path("search_venues", views.search_venues, name="search_venues"),
    path("update_venue/<venue_id>", views.update_venue, name="update_venue"),
    path("add_event/", views.add_event, name="add_event"),
    path("event_update/<event_id>", views.update_event, name="update_events"),
    path("delete_venue/<venue_id>", views.delete_venue, name="delete_venue"),
    path("text_venue", views.text_venue, name="text_venue"),
    path("csv_venue", views.csv_venue, name="csv_venue"),
    path("pdf_venue", views.pdf_venue, name="pdf_venue"),
    path("search_event",views.search_event,name="search_event"),
    path("event_approval",views.event_approval,name="event_approval"),
    path("eventvenue/<venue_id>", views.event_venue, name="event_venue"),
    path("list_of_event/<event_id>", views.list_of_event, name="list_of_event"),

]
