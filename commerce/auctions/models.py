from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse("category_listings", kwargs={"slug": self.slug})

class Listing(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=1000)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null = True,blank=False, related_name="category_listings")
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="listings")
    favoured = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="favoured")



    def save(self, *args, **kwargs):

        if not self.pk:
            if not self.starting_bid:
                self.starting_bid = self.current_price

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("auction_view", kwargs={"pk": self.pk})


class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="bids")

    amount = models.DecimalField(decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.amount} on {self.auction.title} by {self.user.username}"

    class Meta:
        ordering = ['-amount']




class Comment(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        username = self.user.username if self.user else 'Anonymous'
        return f"{self.user} comment on {self.auction}"
