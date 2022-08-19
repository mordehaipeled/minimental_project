from django.urls import path

from . import views
# here to direct paths to the functions in views
urlpatterns = [
    path('', views.postsign, name='login'),
    path('home/', views.home, name="home"),
    path('logout/', views.user_logout, name='login'),
    path('patient_detail/', views.patient_detail, name="patient_detail"),
    path('patient_detail/check', views.patient_detail_check, name="patient_detail_check"),
    path('patient_detail/make_new_test', views.make_new_test, name="make_new_test"),
    path('patient_detail/edit_score', views.edit_score, name="edit_score"),
    path('register/', views.register_new_doctor, name="register"),
    path('add_patient/', views.register_new_patient, name="add_patient"),
    path('add_patient/validate_email', views.validate_email, name="add_patient"),
    path('eng/', views.postsign, name='loginEng')
]
