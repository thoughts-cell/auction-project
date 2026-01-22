from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from .models import User, Category, Listing, Bid, Comment
from .forms import NewAuctionForm, BidForm, CommentForm


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')

    def test_user_authentication(self):
        user = authenticate(username='testuser', password='testpass123')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')

    def test_user_invalid_password(self):
        user = authenticate(username='testuser', password='wrongpassword')
        self.assertIsNone(user)


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(str(self.category), 'Test Category')

    def test_category_slug_unique(self):
        with self.assertRaises(Exception):
            Category.objects.create(name='Another', slug='test-category')


class ListingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='pass123'
        )
        self.category, _ = Category.objects.get_or_create(
            name='Electronics',
            defaults={'slug': 'electronics'}
        )
        self.listing = Listing.objects.create(
            title='iPhone 14',
            description='Used iPhone 14',
            starting_bid=500.00,
            current_price=500.00,
            user=self.user,
            category=self.category
        )

    def test_listing_creation(self):
        self.assertEqual(self.listing.title, 'iPhone 14')
        self.assertEqual(self.listing.user, self.user)
        self.assertEqual(self.listing.category, self.category)
        self.assertTrue(self.listing.is_active)
        self.assertEqual(str(self.listing), 'iPhone 14')

    def test_listing_with_image_url(self):
        listing = Listing.objects.create(
            title='Laptop',
            description='Gaming Laptop',
            starting_bid=1000.00,
            current_price=1000.00,
            image_url='https://example.com/laptop.jpg',
            user=self.user,
            category=self.category
        )
        self.assertEqual(listing.image_url, 'https://example.com/laptop.jpg')

    def test_listing_close(self):
        self.listing.is_active = False
        self.listing.save()
        self.assertFalse(self.listing.is_active)

    def test_listing_watchlist_add_remove(self):
        buyer = User.objects.create_user(username='buyer', password='pass')
        self.listing.favoured.add(buyer)
        self.assertTrue(self.listing.favoured.filter(id=buyer.id).exists())
        
        self.listing.favoured.remove(buyer)
        self.assertFalse(self.listing.favoured.filter(id=buyer.id).exists())


class BidModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='bidder',
            email='bidder@example.com',
            password='pass123'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='pass123'
        )
        self.category, _ = Category.objects.get_or_create(
            name='Electronics',
            defaults={'slug': 'electronics'}
        )
        self.listing = Listing.objects.create(
            title='iPhone 14',
            description='Used iPhone 14',
            starting_bid=500.00,
            current_price=500.00,
            user=self.seller,
            category=self.category
        )
        self.bid = Bid.objects.create(
            amount=550.00,
            user=self.user,
            auction=self.listing
        )

    def test_bid_creation(self):
        self.assertEqual(self.bid.amount, 550.00)
        self.assertEqual(self.bid.user, self.user)
        self.assertEqual(self.bid.auction, self.listing)
        self.assertIsNotNone(self.bid.timestamp)

    def test_multiple_bids(self):
        second_bid = Bid.objects.create(
            amount=600.00,
            user=self.seller,
            auction=self.listing
        )
        self.assertEqual(self.listing.bids.count(), 2)

    def test_bid_ordering(self):
        bids = self.listing.bids.all()
        # Bids should be ordered by -amount
        amounts = list(bids.values_list('amount', flat=True))
        self.assertEqual(amounts, sorted(amounts, reverse=True))


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='commenter',
            email='commenter@example.com',
            password='pass123'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='pass123'
        )
        self.category, _ = Category.objects.get_or_create(
            name='Electronics',
            defaults={'slug': 'electronics'}
        )
        self.listing = Listing.objects.create(
            title='iPhone 14',
            description='Used iPhone 14',
            starting_bid=500.00,
            current_price=500.00,
            user=self.seller,
            category=self.category
        )
        self.comment = Comment.objects.create(
            body='Great item!',
            user=self.user,
            auction=self.listing
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.body, 'Great item!')
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.auction, self.listing)
        self.assertIsNotNone(self.comment.created_on)

    def test_multiple_comments(self):
        comment2 = Comment.objects.create(
            body='Excellent seller!',
            user=self.seller,
            auction=self.listing
        )
        self.assertEqual(self.listing.comments.count(), 2)


