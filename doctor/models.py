from django.db import models
from user.models import User

class Department(models.Model):
    name = models.CharField(max_length=50)
    description  = models.CharField(max_length=350)
    image = models.ImageField(upload_to='department/', null=True,)


    def __str__(self):
        return self.name

class Doctors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    experience = models.IntegerField()
    fee =  models.DecimalField(max_digits=8 ,decimal_places=2)
    certificate = models.ImageField(upload_to='certificates/', null=True,)
     