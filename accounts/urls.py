from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html', success_url='/accounts/profile'), name='change-password'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit_profile', views.ProfileEditView.as_view(), name='edit-profile'),
]