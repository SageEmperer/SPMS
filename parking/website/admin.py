from django.contrib import admin
from .models import Add_vehicle, Category
# Register your models here.


class AddVehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_no', 'parking_area_no',
                    'vehicle_type', 'status', 'arrival_time')
    list_filter = ('status',)
    search_fields = ('vehicle_no', 'parking_area_no', 'vehicle_type')
    ordering = ('arrival_time',)

admin.site.register(Add_vehicle, AddVehicleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('parking_area_no', 'vehicle_type',
                    'vehicle_limit', 'parking_charge', 'status', 'doc')
    list_filter = ('status',)
    search_fields = ('parking_area_no', 'vehicle_type')


admin.site.register(Category, CategoryAdmin)
