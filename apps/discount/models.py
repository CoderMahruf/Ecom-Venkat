from django.db import models
from django.utils import timezone

# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=50,unique=True)
    discount_percentage = models.PositiveIntegerField()
    valid_from = models.DateField()
    valid_until = models.DateField()
    maximum_discount = models.DecimalField(max_digits=10,decimal_places=2,default=10)
    minimum_spend = models.DecimalField(max_digits=10,decimal_places=2,default=500)

    def __str__(self):
        return self.code
    
    # Checks if the coupon is currently valid and the user's cart total meets the minimum spend requirement.
    def is_applicable(self, request):
        today = timezone.now().date()
        # Check if the coupon is currently valid (optional but important)
        if today < self.valid_from or today > self.valid_until:
            return False  # Coupon is expired or not yet active
        user = request.user
        if hasattr(user, 'cart'):  # If the user has a cart
            cart = user.cart
            total_spent = cart.get_total_offer_price()
        else:
            total_spent = 0  # No cart means total is 0
        # Check if the cart total is greater than or equal to the coupon's minimum spend
        if total_spent >= self.minimum_spend:
            return True
        else:
            return False

