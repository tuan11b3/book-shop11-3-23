from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.

class myUser(AbstractUser):
    email = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
