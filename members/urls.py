from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("userlog",views.login_user,name="login_user"),
    path("userlogout",views.logout_user,name="logout_user"),
    path("registration",views.registration,name="registration"),

]