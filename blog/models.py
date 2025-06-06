from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Person(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name= models.CharField(max_length=100)
    age=models.IntegerField()
    email=models.EmailField(max_length=100)
    phone_number=models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name}"