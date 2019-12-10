from unittest import TestCase
from rest_framework.test import RequestsClient
from rest_framework.test import APIRequestFactory
from notification_service.classes.EmailData import EmailData
from notification_service.classes.UserComplaint import UserComplaint
from notification_service.classes.MessageText import MessageText
import json
import django
django.setup()

# NOTE - This test suite was setup initially to test the service, but has not
# been updated as we modified because we decided that manually walking through
# test steps was more effective for testing the whole service functionality and interactions
# All services have been tested manually 

class test_notifications(TestCase):

    def test_email_data(self):
        email = EmailData("fake_user", "fake_email", "fake_subject", "fake_message")
        mock_message_data = {
            'Messages': [
                {
                    "From": {
                        "Email": "skoop@uchicago.edu",
                        "Name": "A+Ocean"
                    },
                    "To": [
                        {
                            "Email": "fake_email",
                            "Name": "fake_user"
                        }
                    ],
                    "Subject": "fake_subject",
                    "TextPart": "fake_subject",
                    "HTMLPart": "fake_message",
                    "CustomID": "AppGettingStartedTest"
                }
            ]
        }
        self.assertEqual(email.get_message_data(), mock_message_data)

    def test_user_complaint(self):
        complaint = UserComplaint(1, "fake_user", "fake_email", "fake_message", "fake_date")
        mock_complaint_data = {
                "message_id": "1",
                "user": "fake_user",
                "email": "fake_email",
                "message": "fake_message",
                "date": "fake_date"}
        self.assertEqual(complaint.get_json(), mock_complaint_data)

    def test_message_watchlist(self):
        message = MessageText("watchlist", {"item": "mock_item"})
        self.assertEqual(message.get_message_subject(), "Watchlist Appearance")
        self.assertEqual(message.get_message_text(), "<h3>Auction Starting for Item on Watchlist</h3><br/>An auction "
                                                     "on item mock_item on your watchlist is starting. Place a bid "
                                                     "before time runs out!")

    def test_message_seller_bid(self):
        message = MessageText("seller_bid", {"item": "mock_item", "bid": "mock_bid"})
        self.assertEqual(message.get_message_subject(), "New Bid Placed on Your Item")
        self.assertEqual(message.get_message_text(), "<h3>New Bid Placed</h3><br/>A new bid on your item mock_item "
                                                     "has been placed. New bid amount: mock_bid")

    def test_message_higher_bid(self):
        message = MessageText("higher_bid", {"item": "mock_item", "bid": "mock_bid"})
        self.assertEqual(message.get_message_subject(), "Higher Bid Placed")
        self.assertEqual(message.get_message_text(), "<h3>Higher Bid Placed</h3><br/>A higher bid has been placed on "
                                                     "item mock_item. Higher bid amount: mock_bid. Place a higher bid "
                                                     "now for a chance to purchase!")

    def test_message_winning_bid(self):
        message = MessageText("winning_bid", {"item": "mock_item", "bid": "mock_bid"})
        self.assertEqual(message.get_message_subject(), "You've Placed the Winning Bid!")
        self.assertEqual(message.get_message_text(), "<h3>Winning Bid Placed!</h3><br/>Congratulations! You've placed "
                                                     "the winning bid on item mock_item. Winning bid amount: "
                                                     "mock_bid. Please log in to A+Ocean to complete purchase.")

    def test_message_auction_expired(self):
        message = MessageText("auction_expiration", {"item": "mock_item", "auction": "mock_auction"})
        self.assertEqual(message.get_message_subject(), "Auction Expired")
        self.assertEqual(message.get_message_text(), "<h3>Auction Expired</h3><br/>Auction mock_auction for item "
                                                     "mock_item has expired. Please log in to A+Ocean to view "
                                                     "results.")

    def test_index(self):
        factory = APIRequestFactory()
        client = RequestsClient()
        response = client.get('http://localhost:8080/')
        content = response.content.decode("utf-8")
        self.assertEqual(content, "Hello, world. You're at the main index.")

    def test_shipping_confirmation_get(self):
        client = RequestsClient()
        response = client.get('http://localhost:8080/confirmations/shipping/')
        content = response.content.decode("utf-8")
        self.assertEqual(content, "Shipping confirmation endpoint.")
