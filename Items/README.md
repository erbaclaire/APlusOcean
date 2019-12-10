# Items Service

## Endpoints

| Endpoint  | What it Does  |
| ------------|-------------|
| `/view_inventory/` |  Returns a json array of all items in the Items Service with all details including item_id, item_name, item_pic, category, item_desc, quantity, start_price, shipping_costs, flagged, auction_start_time, auction_end_time, auction_end_notif_time, buy_now, auction_live_now, in_cart, cart_id, sold, sold_to_account_id, and date_posted. Navigate to /Items/items_service/items_service/models.py to find out more about this variables. |
| `/add_item/` |   Adds an item to the Items Service database based on a frontend form |
| `/get_item_/` |   Returns the details of one item |
| `/seller_update_item/` |   Updates an item in the Items Service database based on a frontend form |
| `/flag_item/` |   Flags an item |
| `/view_flagged_item/` |   Returns a json array of all flagged items in the Items Service with all details including item_id, item_name, item_pic, category, item_desc, quantity, start_price, shipping_costs, flagged, auction_start_time, auction_end_time, auction_end_notif_time, buy_now, auction_live_now, in_cart, cart_id, sold, sold_to_account_id, and date_posted. Navigate to /Items/items_service/items_service/models.py to find out more about this variables. |
| `/get_search_results/` |   Returns a json array of all items that matches the category and item description given by the user in the Items Service with all details including item_id, item_name, item_pic, category, item_desc, quantity, start_price, shipping_costs, flagged, auction_start_time, auction_end_time, auction_end_notif_time, buy_now, auction_live_now, in_cart, cart_id, sold, sold_to_account_id, and date_posted.|
| `/add_category/` |   Adds a new category.|
| `/remove_category/` |   Removes a category.|
| `/update_category/` |   Updates a category.|

## Endpoint Details

| Endpoint  | Methods  | Input |
| ------------|-------------|-------------|
| `/view_inventory/` |  GET | <code> `body = {"item_id"=item_id}` <code> |
| `/add_inventory/` |  POST | <code> `body = {"account_id"=account_id, "item_name"=item_name, "category"=category, "item_desc"=item_desc, "quantity"=quantity, "start_price"=start_price, "shipping_cost"=shipping_cost, "auction_start_time"=auction_start_time, "auction_end_time"=auction_end_time, "auction_end_notif_time"=auction_end_notif_time, "buy_now"=buy_now}` <code> |
| `/get_item/` |  GET | <code> `body = {"item_id"=item_id}` <code> |
| `/seller_item_update/` |  POST | <code> `body = {"item_id":item_id, account_id"=account_id, "item_name"=item_name, "category"=category, "item_desc"=item_desc, "quantity"=quantity, "start_price"=start_price, "shipping_cost"=shipping_cost, "auction_start_time"=auction_start_time, "auction_end_time"=auction_end_time, "auction_end_notif_time"=auction_end_notif_time, "buy_now"=buy_now}` <code> |
| `/flag_item/` |  POST | <code> `body = {"item_id"=item_id}` <code> |
| `/view_flagged_items/` |  GET | |
| `/get_search_results/` |  GET | `body = {"item_name contains item_desc, "category_id"=category_id}` <code>|
| `/add_category/` |  POST | `body = {"category"=category}` <code>|
| `/remove_category/` |  POST | `body = {"category_id"=category_id}` <code>|
| `/update_category/` |  POST | `body = {"category_id"=category_id, "category"=new_category_name}` <code>|