from django.urls import path
from .views import BannerView,CategoryView,ProductView, ProductCreateView,ProductDetailView

urlpatterns = [
    path('banner/',BannerView.as_view()),   
    path('categories/',CategoryView.as_view()),   
    path('product/',ProductView.as_view()),
    path('product/create/', ProductCreateView.as_view()),
    path('product/detail/<int:product_id>/',ProductDetailView.as_view())
]
