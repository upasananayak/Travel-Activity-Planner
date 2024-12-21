from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Email is a required field')
        
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email,password,**extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=200, unique=True)
    username = models.CharField(max_length=50, null=True, blank= True, unique=True)

    objects = CustomUserManager()
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

class Trip(models.Model):
    user = models.ForeignKey(
        # settings.AUTH_USER_MODEL, 
        CustomUser,
        on_delete=models.CASCADE, 
        related_name='trips'
    )
    starting_date = models.DateField()
    place = models.CharField(max_length=255)
    number_of_days = models.PositiveIntegerField()
    image_url = models.URLField(
        blank=True, 
        null=True, 
        default='https://www.travelturtle.world/wp-content/uploads/2024/03/6585d85934a171a9a052c170_traveling-based-on-fare-deals.jpeg'
    )

    
    def __str__(self):
        return f"{self.user.email} - {self.place} ({self.starting_date})"

from django.db import models

class Place(models.Model):
    trip = models.ForeignKey(
        Trip, 
        on_delete=models.CASCADE, 
        related_name='places'
    )
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    visited = models.BooleanField(default=False)
    image_url = models.URLField( 
        blank=True, 
        null=True, 
        default='https://www.travelturtle.world/wp-content/uploads/2024/03/6585d85934a171a9a052c170_traveling-based-on-fare-deals.jpeg'
    )
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name} (Order: {self.order}) - {self.trip}"
