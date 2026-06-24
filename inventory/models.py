from django.db import models


class Category(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    

class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)   
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name
    
    def in_stock(self):
        return self.quantity > 0

    def get_stock_status(self):
        if self.quantity == 0:
            return 'Out of stock'
        elif self.quantity < 5:
            return 'Critical'
        elif self.quantity < 10:
            return 'Low stock'
        else:
            return 'In stock'
            
    def get_stock_color(self):
        if self.quantity == 0:
            return 'pill-red'
        elif self.quantity < 5:
            return 'pill-red'
        elif self.quantity < 10:
            return 'pill-amber'
        else:
            return 'pill-green'
