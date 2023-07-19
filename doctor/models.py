from django.db import models
from user.models import User

class Department(models.Model):
    name = models.CharField(max_length=50)
    description  = models.CharField(max_length=350)
    image = models.ImageField(upload_to='department/', null=True,)


    def __str__(self):
        return self.name

 

class Doctors(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    experience = models.PositiveIntegerField()
    fee = models.DecimalField(max_digits=8, decimal_places=2)
    certificate = models.FileField(upload_to='certificates/',null=True,blank=True)
    is_approved = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name


class Slots(models.Model):
    doctor = models. ForeignKey(User,on_delete=models.CASCADE ,limit_choices_to={'is_active':True,'is_staff':True,'is_superadmin':False} )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.BooleanField(default=True)
    slot_duration  = models.IntegerField()
    is_booked = models.BooleanField(default=False)
    

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_active': True, 'is_staff': False, 'is_superadmin': False})
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, limit_choices_to={'user__is_staff': True})
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('rejected','Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    slot = models.ForeignKey(Slots, on_delete=models.CASCADE)
    appointment_payment_id = models.CharField(max_length=100,null= True)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)


class Prescription(models.Model):
    doctor = models.ForeignKey(Doctors,on_delete=models.CASCADE)
    patient = models.ForeignKey(User,on_delete=models.CASCADE)
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    instructions = models.TextField()
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.patient.first_name
 
     