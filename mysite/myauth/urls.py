from . import views

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'myauth'

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            template_name='myauth/login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('session/get/', views.GetSession.as_view(), name='getsession'),
    path('session/set/', views.SetSession.as_view(), name='setsession'),
    path('cookies/get/', views.GetCookies.as_view(), name='getcookies'),
    path('cookies/set/', views.SetCookies.as_view(), name='setcookies'),
    path('user/info/<int:pk>/', views.UserInfoView.as_view(), name='user_details'),
    path('user/info/', views.UserInfoView.as_view(), name='about_me'),
    path('user/update/<int:pk>/', views.UserInfoUpdateView.as_view(), name='update_user_info'),
    path('users/', views.UsersListView.as_view(), name='users_list'),
]