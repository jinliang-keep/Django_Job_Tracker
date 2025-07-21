from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('job_list/', views.job_list, name='job_list'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    # path('edit_job/<int:job_id>', views.edit_job, name='edit_job'),
    path('job_detail/<int:job_id>/', views.job_detail, name='job_detail'),
]