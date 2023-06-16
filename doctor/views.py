from django.shortcuts import render
from user . models import User
from user . serializers import UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import (Appointmentserializer,DepartmentSerializers,PostDoctorSerializers,SlotSerializers,
PostSlotSerializers,DoctorsSerializers)
from . models import Department,Doctors 
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .serializers import PostDoctorSerializers
from .models import Doctors
from . models import Doctors,Slots,Appointment
import datetime
 

 

class DoctorsCreateAPIView(APIView):
    def post(self, request, format=None):
        print(request.data)

        
        serializer = PostDoctorSerializers(data=request.data)
        if serializer.is_valid():
            doctor = serializer.save()

            # Send email notification to admin for approval
            subject = 'Doctor Approval Request'
            message = f'A new doctor ({doctor.user.first_name}) has been registered and requires approval.'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = 'shadiyackn@gmail.com'
            send_mail(subject, message, from_email, [to_email])

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            is_valid = serializer.is_valid()
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

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
    

class SlotCreateAPIView(APIView):
    def post(self, request):
        serializer = PostSlotSerializers(data=request.data)
        if serializer.is_valid():
            doctor = serializer.validated_data['doctor']
            date = serializer.validated_data['date']
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']
            slot_duration = int(serializer.validated_data['slot_duration'])
            slot_count = (datetime.datetime.combine(date, end_time) - datetime.datetime.combine(date, start_time)) // datetime.timedelta(minutes=slot_duration)

            slots = []
            current_time = start_time
            for _ in range(slot_count):
                slot = Slots(
                    doctor=doctor,
                    date=date,
                    start_time=current_time,
                    end_time=(datetime.datetime.combine(date, current_time) + datetime.timedelta(minutes=slot_duration)).time(),
                    status=True,
                    slot_duration=slot_duration,
                )
                slots.append(slot)
                current_time = (datetime.datetime.combine(date, current_time) + datetime.timedelta(minutes=slot_duration)).time()

            Slots.objects.bulk_create(slots)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    

class AppointmentListAPIView(APIView):
    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = Appointmentserializer(appointments, many=True)
        return Response(serializer.data)


class viewDoctorRequestView(APIView):
    def get(self, request, id):
        try:
            doctor = Doctors.objects.get(id=id)  #
            serializer = PostDoctorSerializers(doctor, many=False)  # Pass many=False for a single object
            return Response(serializer.data)
        except Doctors.DoesNotExist:
            return Response({'msg': 'Doctor not found'})
        except Exception as e:
            return Response({'msg': str(e)})


class UsersDoctorsView(ListAPIView):
    serializer_class = DoctorsSerializers
    # queryset = Doctors.objects.filter(is_approved=True)
    def get_queryset(self):
        return Doctors.objects.filter(is_approved=True)
    

class getDoctorInHome(APIView):
    def get(self,request,id):
        try:
            doctor = Doctors.objects.get(id=id)
            serializer = DoctorsSerializers(doctor, many=False)
            return Response(serializer.data)
        except Doctors.DoesNotExist:
            return Response({'msg': 'Doctor not found'})
        except Exception as e:
            return Response({'msg': str(e)})

class GetSlotsInHome(APIView):
    def get(self,request,id):
        try:
            slot = Slots.objects.filter(doctor_id=id)
            serializer = SlotSerializers(slot,many=True)
            return Response(serializer.data)
        except Slots.DoesNotExist:
            return Response({'msg': 'slot not exits'})
        except Exception as e:
            return Response({'msg': str(e)})
        

class UsersListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # get_queryset overridden to customize the queryset.
    def get_queryset(self):
        return User.objects.filter(is_admin=False, is_staff=False, is_superadmin=False)
    
 

class blockDoctors(APIView):
    def patch(self, request, id):
        print(id)
        try:
            user = User.objects.get(id=id)
            user.is_active = not user.is_active
            user.save()
            return Response({'msg': "Doctor status updated successfully"})
        except User.DoesNotExist:
            print('no users')
            return Response({'msg': "doctor not found"})
        except Exception as e:
            print(e)
            return Response({'msg': str(e)})


class doctorsListView(ListAPIView):
    serializer_class = UserSerializer
    # get_queryset overridden to customize the queryset.
    def get_queryset(self):
        return User.objects.filter(is_admin=False, is_staff=True, is_superadmin=False)        