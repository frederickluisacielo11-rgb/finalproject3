from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from .models import Users


def user_list(request):
    search = request.GET.get('search', '')
    if search:
        users = Users.objects.filter(
            Q(full_name__icontains=search) |
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(address__icontains=search) |
            Q(contact__icontains=search) |
            Q(gender__icontains=search) |
            Q(role__icontains=search)
        )
    else:
        users = Users.objects.all()

    paginator = Paginator(users, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'users/user_list.html',{
            'page_obj': page_obj,
            'search': search,
            'total_results': (users.count())
        }
    )


def user_create(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name','').strip()
        username = request.POST.get('username','').strip()
        password = request.POST.get('password','')
        confirm = request.POST.get('confirm_password','')
        email = request.POST.get('email','').strip()
        gender = request.POST.get('gender','')
        role = request.POST.get('role','')
        birthdate = request.POST.get('birthdate','').strip()
        address = request.POST.get('address','').strip()
        contact = request.POST.get('contact','').strip()

        if not all([full_name, username, password, confirm,
            email, gender, role, birthdate, address,contact]):
            messages.error(request, 'All fields are required!')
            return render(request, 'users/user_form.html', {'form_data': request.POST})

        if password != confirm:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'users/user_form.html',{'form_data': request.POST})

        if Users.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'users/user_form.html', {'form_data': request.POST})

        if Users.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return render(request, 'users/user_form.html', {'form_data': request.POST})

        user = Users(
            full_name=full_name,
            username=username,
            password=make_password(password),
            email=email,
            gender=gender,
            role=role,
            birthdate=birthdate,
            address=address,
            contact=contact,
        )
        if request.FILES.get('profile_picture'):
            user.profile_picture = (request.FILES['profile_picture'])
        user.save()
        messages.success(request, f'{full_name} added successfully!')
        return redirect('user_list')

    return render(request, 'users/user_form.html')



def user_update(request, pk):
    user = get_object_or_404(Users, pk=pk)

    if request.method == 'POST':
        full_name = request.POST.get('full_name','').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email','').strip()
        gender = request.POST.get('gender','')
        role = request.POST.get('role','')
        birthdate = request.POST.get('birthdate','').strip()
        address = request.POST.get('address','').strip()
        contact = request.POST.get('contact','').strip()

        if not all([full_name, username, email, gender, role, birthdate, address, contact]):
            messages.error(request, 'All fields are required!')
            return render(request, 'users/user_form.html',{'user': user,})

        if Users.objects.filter(username=username).exclude(pk=pk).exists():
            messages.error(request, 'Username already exists!')
            return render(request,'users/user_form.html', {'user': user,})

        if Users.objects.filter(email=email).exclude(pk=pk).exists():
            messages.error(request, 'Email already exists!')
            return render(request, 'users/user_form.html', {'user': user,})

        user.full_name = full_name
        user.username = username
        user.email = email
        user.gender = gender
        user.role = role
        user.birthdate = birthdate
        user.address = address
        user.contact = contact

        if request.FILES.get('profile_picture'):
            user.profile_picture = (request.FILES['profile_picture'])
        user.save()
        messages.success(request,f'{full_name} updated successfully!')
        return redirect('user_list')

    return render(request,'users/user_form.html',{'user': user})


def user_delete(request, pk):
    user = get_object_or_404(Users, pk=pk)

    if request.method == 'POST':
        if user.orders.exists():
            messages.error(
                request,
                f'Cannot delete! {user.full_name} has existing orders!'
            )
            return redirect('user_list')

        name = user.full_name
        user.delete()
        messages.success(request, f'{name} deleted successfully!')
        return redirect('user_list')

    return render(request, 'users/user_confirm_delete.html', {'user': user})