from django.contrib import admin
from unicodedata import category

from .models import Bid,Category,Listing
#register models

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title','category','starting_bid')

admin.site.register(Bid,AuctionAdmin)