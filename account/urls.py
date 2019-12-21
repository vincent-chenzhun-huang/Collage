from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # The three urls using Django's built in User model for login, logout, and signup
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.register, name='signup'),
    # The dashboard which displays the image number and greeting messages
    path('', views.dashboard, name='dashboard'),
    # Django's built-in User model for credential changes
    path('password_change/', auth_views.PasswordChangeView.as_view(), name="password_change"),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('users/', views.user_list, name='user_list'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('users/follow', views.user_follow, name='user_follow'),
]