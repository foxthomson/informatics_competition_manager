# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

# imports for user system
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# local imports
from icm.models import Type
from icm.helper_functions import competition_active

# Index page
@login_required
def index(request):
    context = {"usertype": request.user.type.usertype,
               "running":  competition_active(),
               "noindexlink": True}
    return render(request, "base/index.html", context)

# login page
def user_login(request):
    # POST or GET
    if request.method == "POST":
        # Get username and password
        username = request.POST["username"]
        password = request.POST["password"]

        # correct login details
        user = authenticate(username=username, password=password)

        if user is None:
            # invalid login details
            return render(request, "base/login.html", {"fail_login": True, "noindexlink": True})
        else:
            # valid login details
            # Log user in
            login(request, user)
            # redirect to the homepage with success message
            messages.success(request, "Log in successful")
            return HttpResponseRedirect("/index/")
    else:
        return render(request, "base/login.html", {"noindexlink": True})

# Logout
# To logout the user must be logged in
@login_required
def user_logout(request):
    logout(request)

    # Redirect to the login page with success message
    messages.success(request, "Log out successful")
    return HttpResponseRedirect("/login/")

# Change password
@login_required
def user_change_password(request):
    # POST or GET
    if request.method == "POST":
        # Get the user
        user = request.user

        # Check if password correct
        if user.check_password(request.POST["oldpass"]):
            # Check if passwords match
            if request.POST["newpass1"] == request.POST["newpass2"]:
                # update, redirect and add success message
                user.set_password(request.POST["newpass1"])
                user.save()

                messages.success(request, "Password changed")
                return HttpResponseRedirect("/login/")
            else:
                # Render with error
                return render(request, "base/changepass.html", {"no_match": True})
        else:
            # Render with error
            return render(request, "base/changepass.html", {"wrong_pass": True})
    else:
        # If GET render change password page
        return render(request, "base/changepass.html", {})
