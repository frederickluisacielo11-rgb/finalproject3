from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import ProtectedError
from .models import Category, Product
from decimal import Decimal, InvalidOperation


def dashboard(request):
    total_categories = Category.objects.count()
    total_products = Product.objects.count()

    context = {
        'total_categories': total_categories,
        'total_products': total_products,
    }
    return render(request, 'dashboard/index.html', context)


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {'categories': categories})


def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')

        if not name:
            messages.error(request, 'Name is required.')
            return render(request, 'inventory/category_form.html', {
                'name': name, 'description': description
            })

        if Category.objects.filter(name=name).exists():
            messages.error(request, 'A category with this name already exists.')
            return render(request, 'inventory/category_form.html', {
                'name': name, 'description': description
            })
        
        Category.objects.create(name=name, description=description)
        messages.success(request, 'Category added successfully!')
        return redirect('category_list')

    return render(request, 'inventory/category_form.html')


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')

        if not name:
            messages.error(request, 'Name is required.')
            return render(request,'inventory/category_form.html',{'category': category})
        
        if Category.objects.filter(name=name).exclude(pk=pk).exists():
            messages.error(request, 'Category name already exists.')
            return render(request, 'inventory/category_form.html', {'category': category})
        
        category.name = name
        category.description = description
        category.save()

        messages.success(request, 'Category updated successfully!')
        return redirect('category_list')
    
    return render(request, 'inventory/category_form.html',{'category': category})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        try:
            category.delete()
            messages.success(request, 'Category deleted successfully!')
        except ProtectedError:
            messages.error(
                request,
                'Cannot delete! This category still has products assigned to it.'
            )
        return redirect('category_list')
    return render(request, 'inventory/category_confirm_delete.html', {'category': category})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})


def product_create(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        brand = request.POST.get('brand')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description', '')
        image = request.FILES.get('image')

        if quantity == '' or quantity is None:
            messages.error(request, 'Quantity is required.')
            return render(request, 'inventory/product_form.html', {
                'categories': categories
            })

        if not name or not category_id or not brand or not price:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'inventory/product_form.html', {'categories': categories})

        try:
            price = Decimal(price)
            if price <= 0:
                raise InvalidOperation
            quantity = int(quantity)
            if quantity < 0:
                raise ValueError
        except (ValueError, InvalidOperation):
            messages.error(request, 'Price must be a number and Quantity must be an integer!')
            return render(request, 'inventory/product_form.html', {
                'categories': categories
            })

        category = get_object_or_404(Category, pk=category_id)

        Product.objects.create(
            name=name,
            category=category,
            brand=brand,
            price=price,
            quantity=quantity,
            description=description,
            image=image
        )
        messages.success(request, 'Product added successfully!')
        return redirect('product_list')

    return render(request, 'inventory/product_form.html', {'categories': categories})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category_id = request.POST.get('category')
        brand = request.POST.get('brand', '').strip()
        price = request.POST.get('price', '').strip()
        quantity = request.POST.get('quantity', '').strip()
        description = request.POST.get('description', '')
        
        if quantity == '':
            messages.error(request, 'Quantity is required.')
            return render(request, 'inventory/product_form.html', {
            'product': product,'categories': categories
    })

        if not name or not category_id or not brand or not price:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'inventory/product_form.html', {
                'product': product, 'categories': categories
            })

        try:
            product.price = Decimal(price)
            if product.price <= 0:
                raise InvalidOperation
            product.quantity = int(quantity)
            if product.quantity < 0:
                raise ValueError
        except (ValueError, InvalidOperation):
            messages.error(request, 'Price must be a decimal and Quantity must be an integer!')
            return render(request, 'inventory/product_form.html', {
                'product': product, 'categories': categories
            })

        product.name = name
        product.brand = brand
        product.description = description
        product.category = get_object_or_404(Category, pk=category_id)
        
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('product_list')

    return render(request, 'inventory/product_form.html', {'product': product , 'categories': categories})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        try:
            product.delete()
            messages.success(request, 'Product deleted successfully!')
        except ProtectedError:
            messages.error(
                request,
                f'Cannot delete {product.name}! It has existing orders linked to it.'
            )
        return redirect('product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})