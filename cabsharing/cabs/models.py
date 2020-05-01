from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator


Gchoice=(
    ('M',"M"),
    ('F',"F")
)

class Post(models.Model):
    passengers=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(3)])
    date=models.DateField()
    time=models.TimeField()
    destination=models.CharField(max_length=100)
    author=models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=Gchoice, default='M')
    booked = models.BooleanField(default=False)
    pickup_from=models.CharField(max_length=100)


class Feedback(models.Model):
    customer_name = models.CharField(max_length=120)
    email = models.EmailField()
    details = models.TextField()
    date = models.DateField(auto_now_add=True)


class Frequest(models.Model):
    by=models.CharField(max_length=100)
    to=models.CharField(max_length=100)
    accepted=models.BooleanField(default=False)
    booking_id=models.IntegerField(default=0)


class Fgroup2(models.Model):
    created_by1 = models.CharField(max_length=100,default=None)
    passengers1 = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
    time1 = models.TimeField()
    gender1 = models.CharField(max_length=1, choices=Gchoice, default='M')
    pickup_from1 = models.CharField(max_length=100)
    created_by2 = models.CharField(max_length=100,default=None)
    passengers2 = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
    time2 = models.TimeField()
    gender2 = models.CharField(max_length=1, choices=Gchoice, default='M')
    pickup_from2 = models.CharField(max_length=100)
    date = models.DateField()
    destination = models.CharField(max_length=100)
    total_passengers = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)],default=None)