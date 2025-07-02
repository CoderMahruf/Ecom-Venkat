from django.db import models
from apps.authentication.models import User
from apps.product.models import Product
from apps.discount.models import Coupon
from decimal import Decimal
from django.db.models import Sum
# Create your models here.
 
class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart')
    coupon = models.ForeignKey(Coupon,null=True,blank=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.first_name} {self.user.last_name}"

    # Calculates and returns the total price of all items in the cart
    def get_total_price(self):
        item_total = 0
        for item in self.items.all():
            item_price = item.get_total_price()
            item_total += item_price
        return item_total
    
    # Loops through all cart items and adds up their offer prices
    def get_total_offer_price(self):
        total = 0
        all_items = self.items.all()
        for item in all_items:
            item_offer_price = item.get_total_offer_price()
            total += item_offer_price
        return total
    
    # This function calculates the discount amount based on coupon percentage and max discount limit
    def get_discount(self):
        if self.coupon:
            # Calculate the discount using the total price and the coupon's discount percentage
            total_price = Decimal(self.get_total_price())
            discount_percent = Decimal(self.coupon.discount_percentage)
            discount_amount = total_price * discount_percent / 100
            # Return the smaller value between calculated discount and the maximum allowed discount
            return min(discount_amount, self.coupon.maximum_discount)
        # If no coupon, return 0 as discount
        return Decimal('0.00')
    
    # Calculate the final price after subtracting the discount from the total price
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
    
    def get_total_item_count(self):
        # Calculate the total quantity of all items in this object
        total_quantity = self.items.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        if total_quantity is None:
            return 0
        return total_quantity



class CartItems(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10,blank=True,null=True)

    def __str__(self):
        return f"{self.cart.user.first_name} {self.cart.user.last_name}'s Cart Item: {self.product.title} x {self.quantity}"

    def get_total_price(self):
        return self.product.price * self.quantity

    # def get_total_offer_price(self):
    #     return self.product.offer_price * self.quantity
    