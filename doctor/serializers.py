from rest_framework import serializers
from . models import  Department,Doctors
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


class SlotSerializers(serializers.ModelSerializer):
     doctor = UserSerializer()
     class Meta:
          model = Slots
          fields = "__all__"


class  PostSlotSerializers(serializers.ModelSerializer):
     class Meta:
          model = Slots
          fields = "__all__"



class Appointmentserializer(serializers.ModelSerializer):
     patient = UserSerializer()
     doctor = DoctorsSerializers()
     slot = SlotSerializers()
     class Meta:
          model = Appointment
          fields = '__all__'