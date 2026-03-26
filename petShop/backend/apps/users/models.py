from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    THEME_CHOICES = [('light', 'Light'), ('dark', 'Dark')]