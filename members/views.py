from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm #check it in notes for this !
from .forms import RegisterUserForm

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        #print(user.email) authenticate will return the "User" object to user so we can check email
        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            messages.success(
                request, ("Their was a an error in login! plaese try again..")
            )
            return redirect("login_user")
    else:
        return render(request, "reg/login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You loged out sucessfully!"))
    return redirect("home")


def registration(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            
            login(request, user)
            return redirect("home")
    else:
        form = RegisterUserForm()
    return render(request, "reg/registration.html", {"form": form})
