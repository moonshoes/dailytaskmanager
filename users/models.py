from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    birthdate = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return f'{self.user.username} Profile'