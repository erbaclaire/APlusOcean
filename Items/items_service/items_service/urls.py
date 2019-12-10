"""items_service URL Configuration

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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('view_inventory/', views.view_inventory, name='view_inventory'),
    path('view_categories/', views.view_categories, name='view_categories'),
    path('add_item/', views.add_item, name='add_item'),
    path('get_item/', views.get_item, name='get_item'),
    path('seller_item_update/', views.seller_item_update, name='seller_item_update'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('flag_item/', views.flag_item, name='flag_item'),
    path('view_flagged_items/', views.view_flagged_items, name='view_flagged_items'),
    path('get_search_results/', views.get_search_results, name='get_search_results'),
    path('delete_category/', views.delete_category, name='delete_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('update_category/', views.update_category, name='update_category'),
    path('in_cart/', views.in_cart, name='in_cart'),
    path('stop_auction/', views.stop_auction, name='stop_auction'),
    path('item_sold/', views.item_sold, name='item_sold'),
    path('has_bids/', views.has_bids, name='has_bids'),
    path('place_bid/', views.place_bid, name='place_bid')

]
