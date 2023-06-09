from rest_framework import serializers
from . models import  Department,Doctors
from user. serializers import UserSerializer




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