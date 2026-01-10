from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings
class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length = 60)

    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    active = models.BooleanField(default=True)



    def save(self, *args, **kwargs):
        #Check if this is a new record
        if not self.pk:
            self.current_price = self.starting_bid
            self.is_active = True
        super().save(*args, **kwargs)


class Bid(models.Model):

    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    # PROTECT  prevents deleting users who have active financial records
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="bids")

    amount = models.DecimalField(decimal_places=2, max_digits=10)  # Increased max_digits
    timestamp = models.DateTimeField(auto_now_add=True)  # Essential for auction history

    def __str__(self):
        return f"${self.amount} on {self.auction.title} by {self.user.username}"

    class Meta:

        ordering = ['-amount']


class Category:

    def _str(self):
        pass
