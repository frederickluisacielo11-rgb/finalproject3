from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    ROLE_CHOICES = [ 
        ('admin', 'Admin'),  
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user_id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=55)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='male')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    birthdate = models.DateField()
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['full_name']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    def __str__(self):
        return self.full_name