from django.urls import path
from . import views
from . views import MyTokenObtainPairView,UserRegistration

from rest_framework_simplejwt.views import (
  
    TokenRefreshView,
)


urlpatterns = [
    path('',views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserRegistration.as_view()),
    path('activate/<uidb64>/<token>',views.activate, name='activate')
]