

osascript -e 'tell application "Terminal" to do script "cd /Users/matthewpozsgai/Documents/GitHub/APlusOcean;docker-compose exec items_service python manage.py makemigrations items_service;docker-compose exec items_service python manage.py migrate;docker-compose exec notifications_service python manage.py makemigrations notification_service;docker-compose exec notifications_service python manage.py migrate;docker-compose exec carts_service python manage.py makemigrations carts_service;docker-compose exec carts_service python manage.py migrate;docker-compose exec accounts_service python manage.py makemigrations accounts_service;docker-compose exec accounts_service python manage.py migrate"'

