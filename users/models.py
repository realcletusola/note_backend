from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

# custom user manager\
class CustomUserManager(BaseUserManager):
    # create user 
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email address is required"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password is None:
            raise ValueError(_("Password is required"))
        
        user.set_password(password)
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user 
    
    # create super user 
    def create_superuser(self, email, password, **extra_fields):

        user = self.model(
            email=email
        )
        user.is_superuser = True
        user.is_staff = True
        
        if password is None:
            raise ValueError(_("Password is required"))
        
        user.set_password(password)
        user.save()
        return user 
    
# user model 
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return self.email


