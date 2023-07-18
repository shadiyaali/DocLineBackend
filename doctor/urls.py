from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('createDoctors/', views.DoctorsCreateAPIView.as_view(), name='createDoctors'),
   
    path('departments/', views.DepartmentListView.as_view(), name="departments"),
    path('createDepartment/', views.CreateDepartmentView.as_view(), name='create_department'),
    path('homelistdoctor/', views.HomeListDoctor.as_view(), name="homelistdoctor"),
    path('homelistdepartment/', views.HomeListDepartment.as_view(), name="homelistdepartment"),
    path('scheduleappointment/', views.SlotCreateAPIView.as_view(), name='scheduleappointment'),
    path('appointments/',views.AppointmentListAPIView.as_view(),name="appointments"),
    path('appointmentsDoctor/<int:id>/',views. DoctorAppointmentsAPIView.as_view(), name='doctor_appointments'),
    path('updateAppointmentStatus/<int:appointment_id>/',views.Update_appointment_status, name='update_appointment_status'),
    path('createPresciption/',views.PrescriptionCreateAPIView.as_view(),name='createPrescription'),
    path('usersPrescription/<int:id>/',views.GetUserPrescriptionAPIView.as_view(),name='usersPrescription'),
   
     
    path('viewDoctorRequest/<int:id>/', views.viewDoctorRequestView.as_view(), name='viewDoctorRequest'),
    path('docorsUserSide/', views.UsersDoctorsView.as_view(), name='docorsUserSide'),
    path('getDoctorUser/<int:id>/', views.GetDoctorUser.as_view(), name='getDoctorUser'),
    path('getSlotsUser/<int:id>/',views.GetSlotsUser.as_view(),name='getSlotsUser'),
    path('updateDepartment/<int:pk>/', views.DepartmentUpdateView.as_view(), name='update_department'),
    path('deleteDepartment/<int:pk>/',views.DepartmentDeleteView.as_view(), name='delete_department'),


    path('users/',views.UsersListView.as_view(), name='user-list'),

    path('doctors/',views.doctorsListView.as_view(),name='doctorsList'),
    path('blockdoctor/<int:id>/',views.BlockDoctor.as_view(),name='blockdoctors'),
    path('doctorsRequest/',views.DoctorsRequestsView.as_view(),name='doctorsRequest'),
    path('acceptdoctor/<int:id>/', views.AcceptDoctor.as_view(), name='acceptdoctor'),
    path('rejectdoctor/<int:id>/', views.RejectDoctor.as_view(), name='rejectdoctor'),
] 