from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from .serializers import UserSerializer 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from user.models import User
from django.http import HttpResponseRedirect
 

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        # token['userType'] = user.userType
        token['is_doctor'] =user.is_staff
        token['is_admin']=user.is_superadmin
        # ...

        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

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