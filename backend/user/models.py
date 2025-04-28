from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(max_length=10, choices=[(
        'admin', 'Admin'), ('user', 'User'), ('business_owner', 'Business Owner')], default='user')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Location fields
    location = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

    # Profile fields
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)
    links = models.JSONField(blank=True, null=True)


    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.email
