from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Visibility(models.Model):
    mode = models.CharField(max_length=200)

    def __str__(self):
        return self.mode

class Cohort(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # null ->can be empty, blank-> In form also
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True) # everytime I change, time is updated
    created = models.DateTimeField(auto_now_add=True) # Only once the time is updated i.e when created
    visibility = models.ForeignKey(Visibility, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-updated', '-created'] # TO order the contents while displaying
    
    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

class Follow(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='follower')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='followed')
    


