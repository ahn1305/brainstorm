from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required




urlpatterns = [
  path('user_register/', views.user_register , name='register'),
  path('user_register/verify/', views.user_register_verify_view, name='register-verify-view'),
  path('user_login/', views.user_login ,name='login'),
  path('user_login/verify/', views.user_login_verify_view ,name='login-verify-view'),
  path('user_logout/', views.user_logout ,name= 'user_logout'),
  path('profile/', views.profile ,name= 'profile'),
  path('change_password/', views.change_password, name = "change-password"),
  path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html') ,name= 'password_reset'),
  path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html') ,name= 'password_reset_done'),
  path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html') ,name= 'password_reset_confirm'),
  path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html') ,name= 'password_reset_complete'),
  path('<str:username>/delete/', views.delete_user, name='account_delete'),

  
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)