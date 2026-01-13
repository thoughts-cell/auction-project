from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse
class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length = 60)
    description = models.TextField(max_length=1000)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    favoured =models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="favoured")



    def save(self, *args, **kwargs):
        #Check if this is a new record
        if not self.pk:
            self.current_price = self.starting_bid
            self.is_active = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("listing", kwargs={"pk": self.pk})

class Bid(models.Model):

    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="bids")

    amount = models.DecimalField(decimal_places=2, max_digits=10)  # Increased max_digits
    timestamp = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return f"${self.amount} on {self.auction.title} by {self.user.username}"

    class Meta:

        ordering = ['-amount']


class Category(models.Model):

    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(null = False, unique=True)

    def __str__(self):
        return self.name
    class Meta:
       verbose_name_plural = "categories"
    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})

class Comment(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"{self.user} comment on {self.auction}"