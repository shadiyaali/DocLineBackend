from rest_framework import serializers
from . models import  Department,Doctors,Prescription
from user. serializers import UserSerializer
from . models import Slots,Department,Doctors,Appointment




class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
       model = Department
       fields = '__all__'


class DoctorsSerializers(serializers.ModelSerializer):
    user = UserSerializer()
    department = DepartmentSerializers()
    class Meta:
       model = Doctors
       fields = '__all__'
 

class PostDoctorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = '__all__'


# serializers.py 
from .models import Slots

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slots
        fields = '__all__'


class PostSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slots
        exclude = ('is_booked',)  # Exclude the 'is_booked' field during creation


class AppointmentSerializer(serializers.ModelSerializer):
     patient = UserSerializer()
     doctor = DoctorsSerializers()
     slot = SlotSerializer()
     class Meta:
          model = Appointment
          fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    patient = UserSerializer()
    doctor = DoctorsSerializers()
    class Meta:
        model = Prescription
        fields = '__all__'

class  PostPrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'