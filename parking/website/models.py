from django.db import models


class Category(models.Model):
    STATUS_CHOICES = [
        (True, 'Active'),
        (False, 'Inactive'),
    ]
    parking_area_no = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100)
    vehicle_limit = models.CharField(max_length=200)
    parking_charge = models.CharField(max_length=200)
    status = models.BooleanField(default=True, choices=STATUS_CHOICES)
    doc = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.parking_area_no} - {self.vehicle_type} ({self.get_status_display()})"


class Add_vehicle(models.Model):
    STATUS_CHOICES = [
        (True, 'Parked'),
        (False, 'Leaved'),
    ]
    vehicle_no = models.CharField(max_length=200)
    parking_area_no = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=200)
    parking_charge = models.CharField(max_length=200)
    status = models.BooleanField(default=True, choices=STATUS_CHOICES)
    arrival_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_no} - {self.vehicle_type} ({self.get_status_display()})"
