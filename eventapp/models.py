from django.db import models
from django.utils.timezone import now


class Login(models.Model):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=20)
    user_type = models.CharField(max_length=20)

    def __str__(self):
        return self.email


class User(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.firstname


class Vendor(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    image = models.ImageField(upload_to='vendors/', null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return self.business_name


class Service(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    service_category = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='services/', null=True, blank=True)

    def __str__(self):
        return f"{self.vendor.business_name} - {self.service_category}"
