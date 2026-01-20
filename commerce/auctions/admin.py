from django.contrib import admin

from .models import Bid, Category, Listing


# Admin for Listing (Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'starting_bid', 'current_price', 'is_active', 'user')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'description')


# Admin for Bid
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'user', 'amount', 'timestamp')
    list_filter = ('timestamp',)


# Admin for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


# Register models
admin.site.register(Listing, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
