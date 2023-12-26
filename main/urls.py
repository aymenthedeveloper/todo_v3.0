from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_updated, name='home'),
    path('delete_task/<int:pk>', views.delete_task, name='delete_task'),
    path('edit_task/<int:pk>', views.edit_task, name='edit_task'),
    path('complete_task/<int:pk>', views.complete_task, name='complete_task'),
    path('login_user/', views.login_user, name='login_user'),
    path('edit_user/', views.update_user, name='edit_user'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('signup_user/', views.signup_user, name='signup_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('user_profile/', views.user_profile, name='user_profile'),
     path('activate/<uidb64>/<token>', views.activate, name='activate'),
     path('password_reset/<uidb64>/<token>', views.reset_pw, name='reset_pw'),
]