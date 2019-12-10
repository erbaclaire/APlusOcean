"""carts_service URL Configuration

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
    path('all_carts/', views.all_carts, name="all_carts"),
    path('get_cart/', views.get_cart, name="get_cart"),
    path('add_item_to_cart/', views.add_item_to_cart, name="add_item_to_cart"),
    path('log_transaction/', views.log_transaction, name="log_transaction"),
    path('get_cart_item/', views.get_cart_item, name="get_cart_item"),
    path('remove_bids_on_item_in_cart/', views.remove_bids_on_item_in_cart, name="remove_bids_on_item_in_cart")
]
