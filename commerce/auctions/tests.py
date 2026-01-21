from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Category, Listing, Bid, Comment


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


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(str(self.category), 'Test Category')


class ListingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='pass123'
        )
        # Use get_or_create to avoid duplicate unique constraint
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


class ViewsTest(TestCase):
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