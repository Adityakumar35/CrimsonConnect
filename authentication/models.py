from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default="https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg", upload_to='profile_pics/', null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.CharField(max_length=6, null=True, blank=True)
    country = models.CharField(max_length=15, null=True, blank=True)
    education = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=10, null=True, blank=True)  

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    request_id = models.AutoField(primary_key=True) 
    requested_blood = models.CharField(max_length=3, null=True, blank=True)
    recipient_fname = models.CharField(max_length=15)
    recipient_pincode = models.CharField(max_length=6)
    recipient_age = models.IntegerField()
    relation_with = models.CharField(max_length=10)  
    recipient_address = models.CharField(max_length=50)
    recipient_state = models.CharField(max_length=10, null=True, blank=True)

class Notification(models.Model):
    donor_user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_id = models.ForeignKey(Request, on_delete=models.CASCADE)