class FormTests(TestCase):
    def setUp(self):
        self.category, _ = Category.objects.get_or_create(
            name='Electronics',
            defaults={'slug': 'electronics'}
        )

    def test_new_auction_form_valid(self):
        form_data = {
            'title': 'Test Item',
            'description': 'Test Description',
            'image_url': 'https://example.com/image.jpg',
            'starting_bid': 100.00,
            'category': self.category.id,
        }
        form = NewAuctionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_new_auction_form_missing_title(self):
        form_data = {
            'title': '',
            'description': 'Test Description',
            'starting_bid': 100.00,
            'category': self.category.id,
        }
        form = NewAuctionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_new_auction_form_missing_description(self):
        form_data = {
            'title': 'Test Item',
            'description': '',  # Missing description
            'starting_bid': 100.00,
            'category': self.category.id,
        }
        form = NewAuctionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_bid_form_valid(self):
        seller = User.objects.create_user(username='seller', password='pass')
        listing = Listing.objects.create(
            title='Item',
            description='Desc',
            starting_bid=100.00,
            current_price=100.00,
            user=seller,
            category=self.category
        )
        form = BidForm(data={'amount': 150.00}, auction=listing)
        self.assertTrue(form.is_valid())

    def test_bid_form_insufficient_amount(self):
        seller = User.objects.create_user(username='seller', password='pass')
        listing = Listing.objects.create(
            title='Item',
            description='Desc',
            starting_bid=100.00,
            current_price=100.00,
            user=seller,
            category=self.category
        )
        form = BidForm(data={'amount': 50.00}, auction=listing)
        self.assertFalse(form.is_valid())

    def test_comment_form_valid(self):
        form = CommentForm(data={'body': 'Great item!'})
        self.assertTrue(form.is_valid())

    def test_comment_form_empty(self):
        form = CommentForm(data={'body': ''})
        self.assertFalse(form.is_valid())


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category, _ = Category.objects.get_or_create(
            name='Electronics',
            defaults={'slug': 'electronics'}
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_new_auction_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('new_auction'))
        self.assertEqual(response.status_code, 200)

    def test_new_auction_view_unauthenticated(self):
        response = self.client.get(reverse('new_auction'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_create_auction(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('new_auction'), {
            'title': 'Test Item',
            'description': 'Test Description',
            'starting_bid': 100.00,
            'category': self.category.id,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Listing.objects.count(), 1)

    def test_auction_view_display(self):
        listing = Listing.objects.create(
            title='Test Item',
            description='Test',
            starting_bid=100.00,
            current_price=100.00,
            user=self.user,
            category=self.category
        )
        response = self.client.get(reverse('auction_view', args=[listing.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')

    def test_watchlist_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, 200)

    def test_watchlist_view_unauthenticated(self):
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_categories_view(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)

    def test_category_listings_view(self):
        response = self.client.get(reverse('category_listings', args=['electronics']))
        self.assertEqual(response.status_code, 200)


class AuctionLogicTests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='pass123'
        )
        self.bidder1 = User.objects.create_user(
            username='bidder1',
            email='bidder1@example.com',
            password='pass123'
        )
        self.bidder2 = User.objects.create_user(
            username='bidder2',
            email='bidder2@example.com',
            password='pass123'
        )
        self.category, _ = Category.objects.get_or_create(
            name='Electronics',
            defaults={'slug': 'electronics'}
        )
        self.listing = Listing.objects.create(
            title='Auction Item',
            description='Test auction',
            starting_bid=100.00,
            current_price=100.00,
            user=self.seller,
            category=self.category
        )

    def test_bid_increases_current_price(self):
        initial_price = self.listing.current_price
        bid = Bid.objects.create(
            amount=150.00,
            user=self.bidder1,
            auction=self.listing
        )
        self.listing.current_price = bid.amount
        self.listing.save()
        self.listing.refresh_from_db()
        self.assertGreater(self.listing.current_price, initial_price)

    def test_multiple_bids_increment(self):
        Bid.objects.create(amount=150.00, user=self.bidder1, auction=self.listing)
        Bid.objects.create(amount=200.00, user=self.bidder2, auction=self.listing)
        Bid.objects.create(amount=250.00, user=self.bidder1, auction=self.listing)
        
        self.assertEqual(self.listing.bids.count(), 3)

    def test_close_auction(self):
        self.assertTrue(self.listing.is_active)
        self.listing.is_active = False
        self.listing.save()
        self.assertFalse(self.listing.is_active)

    def test_highest_bid_retrieval(self):
        Bid.objects.create(amount=150.00, user=self.bidder1, auction=self.listing)
        Bid.objects.create(amount=200.00, user=self.bidder2, auction=self.listing)
        Bid.objects.create(amount=175.00, user=self.bidder1, auction=self.listing)
        
        highest_bid = self.listing.bids.first()
        self.assertEqual(highest_bid.amount, 200.00)