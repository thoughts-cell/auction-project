from django import forms
from auctions.models import Listing, Category, Bid,Comment

class NewAuctionForm(forms.ModelForm):
    class Meta:
        model =Listing
        fields =['title','description','image_url', 'starting_bid']


class BidForm:
    def __init__(self,*args,**kwargs):
        self.auction = kwargs.pop('auction')
        super(BidForm,self).__init__(*args,**kwargs)

    def clean(self):
        amount = self.cleand_data['amount']
        if amount <= self.auction.current_price:
            raise forms.ValidationError("Your bid is lower than current price")

        return self.cleaned_data

    class Meta:
        model = Bid
        fields = ['amount']


class CommentForm:
    class Meta:
        model = Comment
        fields = ['body']