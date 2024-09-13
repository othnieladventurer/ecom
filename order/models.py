from django.db import models
from django.contrib.auth.models import User
from product.models import *

from django.utils import timezone
from decimal import Decimal


# Create your models here.



class Order(models.Model):
    ORDERED = 'ordered'
    SHIPPED = 'shipped'

    STATUS_CHOICES = (
        (ORDERED, 'ordered'),
        (SHIPPED, 'shipped')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=100)
    place = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    date_created = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)



    def __str__(self):
        return f"{self.first_name}   {self.last_name}  {self.paid_amount}"
    


    class Meta:
        ordering= ('-date_created',)

        

    def get_total_price(self):
        if self.paid_amount:
            return self.paid_amount 
        
        return Decimal('0.00')






class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.order}$ / Product price: {self.product.price}$  {self.product.title} "

    def get_total_price(self):
        return Decimal(self.product.price) * self.quantity  # Convert cents to dollars and multiply by quantity

