from django.db import models
from doctor.models import Slots

# Create your models here.
 

class Order(models.Model):
    order_product = models.CharField(max_length=100)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)
    slot = models.ForeignKey(Slots, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_product
