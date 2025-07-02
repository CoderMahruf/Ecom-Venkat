from django.contrib import admin
from .models import Coupon

# Customize how the Coupon model appears in the Django admin
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'valid_from', 'valid_until', 'maximum_discount', 'minimum_spend')  
    list_filter = ('valid_from', 'valid_until') 
    search_fields = ('code',)  
