from django.shortcuts import render, redirect
from django.contrib.auth.models import *
from django.contrib import auth, messages
from django.conf import settings
from .models import *


def index(request):
    return render(request, 'index.html')


def logout(request):
    request.session.flush()
    return redirect('login')


def vendors(request):
    services = Service.objects.select_related('vendor').filter(vendor__status='approved')
    return render(request, 'vendors.html', {'services': services})


def contact(request):
    return render(request, 'contact.html')


def admin_home(request):
    total_users = User.objects.count()
    total_vendors = Vendor.objects.count()
    vendors = Vendor.objects.all()
    return render(request, 'admin_home.html', {
        'total_users': total_users,
        'total_vendors': total_vendors,
        'vendors': vendors,
    })


def approve_vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    vendor.status = 'approved'
    vendor.save()
    return redirect('admin_vendor_view')


def reject_vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    vendor.status = 'rejected'
    vendor.save()
    return redirect('admin_vendor_view')


def admin_user_view(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'admin_user_view.html', {'users': users})


def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('admin_user_view')


def admin_vendor_view(request):
    vendors = Vendor.objects.all().order_by('-id')
    return render(request, 'admin_vendor_view.html', {'vendors': vendors})


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = Login.objects.filter(email=email, password=password).first()

        if user:
            request.session['lid'] = user.id

            if user.user_type == 'admin':
                return redirect('admin_home')

            elif user.user_type == 'vendor':
                vendor = Vendor.objects.filter(email=email).first()
                if vendor:
                    request.session['vendor_id'] = vendor.id
                    return redirect('vendor_index')
                else:
                    messages.error(request, "Vendor profile not found.")
                    return redirect('login')

            elif user.user_type == 'user':
                return redirect('index')

        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'login.html')


def user_register(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        login_obj = Login.objects.create(
            email=email,
            password=password,
            user_type='user'
        )

        User.objects.create(
            LOGIN=login_obj,
            username=request.POST['username'],
            firstname=request.POST['firstname'],
            lastname=request.POST['lastname'],
            phone=request.POST['phone'],
            created_at=now()
        )
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')
    return render(request, 'user_register.html')


def profile(request):
    login_id = request.session.get('lid')
    if not login_id:
        return redirect('login')
    user = User.objects.filter(LOGIN_id=login_id).first()
    if not user:
        return redirect('login')
    return render(request, 'profile.html', {'user': user})


def vendor_index(request):
    vendor_id = request.session.get('vendor_id')
    if not vendor_id:
        return redirect('login')
    vendor = Vendor.objects.filter(id=vendor_id).first()
    if not vendor:
        return redirect('login')
    services = Service.objects.filter(vendor=vendor)
    return render(request, 'vendor_index.html', {'services': services, 'vendor': vendor})


def vendor_register(request):
    if request.method == "POST":
        business_name = request.POST.get('business_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        image = request.FILES.get('image')
        password = request.POST.get('password')

        if Login.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('vendor_register')

        login_obj = Login.objects.create(
            email=email,
            password=password,
            user_type='vendor'
        )

        Vendor.objects.create(
            LOGIN=login_obj,
            business_name=business_name,
            phone=phone,
            email=email,
            address=address,
            image=image,
            status='pending'
        )

        messages.success(request, "Vendor registered! Waiting for admin approval.")
        return redirect('login')

    return render(request, 'vendor_register.html')


def service_add(request):
    vendor_id = request.session.get('vendor_id')
    if not vendor_id:
        return redirect('login')

    vendor = Vendor.objects.filter(id=vendor_id).first()
    if not vendor:
        return redirect('login')

    if vendor.status != 'approved':
        messages.error(request, "Admin approval required before adding services!")
        return redirect('vendor_index')

    if request.method == "POST":
        category = request.POST.get('service_category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Service.objects.create(
            vendor=vendor,
            service_category=category,
            price=price,
            description=description,
            image=image,
        )

        messages.success(request, "Service added successfully!")
        return redirect('vendor_index')

    return render(request, 'service_add.html')
