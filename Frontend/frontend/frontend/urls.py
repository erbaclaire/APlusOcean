"""frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from aplusocean.views import index_views as index_views
from aplusocean.views import support_views as support_views
from aplusocean.views import items_views as items_views
from aplusocean.views import account_views as account_views
from aplusocean.views import login_register_views as login_register_views
from aplusocean.views import auction_views as auction_views
from aplusocean.views import cart_views as cart_views
from aplusocean.views import account_views as account_views
from aplusocean.views import auction_views as auction_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_views.home, name='home'),
    path('error/', index_views.error, name='error'),
    path('login/', login_register_views.login, name='login'),
    path('register/', login_register_views.register, name='register'),
    path('support/', support_views.support, name='support'),
    path('support/admin/', support_views.admin_support, name='admin_support'),
    path('support/admin/response/', support_views.support_response, name='support_response'),
    path('accounts/', account_views.user_account, name='user_account'),
    path('items/', items_views.items, name='items'),
    path('items/updates/', items_views.update_items, name='update_items'),
    path('items/new/', items_views.new_items, name='new_items'),
    path('items/flag/', items_views.flag_item, name='flag_item'),
    path('search/results/', items_views.search_results, name='search_results'),
    path('admin/add_delete_update_category/', items_views.admin_add_delete_update_category, name='admin_delete_category'),
    path('auctions/details/', auction_views.auction_details, name='auction_details'),
    path('carts/', cart_views.cart, name='carts'),
    path('checkout/', cart_views.checkout, name='checkout'),
    path('buy_now/', cart_views.buy_now, name='buy_now'),
    path('accounts/updates/', account_views.update_account, name='update_account'),
    path('accounts/un_suspend/', account_views.un_suspend, name='un_suspend'),
    path('accounts/suspend/', account_views.suspend, name='suspend'),
    path('accounts/delete/', account_views.delete, name='delete'),
    path('accounts/watchlist_add/', account_views.watchlist_add, name='watchlist_add'),
    path('accounts/watchlist_remove/', account_views.watchlist_remove, name='watchlist_remove'),
    path('confirmations/', cart_views.order_confirmation, name='order_confirmation'),
    path('auctions/place_bid/', auction_views.place_bid, name='place_bid')
]
