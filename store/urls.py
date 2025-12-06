from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="products"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("scan/", views.scan_barcode, name="scan_barcode"),
    path("cart/update/", views.update_cart, name="update_cart"),
    path("inventory/", views.inventory, name="inventory"),
    path("inventory/add/", views.add_product, name="add_product"),
    path("inventory/remove/<int:product_id>/", views.remove_product, name="remove_product"),
]
