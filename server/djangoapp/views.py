from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealers_by_id_from_cf
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def get_about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect('djangoapp:index')
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/a91d51c2-f0b9-497c-9eb3-797e65bafb41/dealership-package/get-dealership.json"
        # Get dealers from the URL
        context = {"dealerships": get_dealers_from_cf(url)}
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in context["dealerships"]])
        return render(request, 'djangoapp/index.html', context)


def signup_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {"reviews": get_dealer_reviews_from_cf("https://eu-de.functions.appdomain.cloud/api/v1/web/a91d51c2-f0b9-497c-9eb3-797e65bafb41/dealership-package/review",dealer_id)}
    print(context)
    return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id):
    if(request.user.is_authenticated):
        review = {}
        review["time"] = datetime.utcnow().isoformat()
        review["dealership"] = 11
        review["review"] = "This is a great car dealer"
        review["name"] = "Jonas"
        review["purchase"] = True
        review["car_make"] = "Audi"
        review["car_model"] = "A6"
        review["car_year"] = "2010"

        json_payload = {}
        json_payload["payload"] = review
        return HttpResponse(post_request("https://eu-de.functions.appdomain.cloud/api/v1/web/a91d51c2-f0b9-497c-9eb3-797e65bafb41/dealership-package/review", json_payload))
    else:
        return HttpResponse("You have to be signed in to use this feature")