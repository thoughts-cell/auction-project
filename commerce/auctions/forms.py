from django import forms
from .models import Listing, Category, Bid, Comment


class NewAuctionForm(forms.ModelForm):
    image_url = forms.CharField(
        required=False, 
        widget=forms.URLInput(attrs={
            'placeholder': 'https://example.com/image.jpg',
            'class': 'validate'
        }),
        label='url of image(optional)'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select a category"
        self.fields['category'].queryset = Category.objects.all()

    def clean_image_url(self):
        image_url = self.cleaned_data.get('image_url')
        if image_url and not image_url.startswith(('http://', 'https://')):
            image_url = 'https://' + image_url
        return image_url if image_url else None

    class Meta:
        model = Listing
        fields = ['title', 'description', 'image_url', 'starting_bid','category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'validate'}),
            'description': forms.Textarea(attrs={'class': 'materialize-textarea'}),
            'starting_bid': forms.NumberInput(attrs={'step': '0.01'}),
            'category': forms.Select(attrs={'class':'browser-default'}),
        }
        labels = {
            'title': 'product name',
            'description': 'description of product',
            'starting_bid': 'starting price',
            'category': '',
        }

class BidForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.auction = kwargs.pop('auction', None)
        super(BidForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'class': 'validate', 'step': '0.01'})

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if self.auction :
            if amount <= self.auction.current_price:

                raise forms.ValidationError(f"you must bid higher than ${self.auction.current_price}")

        return amount

    class Meta:
        model = Bid
        fields = ['amount']
        labels = {'amount': 'Amount to bid $'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'materialize-textarea',
                'placeholder': 'enter your comment here...',
                'data-length': '500'
            }),
        }
        labels = {'body': ''}