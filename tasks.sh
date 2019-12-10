


osascript -e 'tell application "Terminal" to do script "cd /Users/matthewpozsgai/Documents/GitHub/APlusOcean/Items;docker-compose exec items_service python ./items_service/auction_timer_task.py"'

osascript -e 'tell application "Terminal" to do script "cd /Users/matthewpozsgai/Documents/GitHub/APlusOcean/Items;docker-compose exec items_service python ./items_service/rpc_task.py"'

osascript -e 'tell application "Terminal" to do script "cd /Users/matthewpozsgai/Documents/GitHub/APlusOcean/Accounts;docker-compose exec accounts_service python ./accounts_service/watchlist_task.py"'

osascript -e 'tell application "Terminal" to do script "cd /Users/matthewpozsgai/Documents/GitHub/APlusOcean/Notifications;docker-compose exec notifications_service python ./notification_service/notifications_task.py"'

osascript -e 'tell application "Terminal" to do script "cd /Users/matthewpozsgai/Documents/GitHub/APlusOcean/Auctions;docker-compose exec auctions_service python ./auctions_service/place_bid_task.py"'

osascript -e 'tell application "Terminal" to do script "cd /Users/matthewpozsgai/Documents/GitHub/APlusOcean/Auctions;docker-compose exec auctions_service python ./auctions_service/auction_ending_warning_task.py"'

osascript -e 'tell application "Terminal" to do script "cd /Users/matthewpozsgai/Documents/GitHub/APlusOcean/Auctions;docker-compose exec auctions_service python ./auctions_service/auction_over_task.py"'

osascript -e 'tell application "Terminal" to do script "cd /Users/matthewpozsgai/Documents/GitHub/APlusOcean/Auctions;docker-compose exec auctions_service python ./auctions_service/remove_bids_task.py"'

osascript -e 'tell application "Terminal" to do script "cd /Users/matthewpozsgai/Documents/GitHub/APlusOcean/Carts;docker-compose exec carts_service python ./carts_service/add_to_cart_task.py"'

osascript -e 'tell application "Terminal" to do script "cd /Users/matthewpozsgai/Documents/GitHub/APlusOcean/Items;docker-compose exec items_service python ./items_service/winning_bid_in_cart_task.py"'


