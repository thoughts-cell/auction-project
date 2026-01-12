from gc import get_objects

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView

from .models import User, Listing, Bid, Category
from .forms import NewAuctionForm ,BidForm,CommentForm

def index(request):
    return render(request, "auctions/index.html")


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


def auction_view(request,pk):
    auction = get_object_or_404(Listing, pk=pk)
    favoured = False
    if request.user.is_authenticated:
        favoured = auction.favourite.filter(user=request.user.id).exists()
    #get top_bid using .first()
    top_bid = auction.bid_set.filter(user=request.user.id).first()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        if 'bid' in request.POST:
            bid_form =BidForm(request.POST,auction =auction)
            if bid_form.is_valid():
                temp = bid_form.save(commit=False)
                temp.user = request.user
                temp.auction = auction
                temp.save()

                # Sync price
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
                    return redirect("auction_view", pk=auction.pk)

            else:
                # 4. Use string for Decimal to ensure precision
                minimum_bid = auction.current_price + Decimal("0.01")
                bid_form = BidForm(initial={"amount": minimum_bid}, auction=auction)
                comment_form = CommentForm()

            return render(request, "auctions/auction_view.html", {
                "auction": auction,
                "bid_form": bid_form,
                "favoured": favoured,
                "top_bid": top_bid,
                "comment_form": comment_form,
                "comments": auction.comment_set.all()  # Or auction.comments.all() if related_name set
            })

class CategoryListings(ListView):
    template_name = "auctions/category_listings.html"
    model = Listing
    context_object_name = 'listings'
    
    def get_queryset(self):
        category_slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=category_slug)
        return Listing.objects.filter(category=category, is_active=True)


def bookmarks(request):
    return None




@login_required
def new_auction(request):
    if request.method == "POST":
        form = NewAuctionForm(request.POST)
        if  form.is_valid():
            auction = form.save(commit=False)
            auction.user = request.user
            obj = form.save(commit=False)

            obj.owner = request.user
            obj.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            form  = NewAuctionForm()
        return render((request, "auctions/new_auction.html", {"form": form}))

def end_auction(request):
    return None


def favourite_post(request):
    return None


class CategoriesView(ListView):
    template_name = "auctions/categories.html"
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context