
from django.urls import path
from .views import UserCartView, AddCartItemView, DeleteCartItemView

urlpatterns = [
    path('cart/', UserCartView.as_view(), name='view-cart'),
    path('cart/items/add/', AddCartItemView.as_view(), name='add-cart-item'),
    path('cart/items/delete/<int:pk>/', DeleteCartItemView.as_view(), name='delete-cart-item'),
]