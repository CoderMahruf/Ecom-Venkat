from django.urls import path
from .views import WishlistView,WishlistCreateView

urlpatterns = [
    path('wishlist/',WishlistView.as_view(),name="wishlist"),
    path('wishlist/create/<int:product_id>/',WishlistCreateView.as_view(),name="wishlist-create-delete")
]
