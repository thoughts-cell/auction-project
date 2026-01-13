from django import forms
from .models import Listing, Category, Bid, Comment


class NewAuctionForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'image_url', 'starting_bid']


class BidForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.auction = kwargs.pop('auction', None)
        super(BidForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if self.auction and amount <= self.auction.current_price:
            raise forms.ValidationError("Your bid must be higher than the current price")
        return amount

    class Meta:
        model = Bid
        fields = ['amount']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']