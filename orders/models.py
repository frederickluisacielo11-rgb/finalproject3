from django.db import models
from django.core.validators import MinValueValidator
from inventory.models import Product
from users.models import Users

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    order_id = models.BigAutoField(primary_key=True)
    users = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orders')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return (f'Order {self.order_id} - {self.users.full_name}' )

    def get_status_color(self):
        if self.status == 'completed':
            return 'pill-green'
        elif self.status == 'pending':
            return 'pill-amber'
        elif self.status == 'cancelled':
            return 'pill-red'
        return 'pill-blue'



