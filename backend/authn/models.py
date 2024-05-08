from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_img = models.FileField(upload_to='profile_images', null=True, blank=True)
    
    COOKING_SKILL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    
    cooking_skill_lvl = models.CharField(max_length=15, choices=COOKING_SKILL_CHOICES, blank=True, null=True)