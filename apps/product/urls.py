from django.urls import path
from .views import BannerView,CategoryView,ProductView, ProductCreateView

urlpatterns = [
    path('banner/',BannerView.as_view()),   
    path('categories/',CategoryView.as_view()),   
    path('product/',ProductView.as_view()),
    path('product/create/', ProductCreateView.as_view())

]
