from django.shortcuts import render
from user . models import User
from user . serializers import UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import  DepartmentSerializers,PostDoctorSerializers,DoctorsSerializers 
from . models import Department,Doctors 
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
 


class DoctorsCreateAPIView(APIView):
    def post(self, request,format =None):
        data = request.data
        user = data['user']

        current_user = User.objects.get(id=user)

        doctor = PostDoctorSerializers(data=request.data)
        if doctor.is_valid():
            doctor.save()

            
            # Send email notification to admin
            subject = 'Doctor Approval Request'
            message = f'A new doctor ({current_user}) has been registered and requires approval.'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = 'shadi@gmail.com'  

            send_mail(subject, message, from_email, [to_email])
            return Response( status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST) 

class DepartmentListView(APIView):
    
    def get(self,request):
        departments = Department.objects.all()
        serializer_class = DepartmentSerializers(departments,many =True)
        print(departments)
        return Response(serializer_class.data)  

@api_view(['POST'])
def createDepartment(request):
    serializer = DepartmentSerializers(data=request.data)
    print(serializer,'gshiguiuhsuidh')
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)  

class HomeListDoctor(APIView):
    def get(self, request):
        queryset = Doctors.objects.all()
        serializer=DoctorsSerializers(queryset, many=True)
        return Response(serializer.data)

class HomeListDepartment(APIView):
    def get(self, request):
        queryset = Department.objects.all()
        serializer=DepartmentSerializers(queryset, many=True)
        return Response(serializer.data)
    
            