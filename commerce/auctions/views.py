from decimal import Decimal

from django.contrib.admin.templatetags.admin_list import pagination
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.db.models import Max
from django.views import View
from django.contrib import messages
def index(request):
    return render(request, "auctions/index.html")
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView

from .models import User, Listing, Bid, Category
from .forms import NewAuctionForm, BidForm, CommentForm


def IndexListView(ListView):
    model = Listing
    template_name = "auctions/index.html"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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


        


class CategoryListings(ListView):
    template_name = "auctions/category_listings.html"
    model = Listing
    context_object_name = 'listings'
    
    def get_queryset(self):
        category_slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=category_slug)
        return Listing.objects.filter(category=category, is_active=True)


@login_required
def watchlist(request):
    watched_items = request.user.favoured.all()
    return render(request, "auctions/watchlist.html", {"listings": watched_items})


@login_required
def new_auction(request):
    if request.method == "POST":
        form = NewAuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.user = request.user
            auction.current_price = auction.starting_bid
            auction.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = NewAuctionForm()
    return render(request, "auctions/new_auction.html", {"form": form})

def auction_view(request, pk):
    auction = get_object_or_404(Listing, pk=pk)
    favoured = False
    if request.user.is_authenticated:
        favoured = auction.favoured.filter(id = request.user.id).exists()

    top_bid = auction.bid_set.order_by("-amount").first()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect("login")

        if 'bid' in request.POST:
            bid_form = BidForm(request.POST, auction=auction)
            if bid_form.is_valid():
                temp = bid_form.save(commit=False)
                temp.user = request.user
                temp.auction =  auction
                temp.save()

                #update the price
                auction.current_price = temp.amount
                auction.save()
                return redirect("auction_view", pk=auction.pk)

            elif 'comment' in request.POST:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    temp = comment_form.save(commit=False)
                    temp.user = request.user
                    temp.auction = auction
                    temp.save()
                    return redirect("auction_view",pk = auction.pk)

        increment  = Decimal("0.01")
        minimum_bid = auction.current_price + increment
        bid_form = BidForm(initial={"amount": minimum_bid}, auction=auction)
        comment_form = CommentForm()
    return render(request,"auctions/auction_view.html",{
        "auction": auction,
        "bid_form": bid_form,
        "favoured": favoured,
         "top_bid": top_bid,
        "comment_form": comment_form,
        "comments": auction.comments.all().order_by("-created_on")
    })

@login_required
def end_auction(request, pk):
    auction = get_object_or_404(Listing, pk=pk)
    if request.user.is_authenticated and request.user == auction.user:
        auction.is_active = False
        auction.save()
    return HttpResponseRedirect(reverse("auction_view", args=[pk]))


@login_required
def add_to_watchlist(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if listing.favoured.filter(id=request.user.id).exists():
        listing.favoured.remove(request.user)
        messages.info(request, "Removed from watchlist")
    else:
        listing.favoured.add(request.user)
        messages.info(request, "Added to watchlist")
    return HttpResponseRedirect(reverse("auction_view", args=[pk]))


class CategoriesView(ListView):
    template_name = "auctions/categories.html"
    model = Category
    context_object_name = "categories"
