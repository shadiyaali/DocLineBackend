from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import UserSerializer 
from doctor.serializers import AppointmentSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from user.models import User
from doctor.models import Appointment
from django.http import HttpResponseRedirect
from rest_framework.generics import UpdateAPIView 



@api_view(['GET'])
def getRoutes(request):
    routes=[
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)


class UserRegistration(APIView):
      def post(self, request, format=None):
          email = request.data.get('email')
          print(request.data)
        

          serializer = UserSerializer(data=request.data)
          #print(serializer.is_valid())
          if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            mail_subject = 'Please activate your account'
            
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': uid,
                'token': token,
                'usename': urlsafe_base64_encode(force_bytes(user.email))
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({'msg':'Registration Success'}, status=status.HTTP_201_CREATED)
            
          print(serializer.errors)
          return Response({'msg':'Registration Failed',}, status=status.HTTP_400_BAD_REQUEST)
  

@api_view(['GET'])
def activate(request, uidb64, token):
    try:

        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        print('checked')
        user.is_active = True
        user.save()
      

        return HttpResponseRedirect('http://localhost:3000/login')
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.first_name
        token['is_staff'] = user.is_staff
        token['is_admin'] = user.is_superadmin 

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ForgotPasswordView(APIView):
     def post(self, request:Response):
        email = request.data['email']
        print(email)
        if User.objects.filter(email=email).exists:
            user = User.objects.get(email__exact=email)

            current_site=get_current_site(request)
            mail_subject = 'Reset your password'
            message=render_to_string('accounts/Reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return Response({'message':'Forgot password mail sented Success','user':user.id})
        else:
            return Response({"message": "failed to sent msg"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def resetPassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        return HttpResponseRedirect('http://localhost:3000/ResetPassword')
    else:
        return Response({'message':'Forgot password mail sented Success'}) 

class ResetPasswordView(APIView):
    def post(self, request: Response):
        password = request.data['password']
        user_data = request.data['storedData']
        user_id = user_data['user']
       
       
        if password :
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            return Response({'message': 'Password changed successfully'})
        else:
            return HttpResponseRedirect('http://localhost:3000/ResetPassword')


class UsersListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def get_queryset(self):
        return User.objects.filter(is_admin=False, is_staff=False, is_superadmin=False)

class BlockUser(APIView):
    def patch(self, request, id):
        try:
            user = get_user_model().objects.get(id=id)
            user.is_active = not user.is_active
            user.save()
            if user.is_active:
                msg = "Blocked successfully"
            else:
                msg = "Unblocked successfully"
            return Response({'msg': msg})
        except get_user_model().DoesNotExist:
            return Response({'msg': "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class getSingleUser(APIView):
    def get(self,request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, many=False)
            appointment = Appointment.objects.filter(patient=id)
            if appointment :
                appointment_serializer = AppointmentSerializer(appointment,many=True)
                return Response({'appointment':appointment_serializer.data,'userDetails':serializer.data})
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'msg': 'Doctor not found'})
        except Exception as e:
            return Response({'msg': str(e)})

class UserUpdateView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class GetAppointmentsAPIView(APIView):
    def get(self, request,id):
        current_user = User.objects.get(id=id)
        appointments = Appointment.objects.filter(patient=current_user)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)