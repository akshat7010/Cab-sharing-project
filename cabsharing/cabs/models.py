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
