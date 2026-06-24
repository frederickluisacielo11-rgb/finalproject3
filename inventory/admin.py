from django.contrib import admin 
from inventory.models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_per_page = 15

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'name', 'category', 'brand', 'price', 'quantity', 'display_stock_status', 'created_at']
    search_fields = ['name', 'brand', 'description']
    list_filter = ['category', 'brand']
    list_editable = ['price', 'quantity']
    list_per_page = 15

    @admin.display(description='Stock Status')
    def display_stock_status(self, obj):
        return obj.get_stock_status()