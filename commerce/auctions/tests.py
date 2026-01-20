from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Listing, Category, User, Bid


class AuctionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.listing = Listing.objects.create(
            title="Laptop",
            description="A great laptop",
            starting_bid=Decimal("500.00"),
            current_price=Decimal("500.00"),
            user=self.user,
            category=self.category
        )

    def test_listing_creation(self):
        """Test if a listing is created correctly with default values"""
        l = self.listing
        self.assertEqual(l.title, "Laptop")
        self.assertTrue(l.is_active)
        self.assertEqual(str(l), "Laptop")

    def test_index_page(self):
        """Test if the home page loads correctly"""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Laptop")

    def test_auction_detail_page(self):
        """Test if a specific auction page loads"""
        response = self.client.get(reverse("auction_view", kwargs={"pk": self.listing.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A great laptop")

    def test_invalid_bid(self):
        """Test that a bid lower than current price fails"""
        self.client.login(username="testuser", password="password123")

        # Attempt to bid $400 on a $500 item
        response = self.client.post(
            reverse("auction_view", kwargs={"pk": self.listing.id}),
            {"amount": 400.00, "bid": "Submit"}  # Trigger the 'bid' logic
        )

        # 1. Check that we stayed on the page (didn't redirect)
        self.assertEqual(response.status_code, 200)

        # 3. Double-check the database to ensure price hasn't changed
        self.listing.refresh_from_db()
        self.assertContains(response, "you must bid higher than $500.00")

    def test_watchlist_toggle(self):
        """Test adding/removing from watchlist"""
        self.client.login(username="testuser", password="password123")

        # Add to watchlist
        self.client.get(reverse("add_to_watchlist", kwargs={"pk": self.listing.id}))
        self.assertTrue(self.listing.favoured.filter(id=self.user.id).exists())

        # Remove from watchlist
        self.client.get(reverse("add_to_watchlist", kwargs={"pk": self.listing.id}))
        self.assertFalse(self.listing.favoured.filter(id=self.user.id).exists())

    def test_end_auction_permissions(self):
        """Only the owner should be able to end the auction"""
        # Create a second user
        other_user = User.objects.create_user(username="hacker", password="password123")
        self.client.login(username="hacker", password="password123")

        # Hacker tries to end 'testuser's auction
        response = self.client.get(reverse("end_auction", kwargs={"pk": self.listing.id}))

        self.listing.refresh_from_db()
        # The auction should still be active
        self.assertTrue(self.listing.is_active)

        # Now the real owner logs in
        self.client.login(username="testuser", password="password123")
        self.client.get(reverse("end_auction", kwargs={"pk": self.listing.id}))

        self.listing.refresh_from_db()
        # Now it should be closed
        self.assertFalse(self.listing.is_active)

    def test_category_listings_filter(self):
        """Test that the category page filters correctly    """
        # create a different category item
        other_cat = Category.objects.create(name="Books", slug="books")
        Listing.objects.create(
            title="Python Book",
            description="Learn Django",
            starting_bid=10,
            current_price=10,
            user=self.user,
            category=other_cat
        )
        # Visit 'Electronics' category page
        response = self.client.get(reverse("category_listings", kwargs={"slug": "electronics"}))

        self.assertContains(response, "Laptop")
        self.assertNotContains(response, "Python Book")

    def test_winner_message_display(self):
        winner = User.objects.create_user(username="winner", password="password123")
        Bid.objects.create(user=winner, auction=self.listing, amount=600.00)

        self.listing.is_active = False
        self.listing.save()

        self.client.login(username="winner", password="password123")
        response = self.client.get(reverse("auction_view", kwargs={"pk": self.listing.id}))

        self.assertNotContains(response, 'name="bid"')
