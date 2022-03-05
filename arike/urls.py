"""arike URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from app.views import (CreateMemberView, CreateUserView, DeleteMemberView, DeleteUserView, DetailUserView,
                       GenericFacilityCreateView, GenericFacilityDeleteView,
                       GenericFacilityDetailView, GenericFacilityUpdateView,
                       GenericFacilityView, GenericPatientCreateView,
                       GenericPatientDeleteView, GenericPatientDetailView,
                       GenericPatientUpdateView, GenericPatientView, ListFamilyView, LoginView,
                       ProfileView, UpdateMemberView, UpdatePasswordView, UpdateProfileView,
                       UpdateUserView, UsersListView)
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',LoginView.as_view()),
    path('logout',LogoutView.as_view()),
    path('profile',ProfileView.as_view()),
    path('update-profile',UpdateProfileView.as_view()),
    path('update-pass',UpdatePasswordView.as_view()),]
urlpatterns += [
    path('users',UsersListView.as_view(), name='users'),
    path('user/<pk>',DetailUserView.as_view(), name='users'),
    path('add-user',CreateUserView.as_view(), name='users'),
    path('update-user/<pk>',UpdateUserView.as_view(), name='users'),
    path('delete-user/<pk>',DeleteUserView.as_view(), name='users'),
]
urlpatterns += [
    path('facilities',GenericFacilityView.as_view(), name='facility'),
    path('add-facilities',GenericFacilityCreateView.as_view(), name='facility'),
    path('facility/<pk>',GenericFacilityDetailView.as_view(), name='facility'),
    path('update-facility/<pk>',GenericFacilityUpdateView.as_view(), name='facility'),
    path('delete-facility/<pk>',GenericFacilityDeleteView.as_view(), name='facility'),
]
urlpatterns += [
    path('patients',GenericPatientView.as_view(), name='patient'),
    path('add-patient',GenericPatientCreateView.as_view(), name='patient'),
    path('patient/<pk>',GenericPatientDetailView.as_view(), name='patient'),
    path('update-patient/<pk>',GenericPatientUpdateView.as_view(), name='patient'),
    path('delete-patient/<pk>',GenericPatientDeleteView.as_view(), name='patient')
]

urlpatterns += [
    path('patient/<pk>/family-details',ListFamilyView.as_view(), name='patient'),
    path('patient/<int:patient>/add-member',CreateMemberView.as_view(), name='patient'),
    path('patient/<pk>/update-member',UpdateMemberView.as_view(), name='patient'),
    path('delete-member/<pk>',DeleteMemberView.as_view(), name='patient'),
]
