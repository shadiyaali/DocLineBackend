from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('createDoctors/', views.DoctorsCreateAPIView.as_view(), name='createDoctors'),
    path('createDepartment/', views.createDepartment, name='createDepartment'),
    path('departments/', views.DepartmentListView.as_view(), name="departments"),
    path('homelistdoctor/', views.HomeListDoctor.as_view(), name="homelistdoctor"),
    path('homelistdepartment/', views.HomeListDepartment.as_view(), name="homelistdepartment"),
   path('scheduleappointment/', views.SlotCreateAPIView.as_view(), name='scheduleappointment'),

    path('viewDoctorRequest/<int:id>/', views.viewDoctorRequestView.as_view(), name='viewDoctorRequest'),
    path('docorsUserSide/', views.UsersDoctorsView.as_view(), name='docorsUserSide'),
    path('getDoctorHome/<int:id>/', views.getDoctorInHome.as_view(), name='getDoctorHome'),
    


    path('users/',views.UsersListView.as_view(), name='user-list'),

    path('doctors/',views.doctorsListView.as_view(),name='doctorsList'),
    path('blockdoctor/<int:id>/',views.BlockDoctor.as_view(),name='blockdoctors'),
    path('doctorsRequest/',views.DoctorsRequestsView.as_view(),name='doctorsRequest'),
    path('acceptdoctor/<int:id>/', views.AcceptDoctor.as_view(), name='acceptdoctor'),
    path('rejectdoctor/<int:id>/', views.RejectDoctor.as_view(), name='rejectdoctor'),

]