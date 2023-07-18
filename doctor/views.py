from user.models import User
from user.serializers import UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (  DepartmentSerializers, PostDoctorSerializers,AppointmentSerializer,
                          DoctorsSerializers, SlotSerializer, PostSlotSerializer,PostPrescriptionSerializer,PrescriptionSerializer)
from .models import Department, Doctors
from rest_framework.decorators import api_view
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .serializers import PostDoctorSerializers
from .models import Doctors, Slots ,Appointment,Prescription
import datetime
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import generics
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView
 

 

class DoctorsCreateAPIView(APIView):
    def post(self, request, format=None):
        print(request.data)

        
        serializer = PostDoctorSerializers(data=request.data)
        if serializer.is_valid():
            doctor = serializer.save()

            # Send email notification to admin for approval
            # subject = 'Doctor Approval Request'
            # message = f'A new doctor ({doctor.user.first_name}) has been registered and requires approval.'
            # from_email = settings.DEFAULT_FROM_EMAIL
            # to_email = 'shadiyackn@gmail.com'
            # send_mail(subject, message, from_email, [to_email])

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
 

 

class CreateDepartmentView(APIView):
    def post(self, request):
        serializer = DepartmentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

class DepartmentUpdateView(UpdateAPIView):
    serializer_class = DepartmentSerializers
    queryset = Department.objects.all()




class DepartmentDeleteView(APIView):
    def delete(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


 
 

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
    


        

class UsersListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # get_queryset overridden to customize the queryset.
    def get_queryset(self):
        return User.objects.filter(is_admin=False, is_staff=False, is_superadmin=False)
    
 

class BlockDoctor(APIView):
    def get(self, request, id):
        try:
            doctor = Doctors.objects.get(id=id)
            doctor.is_blocked = not doctor.is_blocked
            doctor.save()
            return Response({'msg': "Doctor status updated successfully"})
        except Doctors.DoesNotExist:
            return Response({'msg': "Doctor not found"})
        except Exception as e:
            return Response({'msg': str(e)})


class doctorsListView(ListAPIView):
    serializer_class = DoctorsSerializers

    def get_queryset(self):
        return Doctors.objects.filter(is_approved=True)

           
    


class DoctorsRequestsView(ListAPIView):
    serializer_class = DoctorsSerializers
    queryset = Doctors.objects.all()
    
    def get_queryset(self):
        return Doctors.objects.filter(is_approved=False)


class AcceptDoctor(APIView):
    def post(self, request, id):
        print(id)
        try:
            doctor = Doctors.objects.get(id=id)
        except Doctors.DoesNotExist:
            return Response({'msg': "User not found"})

        # Update doctor's approval status and set them as staff
        doctor.is_approved = True
        email = doctor.user.email

        user_data = User.objects.get(email=email)
        user_data.is_staff = True
        user_data.save()
        print(user_data)
        doctor.save()

        # Send email to the doctor
        current_site = get_current_site(request)
        mail_subject = 'Doctor request Accepted'
        message = render_to_string('acceptDoctor.html', {
            'doctor': doctor,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(doctor.user.pk)),
            'token': default_token_generator.make_token(doctor.user),
        })
        to_email = doctor.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        return Response({'msg': "Request accepted successfully"})


class RejectDoctor(APIView):
    def post(self, request, id):
        try:
            doctor = Doctors.objects.get(id=id)
            email = doctor.user.email
            current_site = get_current_site(request)
            mail_subject = 'Doctor request Rejected'
            message = render_to_string('rejectDoctor.html', {
                'doctor': doctor,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(doctor.user.pk)),
                'token': default_token_generator.make_token(doctor.user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({'msg': "Request rejected successfully"})
        except Doctors.DoesNotExist:
            return Response({'msg': "User not found"})
        except Exception as e:
            return Response({'message': str(e)})


class SlotCreateAPIView(APIView):
    def post(self, request):
        serializer = PostSlotSerializer(data=request.data)
        valid = serializer.is_valid()
        print(serializer.errors)
        if serializer.is_valid():
            doctor = serializer.validated_data['doctor']
            date = serializer.validated_data['date']
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']
            slot_duration = int(serializer.validated_data['slot_duration'])
            

            overlapping_slots = Slots.objects.filter(
                Q(date=date) & (
                    Q(start_time__lt=start_time, end_time__gt=start_time) |
                    Q(start_time__lt=end_time, end_time__gt=end_time) |
                    Q(start_time__gte=start_time, end_time__lte=end_time)
                )
            )

            if overlapping_slots.exists():
                return Response({'error': 'Slot overlaps with existing slots'}, status=status.HTTP_400_BAD_REQUEST)
            # Slot creation logic
            # Adjust the code below as per your requirements
            slots = []
            current_time = start_time
            slot_count = (datetime.datetime.combine(date, end_time) - datetime.datetime.combine(date, start_time)) // datetime.timedelta(minutes=slot_duration)
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
    
class GetDoctorUser(APIView):
    def get(self,request,id):
        try:
            doctor = Doctors.objects.get(id=id)
            print(doctor)
            serializer = DoctorsSerializers(doctor, many=False)
            return Response(serializer.data)
        except Doctors.DoesNotExist:
            return Response({'msg': 'Doctor not found'})
        except Exception as e:
            return Response({'msg': str(e)})

class GetSlotsUser(APIView):
    def get(self,request,id):
        print(id)
        slot = Slots.objects.filter(doctor=id,is_booked=False)
        serializer = SlotSerializer(slot,many=True)

        return Response(serializer.data)

 



class AppointmentListAPIView(APIView):
    def get(self, request):
        
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

class DoctorAppointmentsAPIView(APIView):
    def get(self, request,id):
        try:
            current_user=User.objects.get(id=id)
            doctor = Doctors.objects.get(user=current_user)
            appointments = Appointment.objects.filter(doctor=doctor)
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response("Appointments not found", status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
def Update_appointment_status(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response({"message": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('status')
    if not new_status:
        return Response({"message": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)

    appointment.status = new_status
    appointment.save()

    return Response({"message": "Appointment status updated successfully"})


class PrescriptionCreateAPIView(APIView):
    def post(self, request):
        serializer = PostPrescriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class GetUserPrescriptionAPIView(APIView):
    def get(self,request,id):
        try:
            print(id)
            prescription = Prescription.objects.filter(patient=id)
            serializer = PrescriptionSerializer(prescription,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Prescription.DoesNotExist:
            return Response("Prescription not found", status=status.HTTP_404_NOT_FOUND)
   