from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .models import Category, Add_vehicle
from django.core.paginator import Paginator
from django.db.models import Sum


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'login.html')


@login_required
def dashboard(request):
    parked_vehicle_count = Add_vehicle.objects.count()
    leaved_vehicle_count = Add_vehicle.objects.count()
    parking_charge_sum = Add_vehicle.objects.aggregate(
        Sum('parking_charge'))['parking_charge__sum'] or 0
    vehicle_count = Add_vehicle.objects.all().count()
    category_data_available = Category.objects.all().count()
    category_data = Category.objects.all()
    vehicle_data = Add_vehicle.objects.all()
    # calculating the parking slot available
#    vehicle_limit
    total_vehicle_limit = sum(int(category.vehicle_limit)
                              for category in category_data)
    total_vehicle_limit = total_vehicle_limit-parked_vehicle_count

    context = {
        "category": category_data,
        "vehicle": vehicle_data,
        "parked_vehicle_count": parked_vehicle_count,
        "leaved_vehicle_count": leaved_vehicle_count,
        "category_data_available": category_data_available,
        "parking_charge_sum": parking_charge_sum,
        "vehicle_count": vehicle_count,
        "total_vehicle_limit": total_vehicle_limit,


    }
    return render(request, 'dashboard.html', context)


@login_required
def category(request):
    # filtering the data from the search
    search_query = request.GET.get('search')
    if search_query:
        category_data = Category.objects.filter(
            parking_area_no__icontains=search_query)
    else:
        category_data = Category.objects.all()

    paginator = Paginator(category_data, 4)
    page_number = request.GET.get('page')
    Category_data_final = paginator.get_page(page_number)
    Category_all = Category.objects.all()
    context = {
        'category_data': Category_data_final,
        "category_all": Category_all
    }
    return render(request, 'category.html', context)


@login_required
def vehicle_entry(request):
    vehicle_data_all = Add_vehicle.objects.all()
    category = Category.objects.all()
    # filtering the data from the search
    search_query = request.GET.get('search')
    if search_query:
        vehicle_data = Add_vehicle.objects.filter(
            vehicle_no__icontains=search_query)
    else:
        vehicle_data = Add_vehicle.objects.all()

    paginator = Paginator(vehicle_data, 4)
    page_number = request.GET.get('page')
    vehicle_data_final = paginator.get_page(page_number)
    context = {
        'vehicle_data': vehicle_data_final,
        'category': category,
        "vehicles": vehicle_data_all
    }
    return render(request, 'vehicle-entry.html', context)


@login_required
def manage_vehicles(request):
    # filtering the data from the search
    search_query = request.GET.get('search')
    if search_query:
        vehicle_data = Add_vehicle.objects.filter(
            vehicle_no__icontains=search_query)
    else:
        vehicle_data = Add_vehicle.objects.all()

    paginator = Paginator(vehicle_data, 5)
    page_number = request.GET.get('page')
    vehicle_data_final = paginator.get_page(page_number)
    context = {
        "vehicle_data": vehicle_data_final
    }
    return render(request, 'manage-vehicles.html', context)


@login_required
def search_data(request):
    search_query = request.GET.get('search')
    vehicle_data = Add_vehicle.objects.all()
    if search_query:
        vehicle_data = vehicle_data.filter(
            vehicle_no__icontains=search_query
        )
    paginator = Paginator(vehicle_data, 5)
    page_number = request.GET.get('page')
    vehicle_data_final = paginator.get_page(page_number)
    context = {

        "vehicle_data": vehicle_data_final
    }
    return render(request, 'search-data.html', context)
# changeing the status of the vehicle in the search


@login_required
def change_status_manage_vehicle(request, id):
    vehicle = Add_vehicle.objects.get(id=id)
    if vehicle.status:
        vehicle.status = False
    else:
        vehicle.status = True
    vehicle.save()
    return redirect('manage_vehicles')


@login_required
def account(request):
    return render(request, 'account.html')


# logout
@login_required
def logout_user(request):
    logout(request)
    return render(request, 'login.html')

# adding category form


@login_required
def add_category(request):
    if request.method == "POST":
        parking_area_number = request.POST.get('parkingAreaNumber')
        vehicle_type = request.POST.get('vehicleType')
        vehicle_limit = request.POST.get('vehicleLimit')
        parking_charge = request.POST.get('parkingCharge')

        Category.objects.create(
            parking_area_no=parking_area_number,
            vehicle_type=vehicle_type,
            vehicle_limit=vehicle_limit,
            parking_charge=parking_charge
        )

        return redirect('category')

    return redirect('category')

# add vehicle form


@login_required
def add_vehicle_form(request):
    if request.method == "POST":
        vehicle_number = request.POST.get('vehicleNumber')
        vehicleType = request.POST.get('vehicleType')
        parkingAreaNumber = request.POST.get('parkingAreaNumber')
        parkingCharge = request.POST.get('parkingCharge')
        try:
            # Convert the parking_area_id to a Category instance
            category_instance = Category.objects.get(pk=parkingAreaNumber)
        except Category.DoesNotExist:
            # Handle the case where the specified Category does not exist
            # You may want to add appropriate error handling here
            return redirect('error_page')

        Add_vehicle.objects.create(

            vehicle_no=vehicle_number,
            parking_area_no=category_instance,
            vehicle_type=vehicleType,
            parking_charge=parkingCharge,
        )
        redirect('vehicle_entry')
    return redirect('vehicle_entry')

# edit category


@login_required
def edit_category(request):
    if request.method == "POST":
        category = Category.objects.get(id=request.POST.get('id'))
        category.parking_area_no = request.POST.get('parkingAreaNumber')
        category.vehicle_type = request.POST.get('vehicleType')
        category.vehicle_limit = request.POST.get('vehicleLimit')
        category.parking_charge = request.POST.get('parkingCharge')
        category.save()
        return redirect('category')
# deleting an category


@login_required
def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('category')

# deactivating the category


@login_required
def deactivate_category(request, id):
    category = Category.objects.get(id=id)
    category.status = False
    category.save()
    return redirect('category')
# activating the category


@login_required
def activate_category(request, id):
    category = Category.objects.get(id=id)
    category.status = True
    category.save()
    return redirect('category')


# password change
@login_required
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        re_entered_password = request.POST.get('rePassword')
        # validating the form

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is not correct')
            return redirect('change_password')
        if new_password != re_entered_password:
            messages.error(
                request, 'New password and re-entered password do not match')
            return redirect('change_password')

        if new_password == current_password:
            messages.error(
                request, 'New password cannot be same as current password')
            return redirect('change_password')
        request.user.set_password(new_password)
        request.user.save()
        login(request, request.user)
        messages.success(request, 'Password changed successfully')
        return render(request, 'account.html')

    return render(request, 'account.html')
