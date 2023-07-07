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
    path('activate/<uidb64>/<token>',views.activate, name='activate'),
    path('forgot_password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('resetPassword_validate/<uidb64>/<token>/',views.resetPassword_validate,name='resetPassword_validate'),
    path('resetPassword/',views.ResetPasswordView.as_view(), name='reset_password'),
    path('updateUser/<int:pk>/', views.UserUpdateView.as_view(), name='update-user'),

    path('getSingleUser/<int:id>/',views.getSingleUser.as_view(),name='getDoctorInHome'),
    path('blockuser/<int:id>/',views.BlockUser.as_view(),name="blockuser") 
]