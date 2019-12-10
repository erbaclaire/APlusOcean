Steps to set up presentation
1. remove all aplusocean containers
2. remove all aplusocean images
3. docker-compose up --build
4. fix config files
5. make migrations and migrate each of the DBs
6. exec in to each aplusocean_<service>_service_1 container and run "python3 manage.py shell"
 - do "from <service>_service import <tables>
        - Items, Categories for items_service
        - Accounts, Watchlists for accounts_service
        - Bids for auctions_service
        - Carts, Transactions for carts_service
        - UserComplaints for notification_service
 - There shouldn't be any data in the DB after all the other steps but if there is do "<Table>.objects.all().delete()"
7. Add you and me as users through the frontend. My email is erbaclaire@gmail.com and address is 4850 S Drexel Blvd, Chicago, IL 60615. Just lmk what you make my password.
8. Assuming you add yourself first - In the Accounts database do "x = Accounts.objects.all()[0]" and then "x.is_admin = True" and then "x.save()". If you add yourself second do [1] instead of [0]
9. Go in to the Items database and add categories as "x = Categories(category="All")" and "x.save()". Do this for the three categories we decided on in the script. After you save the All category do "x.pk" to see what the id is -- it should be 1 but lmk if it is not.