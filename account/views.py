from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect, render
from .forms import FormRegistration
from django.contrib.auth import authenticate, login


def registration_view(request):        # ESERCIZIO 1
    if request.method == "POST":
        form = FormRegistration(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = FormRegistration()
    context = {"form": form}
    return render(request, "account/registration.html", context)
