# Notification Service

## Endpoints

| Endpoint  | What it Does  |
| ------------|-------------|
| `/notifications/` |   Sends an email to the user email address included in the body via Mailjet API with email message based on the notification type included in the request body |
| `/complaints/` |   Adds or retrieves user support messages |
| `/complaints/admin/` |   Sends an email to the user email address included in the body via Mailjet API with email message from the customer support admin |

## Endpoint Details

| Endpoint  | Methods  | Input |
| ------------|-------------|-------------|
| `/notifications/` |   POST | `body = {"type": "watchlist", "item": item, "username": username, "email": email_address}` <br> OR <br> `body = {"type": "seller_bid", "item": item, "bid": bid, "username": username, "email": email_address}` <br> OR <br> `body = {"type": "higher_bid", "item": item, "bid": bid, "username": username, "email": email_address}` <br> OR <br> `body = {"type": winning_bid", "item": item, "bid": bid, "username": username, "email": email_address}` <br> OR <br> `body = {"type": auction_expiration", "item": item, "auction": auction_id, "username": username, "email": email_address}`|
| `/complaints/` |   GET, POST |   `body = {"username": username, "email": email_address, "message": message_text}` |
| `/complaints/admin/` |  POST |  `body = {"email": email_address, "message": message_text, "message_id": message_id}` |


### Sources:
- https://stackoverflow.com/questions/17716624/django-csrf-cookie-not-set
- https://app.mailjet.com/auth/get_started/developer
- https://stackoverflow.com/questions/43357687/django-python-rest-framework-no-access-control-allow-origin-header-is-present
- https://stackoverflow.com/questions/43250263/bootstrap-4-file-input
- https://stackoverflow.com/questions/37225035/serialize-in-json-a-base64-encoded-data
