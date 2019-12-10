class MessageText:

    def __init__(self, notification_type, request_data):
        self.notification_type = notification_type
        self.request_data = request_data

    def get_message_subject(self):
        notification_subjects = {"watchlist": "Watchlist Appearance",
                                 "seller_bid": "New Bid Placed on Your Item",
                                 "higher_bid": "Higher Bid Placed",
                                 "winning_bid": "You've Placed the Winning Bid!",
                                 "auction_expiration": "Auction Expiring Soon",
                                 "auction_expiration_seller": "Auction Expiring Soon"}
        return notification_subjects[self.notification_type]

    def get_message_text(self):
        if self.notification_type == "watchlist":
            return self.get_watchlist_text()
        elif self.notification_type == "seller_bid":
            return self.get_seller_bid_text()
        elif self.notification_type == "higher_bid":
            return self.get_higher_bid_text()
        elif self.notification_type == "winning_bid":
            return self.get_winning_bid_text()
        elif self.notification_type == "auction_expiration":
            return self.get_auction_expired_text()
        elif self.notification_type == "auction_expiration_seller":
            return self.get_auction_expired_seller_text()
        else:
            return "Error"

    def get_watchlist_text(self):
        item = self.request_data["item"]
        return "<h3>Item on Watchlist Added</h3><br/>An item " \
               + item + " that matches your watchlist has been added. Log into A+Ocean to view it!"

    def get_seller_bid_text(self):
        item = self.request_data["item"]
        bid = self.request_data["bid"]
        return "<h3>New Bid Placed</h3><br/>A new bid on your item " \
               + item + " has been placed. New bid amount: " + bid

    def get_higher_bid_text(self):
        item = self.request_data["item"]
        bid = self.request_data["bid"]
        return "<h3>Higher Bid Placed</h3><br/>A higher bid has been placed on item " \
               + item + ". Higher bid amount: " + bid + ". Place a higher bid now for a chance to purchase!"

    def get_winning_bid_text(self):
        item = self.request_data["item"]
        bid = self.request_data["bid"]
        return "<h3>Winning Bid Placed!</h3><br/>Congratulations! You've placed the winning bid on item " \
               + item + ". Winning bid amount: " + bid + ". Please log in to A+Ocean to complete purchase."

    def get_auction_expired_text(self):
        item = self.request_data["item"]
        return "<h3>Auction Expiring Soon</h3><br/>Auction for item " + item + \
               " is expiring soon!. Please log in to A+Ocean to place a final bid."

    def get_auction_expired_seller_text(self):
        item = self.request_data["item"]
        return "<h3>Auction Expiring Soon</h3><br/>Your auction for item " + item + \
                   " is expiring soon!. Please log in to A+Ocean to view results."
