from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new/", views.new_auction, name="new_auction"),
    path("auction/<int:pk>/", views.auction_view, name='auction_view'),
    path("auction/<int:pk>/favourite/", views.favourite_post, name='favourite_post'),
    path("auction/<int:pk>/end/", views.end_auction, name="end_auction"),


    path("watchlist/", views.bookmarks, name="bookmarks"),  # "watchlist" is standard for auctions
    path("categories/", views.CategoriesView.as_view(), name="categories"),
    path("categories/<slug:slug>/", views.CategoryListings.as_view(), name="category_listings")
]
