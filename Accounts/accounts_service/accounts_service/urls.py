"""accounts_service URL Configuration

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
    path('account_info/', views.account_info, name='account_info'),
    path('all_users/', views.all_users, name='all_users'),
    path('new_user/', views.new_user, name='new_user'),
    path('update_account/', views.update_account, name='update_account'),
    path('un_suspend_account/', views.un_suspend_account, name='un_suspend_account'),
    path('suspend_account/', views.suspend_account, name='suspend_account'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('block_user/', views.block_user, name='block_user'),
    path('un_block_user/', views.un_block_user, name='un_block_user'),
    path('add_watchlist_item/', views.add_watchlist_item, name='add_watchlist_item'),
    path('get_watchlist_items/', views.get_watchlist_items, name='get_watchlist_items'),
    path('watchlist_remove/', views.remove_watchlist_items, name='remove_watchlist_items'),
    path('rate_seller/', views.rate_seller, name='rate_seller')
]
