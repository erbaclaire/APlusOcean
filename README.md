 # APlusOcean

## Description
APlusOcean is a web app that mirrors the functionality of E-Bay. Users can simulate posting items, selling items, checking out, rating items, bidding on auctions, and communicating with admins.

## Stack
There are 5 microservices - Accounts, Auctions, Carts, Items, and Notifications. Each microservice is launched in its own ubuntu Docker container. Each microservice (Docker container) has its own database. Accounts, Carts, Items, and Notifications use Postgres relational databases and Auctions has a MongoDB database for quick processing of bids. All microservices (Docker containers) have RabbitMQ spun to send Pub/Sub or Point-to-Point asynchronous communications between the microservices. Some tasks use synchronous RPC calls to block before other actions can occur. The Docker containers also have Django imported to interact with the frontend calls. 

## Lessons Learned
The project gave me a foundational understanding of microservices - how monolithic applications are unstable because if one element goes down then the entire app goes down. The microservice structure allows for compartmentalization of tasks so that if something fails the app as a whole can still partially function. Additionally, this allowes for partial deployments. This project was my first exposure to Docker, as well. I learned how Docker containers make it easy to put out new features quickly, they often save costs and time because of shared OS, and how they are lightweight and portable because they have only what the app component needs and nothing more. Finally, this app gave me exposure to asynchronous communication with RabbitMQ, where a service sends a message and that message gets put in to a queue and is addressed as soon as it can be but in the meantime the app continues to function. Previously I had only known about synchronous applications. 

Below is how to run the application. One notices that it is a very manual process to start up the application. Towards the end of this project we were on a time crunch so that we could only partially automate the startup process with a Docker compose file. The next step for this project, therefore, is to encapsulate the below commands in a Docker compose file and deploy the app to a web server.

## How to Run the Application
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
