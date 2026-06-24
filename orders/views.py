from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, ProtectedError
from .models import Order
from inventory.models import Product
from users.models import Users


def order_list(request):
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')

    orders = Order.objects.select_related('users', 'product')

    if search:
        orders = orders.filter(
            Q(users__full_name__icontains=search) |
            Q(users__email__icontains=search) |
            Q(product__name__icontains=search) |
            Q(product__brand__icontains=search) |
            Q(status__icontains=search)
        )

    if status:
        orders = orders.filter(status=status)

    paginator = Paginator(orders, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'orders/order_list.html',
        {
            'page_obj': page_obj,
            'search': search,
            'status': status,
            'total_results': (orders.count())
        }
    )



def order_create(request):
    users = Users.objects.all()
    products = Product.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user')
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        status = request.POST.get('status')

        if not all([user_id, product_id, quantity, status]):
            messages.error(request, 'All fields are required!')
            return render(request, 'orders/order_form.html',{
                'users': users, 'products': products
            })

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messages.error(
                request,
                'Quantity must be a '
                'positive number!'
            )
            return render(
                request,
                'orders/order_form.html',
                {
                    'users': users,
                    'products': products
                }
            )

        product = get_object_or_404(
            Product, pk=product_id
        )

        if not product.in_stock():
            messages.error(request, f'{product.name} is out of stock!')
            return render(request, 'orders/order_form.html',{
                'users': users, 'products': products
            })

        if quantity > product.quantity:
            messages.error(
                request,
                f'Not enough stock! Only {product.quantity} units available.'
            )
            return render(
                request,
                'orders/order_form.html',
                {
                    'users': users,
                    'products': products
                }
            )

        total_price = quantity * product.price

        Order.objects.create(
            users_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price,
            status=status,
        )

        product.quantity -= quantity
        product.save()

        messages.success(
            request,
            'Order created successfully!'
        )
        return redirect('order_list')

    return render(
        request,
        'orders/order_form.html',
        {
            'users': users,
            'products': products
        }
    )



def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    users = Users.objects.all()
    products = Product.objects.all()

    if request.method == 'POST':
        status = request.POST.get('status')

        if not status:
            messages.error(
                request,
                'Status is required!'
            )
            return render(
                request,
                'orders/order_form.html',
                {
                    'order': order,
                    'users': users,
                    'products': products
                }
            )

        if status == 'cancelled' and \
            order.status != 'cancelled':
            product = order.product
            product.quantity += order.quantity
            product.save()
            messages.success(
                request,
                f'Order cancelled. {order.quantity} units returned to stock.'
            )
        else:
            messages.success(
                request,
                'Order updated successfully!'
            )

        order.status = status
        order.save()
        return redirect('order_list')

    return render(
        request,
        'orders/order_form.html',
        {
            'order': order,
            'users': users,
            'products': products
        }
    )



def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        if order.status != 'cancelled':
            product = order.product
            product.quantity += order.quantity
            product.save()

        order.delete()
        messages.success(
            request,
            'Order deleted successfully!'
        )
        return redirect('order_list')

    return render(
        request,
        'orders/order_confirm_delete.html',
        {'order': order}
    )