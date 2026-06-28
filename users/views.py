
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Users
 
 
# ─────────────────────────────────────────────
# PUBLIC: Register (no login required)
# ─────────────────────────────────────────────
def register(request):
    if request.method == 'POST':
        full_name        = request.POST.get('full_name', '').strip()
        username         = request.POST.get('username', '').strip()
        email            = request.POST.get('email', '').strip()
        password         = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        gender           = request.POST.get('gender', '')
        role             = request.POST.get('role', '')
        birthdate        = request.POST.get('birthdate', '')
        address          = request.POST.get('address', '').strip()
        contact          = request.POST.get('contact', '').strip()
 
        context = {'form_data': request.POST}
 
        if not all([full_name, username, email, password, password_confirm,
                    gender, role, birthdate, address, contact]):
            messages.error(request, 'All required fields must be filled in.')
            return render(request, 'auth/register.html', context)
 
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/register.html', context)
 
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'auth/register.html', context)
 
        if Users.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'auth/register.html', context)
 
        if Users.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return render(request, 'auth/register.html', context)
 
        user = Users(
            full_name=full_name,
            username=username,
            email=email,
            gender=gender,
            role=role,
            birthdate=birthdate,
            address=address,
            contact=contact,
        )
        user.set_password(password)   # ← hashes correctly for Django auth
 
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']
 
        user.save()
        messages.success(request, f'Account created for {full_name}. You can now log in.')
        return redirect('login')
 
    return render(request, 'auth/register.html', {'form_data': {}})
 
 
# ─────────────────────────────────────────────
# PROTECTED: all views below require login
# ─────────────────────────────────────────────
@login_required
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
 
    return render(request, 'users/user_list.html', {
        'page_obj': page_obj,
        'search': search,
        'total_results': users.count(),
    })
 
 
@login_required
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
 
 
@login_required
def user_create(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        username  = request.POST.get('username', '').strip()
        email     = request.POST.get('email', '').strip()
        password  = request.POST.get('password', '')
        gender    = request.POST.get('gender', '')
        role      = request.POST.get('role', '')
        birthdate = request.POST.get('birthdate', '')
        address   = request.POST.get('address', '').strip()
        contact   = request.POST.get('contact', '').strip()
 
        context = {'user': None, 'form_data': request.POST}
 
        if Users.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'users/user_form.html', context)
 
        if Users.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return render(request, 'users/user_form.html', context)
 
        user = Users(
            full_name=full_name,
            username=username,
            email=email,
            gender=gender,
            role=role,
            birthdate=birthdate,
            address=address,
            contact=contact,
        )
        # FIX: use set_password so the hash is stored, not raw text
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
 
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']
 
        user.save()
        messages.success(request, f'{full_name} added successfully!')
        return redirect('user_list')
 
    return render(request, 'users/user_form.html', {
        'user': None,
        'form_data': {},
    })
 
 
@login_required
def user_update(request, pk):
    user = get_object_or_404(Users, pk=pk)
 
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        username  = request.POST.get('username', '').strip()
        email     = request.POST.get('email', '').strip()
        password  = request.POST.get('password', '')
        gender    = request.POST.get('gender', '')
        role      = request.POST.get('role', '')
        birthdate = request.POST.get('birthdate', '')
        address   = request.POST.get('address', '').strip()
        contact   = request.POST.get('contact', '').strip()
 
        context = {'user': user, 'form_data': request.POST}
 
        if not all([full_name, username, email, gender,
                    role, birthdate, address, contact]):
            messages.error(request, 'All fields are required!')
            return render(request, 'users/user_form.html', context)
 
        if Users.objects.filter(username=username).exclude(pk=pk).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'users/user_form.html', context)
 
        if Users.objects.filter(email=email).exclude(pk=pk).exists():
            messages.error(request, 'Email already exists!')
            return render(request, 'users/user_form.html', context)
 
        user.full_name = full_name
        user.username  = username
        user.email     = email
        user.gender    = gender
        user.role      = role
        user.birthdate = birthdate
        user.address   = address
        user.contact   = contact
 
        # Only update password if a new one was typed
        if password:
            user.set_password(password)
 
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']
 
        user.save()
        messages.success(request, f'{full_name} updated successfully!')
        return redirect('user_list')
 
    return render(request, 'users/user_form.html', {
        'user': user,
        'form_data': {},
    })
 