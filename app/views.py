from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.list import ListView

from app.forms import CustomUserCreationForm, CustomUserUpdateForm, FacilityCreateForm, FamilyCreateForm, PatientCreateForm


from app.models import CustomUser, Facility, FamilyDetail, Patient


# Create your views here.
########################################################################################
class UserLoginView(LoginView):
    template_name = "registration/login.html"
    success_url = '/profile'
########################################################################################
class CreateUserView(CreateView):
    model = CustomUser
    template_name = 'users/create.html'
    form_class = CustomUserCreationForm
    success_url = '/users'

class UpdateUserView(UpdateView):
    model = CustomUser
    template_name = 'users/update.html'
    form_class = CustomUserUpdateForm
    success_url = '/users'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return f"/user/{pk}" 

class DetailUserView(DetailView):
    model = CustomUser
    template_name = 'users/detail.html'
    context_object_name = "object"

    def get_queryset(self):
        pk = self.kwargs["pk"]
        qs = CustomUser.objects.filter(pk=pk)
        return qs

class UsersListView(ListView):
    model = CustomUser
    template_name = "users/list.html"
    context_object_name = "users"

    def get_queryset(self):
        return CustomUser.objects.filter().exclude(role=30)

class DeleteUserView(DeleteView):
    model = CustomUser
    template_name = "users/delete.html"
    success_url = "/users"
########################################################################################
########################################################################################

class ProfileView(LoginRequiredMixin,DetailView):
    model = CustomUser
    template_name = 'users/profile.html'

    def get_object(self):
        return self.request.user

class UpdateProfileView(LoginRequiredMixin,UpdateView):
    model = CustomUser
    template_name = 'users/update_profile.html'
    form_class = CustomUserUpdateForm
    success_url = "/profile"


    def get_object(self):
        return self.request.user

class UpdatePasswordView(LoginRequiredMixin,UpdateView):
    model = CustomUser
    template_name = 'users/update_profile.html'
    form_class = PasswordChangeForm

    def get_object(self):
        return self.request.user
########################################################################################
########################################################################################

class GenericFacilityView(ListView):
    model = Facility
    template_name = "facility/list.html"
    context_object_name = "facs"

class GenericFacilityCreateView(CreateView):
    model = Facility
    form_class = FacilityCreateForm
    template_name = "facility/create.html"
    success_url = "/facilities"

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

class GenericFacilityDetailView(DetailView):
    model = Facility
    template_name = "facility/detail.html"

class GenericFacilityUpdateView(UpdateView):
    model = Facility
    form_class = FacilityCreateForm
    template_name = "facility/update.html"
    # success_url = "/facilities"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return f"/facility/{pk}" 

class GenericFacilityDeleteView(DeleteView):
    model = Facility
    template_name = "facility/delete.html"
    success_url = "/facilities"
########################################################################################
########################################################################################

class GenericPatientView(ListView):
    model = Patient
    template_name = "patient/list.html"
    context_object_name = "patients"

class GenericPatientCreateView(CreateView):
    model = Patient
    form_class = PatientCreateForm
    template_name = "patient/create.html"
    success_url = "/patients"

#     def form_valid(self, form):
#         self.object = form.save()
#         return HttpResponseRedirect(self.get_success_url())

class GenericPatientDetailView(DetailView):
    model = Patient
    template_name = "patient/detail.html"

class GenericPatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientCreateForm
    template_name = "patient/update.html"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return f"/patient/{pk}"        
    
class GenericPatientDeleteView(DeleteView):
    model = Patient
    template_name = "patient/delete.html"
    success_url = "/patients"

########################################################################################
########################################################################################
class ListFamilyView(ListView):
    model = FamilyDetail
    template_name = "family/list.html"
    context_object_name = "objects"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        context['patient'] = Patient.objects.get(pk=pk)
        return context

    def get_queryset(self):
        pk = self.kwargs["pk"]
        qs = FamilyDetail.objects.filter(patient=pk)
        return qs

class CreateMemberView(CreateView):
    model = FamilyDetail
    form_class = FamilyCreateForm
    template_name = "family/create.html"

    def get_success_url(self):
        pk = self.kwargs["patient"]
        return f"/family-details/{pk}"

    def form_valid(self, form):
        self.object = form.save()
        patient = self.kwargs["patient"]
        self.object.patient = Patient.objects.get(pk=patient)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class DeleteMemberView(DeleteView):
    model = FamilyDetail
    template_name = "family/delete.html"
    success_url = "/patients"

class UpdateMemberView(UpdateView):
    model = FamilyDetail
    form_class = FamilyCreateForm
    template_name = "family/update.html"
    success_url = "/patients"


########################################################################################
########################################################################################



########################################################################################