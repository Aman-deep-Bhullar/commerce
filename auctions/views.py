from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from  django import forms
from  django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from .models import auction, watchlist,bids,Comment

from .models import User

class commentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": auction.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class listform(ModelForm):
    class Meta:
        model = auction
        fields =["title","description","category","price","image",]

@login_required
def newlist(request):
    if request.method == "POST":
        list = auction()
        form = listform(request.POST)
        if form.is_valid():
            create = form.save(commit=False)
            create.user = request.user
            create.save()
            return HttpResponseRedirect(reverse("index"))

    form= listform()
    return render(request,"auctions/list.html", {
           "form":form
    })
class bidsForm(ModelForm):
      class Meta:
        model = bids
        fields = ["price"]

def details(request, pk):
    productdetails= auction.objects.get(pk=pk)
    if request.method=="POST":

       form = bidsForm(request.POST)
       if form.is_valid():
           inputprice = form.cleaned_data["price"]
       if  bids.objects.filter(item=productdetails).last():
           if inputprice > bids.objects.filter(item=productdetails).last().price:
              findingbids=bids(user=request.user, price=inputprice, item=productdetails)
              findingbids.save()
       else:
               if inputprice > productdetails.price:
                   findingbids = bids(user=request.user, item=productdetails, price=inputprice)
                   findingbids.save()

    form = bidsForm()

    formcomment = commentForm()

    bid = bids.objects.filter(item=productdetails).last()
    comments = Comment.objects.filter(auctioninfo=productdetails)
    return render(request,"auctions/Listing.html",{
                  "productdetails":productdetails,
                  "formcomment": formcomment,
                  "form": form,
                  "bid" : bid,
                  "comments":comments
             })

def addwatchlist(request,product_id):
     productsinfo = auction.objects.get(id=product_id)
     w = watchlist(product=productsinfo, user=request.user)
     w.save()
     return HttpResponseRedirect(reverse ("watchlist"))

def watch(request):
    watch = watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watch":watch
    })

def remove(request,watchlist_id):
   wa= watchlist.objects.get(pk=watchlist_id)
   wa.delete()
   return HttpResponseRedirect(reverse ("watchlist"))

def closebid(request,product_id):
    closingbid= auction.objects.get(pk=product_id)
    if request.user == closingbid.user:
         closingbid.openorclosed = 1
         closingbid.save()
    return HttpResponseRedirect(reverse("details",kwargs={ 'pk':product_id}))



def comment(request,pk):
    commentinfo = auction.objects.get(pk=pk)
    if request.method == "POST":

        form = commentForm(request.POST)
        if form.is_valid():
            comments =form.save(commit=False)
            comments.auctioninfo =commentinfo
            comments.user = request.user
            comments.save()
            return HttpResponseRedirect(reverse("details", kwargs={'pk': pk}))

























