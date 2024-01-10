from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Email(models.Model):
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.email
    

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

class Notification(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    status = models.CharField(max_length=100,default='unread', choices=(('read','read'),('unread','unread'))) 
    timestamp = models.DateTimeField(auto_now_add=True)   
    email = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications", default=1)                                                  

    def __str__(self):
        return self.title
    

class Profile(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name="profile")
    token = models.CharField(default='',max_length=1000)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.email)
    
    def save(self, *args, **kwargs):
        self.token = str(uuid.uuid4())
        super(Profile, self).save(*args, **kwargs)



