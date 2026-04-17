from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
class CustomUser(AbstractUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('first_name').verbose_name = 'Имя'
        self._meta.get_field('last_name').verbose_name = 'Фамилия'
    avatar = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name="Аватар")
    address = models.CharField(max_length=255, blank=True, verbose_name="Адрес")
    hidden_fields = ['password', 'last_login', 'is_superuser', 'username', 'email', 'avatar', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions']
    

    def get_extra_fields(self):
        return {f"{f.name}": f for f in self._meta.get_fields() if f.name not in self.hidden_fields and hasattr(f, 'editable') and f.editable}