 # APlusOcean

 ### How to Run the Application
First delete all existing containers and aplusocean images:
- `docker rm -vf $(docker ps -a -q)`
- `docker rmi -f $(docker images | grep ^"aplusocean" | awk "{print $3}")`

To run the micorservices in docker:
- ```docker-compose build```
- ```docker-compose up```

Next fix the rabbit connections:
- ``` docker exec -it aplusocean_rabbitmq_1 /bin/bash ```
- Then in the rabbitMQ root:``` apt-get update ```
- Then in the rabbitMQ root:``` apt-get install net-tools ```
- Then in the rabbitMQ root:``` ifconfig ```
- Take the host output (something like '172.17.0.3') and put it the config.py file in each of the services AND the Frontend

- Note: if you get errors trying to run the rabbitMQ container, it is likely because you already have a rabbitMQ container bound to that port from the labs.  Remove your old container and try again and it should resolve.


In a separate terminal then do the following to update databases:
- ```docker-compose exec items_service python manage.py makemigrations items_service```
- ```docker-compose exec items_service python manage.py migrate```
- ```docker-compose exec notifications_service python manage.py makemigrations notification_service```
- ```docker-compose exec notifications_service python manage.py migrate```
- ```docker-compose exec carts_service python manage.py makemigrations carts_service```
- ```docker-compose exec carts_service python manage.py migrate```
- ```docker-compose exec accounts_service python manage.py makemigrations accounts_service```
- ```docker-compose exec accounts_service python manage.py migrate```
- ```docker-compose exec auctions_service python manage.py makemigrations auctions_service```
- ```docker-compose exec auctions_service python manage.py migrate```

Run the following tasks in different terminals
- ```docker-compose exec items_service python ./items_service/auction_timer_task.py```
- ```docker-compose exec items_service python ./items_service/rpc_task.py```
- ```docker-compose exec accounts_service python ./accounts_service/watchlist_task.py```
- ```docker-compose exec notifications_service python ./notification_service/notifications_task.py```
- ```docker-compose exec auctions_service python ./auctions_service/auction_over_task.py```
- ```docker-compose exec auctions_service python ./auctions_service/auction_ending_warning_task.py```
- ```docker-compose exec auctions_service python ./auctions_service/place_bid_task.py```
- ```docker-compose exec auctions_service python ./auctions_service/remove_bids_task.py```
- ```docker-compose exec carts_service python ./carts_service/add_to_cart_task.py```
- ```docker-compose exec items_service python ./items_service/winning_bid_in_cart_task.py```
- ```docker-compose exec carts_service python ./carts_service/automatic_checkout_tasks.py```

Run the frontend locally:
- cd to ```Frontend/frontend```
- do ```pip3 install -r requirements.txt```
- ```python3 manage.py runserver```

 ## Notes for Graders:
 - The auctions ending soonest are automatically sorted on the admin page
 - Searching terms is case sensitive. If the item name includes the search term then you will get results.
 - We decided that a user cannot be deleted, blocked, or suspended if they have active auctions, bids, or items in their carts.
 - We are not providing fake items data to start with because the bulk of the site functionality is demonstrated at auction start and end times, and we don't know when the graders will be testing. To test this site, you can simply follow the instructions above to get the site running, and sign up as a user.  You can then post items to auctions starting whenever you want to test the features.  You can create more than one account and log in in separate windows to test bidding. In the AddingInitialFakeData.md file in this directory you can find steps on how to add the initial fake data we did to the databases.
 - Please note that the notificaiton service uses a Mail API, and will send actual emails to the login email you use, so please only test with your own email address or one of our team's email addresses.
- We did not get the docker compose setup with RabbitMQ, so you still have to change each of the config files manually (unfortunately)
- We did manual testing instead of a test suite and unit testing to make it easier to test the integrated functionality. 

## Sources:
 - https://www.rabbitmq.com/tutorials/tutorial-one-python.html
 - https://docs.docker.com/reference/
 - https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_countdown
 - https://stackoverflow.com/questions/17594298/date-time-formats-in-python/17594571
 - https://stackoverflow.com/questions/24403817/html5-required-attribute-one-of-two-fields
 - https://www.w3schools.com/howto/howto_js_countdown.asp
 - All frontend html/css uses Bootstrap templates (https://getbootstrap.com/)
