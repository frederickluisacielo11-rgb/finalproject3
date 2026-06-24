from django.contrib import admin
from orders.models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'users', 'product', 'quantity', 'total_price', 'status', 'created_at']
    search_fields = ['users__full_name', 'users__username', 'users__email', 'product__name', 'product__brand', 'status']
    list_filter = ['status']
    list_per_page = 15
