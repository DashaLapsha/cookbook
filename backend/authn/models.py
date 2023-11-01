from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    dietary_pref = models.CharField(max_length=255, blank=True, null=True)
    
    COOKING_SKILL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    
    cooking_skill_lvl = models.CharField(max_length=15, choices=COOKING_SKILL_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"Username: {self.username}, Email: {self.email}, Dietary Preferences: {self.dietary_pref}, Cooking Skill Level: {self.cooking_skill_lvl}"
