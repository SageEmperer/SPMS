from django.urls import path
from django.contrib import admin
from .import views
urlpatterns = [
    path('', views.login_page, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('category/', views.category, name="category"),
    path('vehicle_entry/', views.vehicle_entry, name="vehicle_entry"),
    path('manage_vehicles/', views.manage_vehicles, name="manage_vehicles"),
    path('search_data/', views.search_data, name="search_data"),
    path('account/', views.account, name="account"),
    path('logout/', views.logout_user, name="logout"),
    path('add_category/', views.add_category, name="add_category"),
    path('add_vehicle/', views.add_vehicle_form, name="add_vehicle"),
    path('edit_category/', views.edit_category, name="edit_category"),
    path('delete_category/<int:id>', views.delete_category, name="delete_category"),
    path('deactivate_category/<int:id>',
         views.deactivate_category, name="deactivate_category"),
    path('activate_category/<int:id>',
         views.activate_category, name="activate_category"),
    path('change_status_manage_vehicle/<int:id>',
         views.change_status_manage_vehicle, name="change_status_manage_vehicle"),
    path('change_password/', views.change_password, name="change_password"),
]
