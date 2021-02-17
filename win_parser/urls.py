from django.urls import path
from django.contrib.auth import views as auth_views
from win_parser import views

app_name = 'win_parser'

urlpatterns = [
    path('upload/', views.FileUploadView.as_view(), name='upload'),
    path('config/<int:pk>/', views.delete_config_file, name='delete_config_file'),
    path('parse/', views.parse_configs, name='parse_configs'),
    path('report/overview', views.ReportView.as_view(), name='reports')
]

