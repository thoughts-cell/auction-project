from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'starting_bid', 'current_price', 'is_active']
    list_filter = ['is_active', 'category', 'user']
    search_fields = ['title', 'description']
    readonly_fields = ['current_price']


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['amount', 'auction', 'user', 'timestamp']
    list_filter = ['timestamp', 'auction']
    search_fields = ['auction__title', 'user__username']
    readonly_fields = ['timestamp']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'auction', 'created_on']
    list_filter = ['created_on', 'auction']
    search_fields = ['body', 'user__username', 'auction__title']
    readonly_fields = ['created_on']

