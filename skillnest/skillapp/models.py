from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    branch = models.CharField(max_length=50, blank=True)
    year = models.CharField(max_length=10, blank=True)
    year = models.CharField(max_length=10, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    points = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} Profile"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
