from django.urls import path
from . import views


from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)



urlpatterns = [
     
    path('createDoctors/',views.DoctorsCreateAPIView.as_view(), name='createDoctors'),
    path('createDepartment/',views.createDepartment,name='createDepartment'),
    path('departments/',views.DepartmentListView.as_view(),name="departments"),
    path('homelistdoctor/',views.HomeListDoctor.as_view(),name="homelistdoctor"),
    path('homelistdepartment/',views. HomeListDepartment.as_view(),name="homelistdepartment")
]