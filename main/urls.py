from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('si_stats/', views.si_stats, name='si_stats'),
    path('isi_stats/', views.isi_stats, name='isi_stats'),
    path('stats/', views.stats, name='stats'),
    path('students/<int:id>/', views.student_details, name='student_details'),
    path('students/views/', views.all_views ),
    path('compare-students', views.compare_students, name='compare_students'),
]
