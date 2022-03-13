from datetime import datetime, timedelta
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from app.forms import (CustomUserCreationForm, CustomUserUpdateForm,
                       DiseaseHistoryCreateForm, FacilityCreateForm,
                       FamilyCreateForm, HealthInfoForm, PatientCreateForm,
                       TreatementCreateForm, TreatmentNoteForm, VisitScheduleCreateForm)
from app.models import (CustomUser, Facility, FamilyDetail, Patient,
                        PatientDisease,  Treatment, TreatmentNotes, VisitDetails, VisitSchedule)


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
        pk = self.kwargs["patient"]
        context['patient'] = Patient.objects.get(pk=pk)
        return context

    def get_queryset(self):
        pk = self.kwargs["patient"]
        qs = FamilyDetail.objects.filter(patient=pk)
        return qs

class CreateMemberView(CreateView):
    model = FamilyDetail
    form_class = FamilyCreateForm
    template_name = "family/create.html"

    def get_success_url(self):
        pk = self.kwargs["patient"]
        return f"/patient/{pk}/family-details"

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

class ListDiseaseHistoryView(ListView):
    model = PatientDisease
    template_name = "patient_disease/list.html"
    context_object_name = "objects"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        context['patient'] = Patient.objects.get(pk=pk)
        return context

    def get_queryset(self):
        pk = self.kwargs["pk"]
        qs = PatientDisease.objects.filter(patient=pk)
        return qs


class CreateDiseaseHistoryView(CreateView):
    model = PatientDisease
    form_class = DiseaseHistoryCreateForm
    template_name = "patient_disease/create.html"

    def get_success_url(self):
        pk = self.kwargs["patient"]
        return f"/patient/{pk}/disease-history"

    def form_valid(self, form):
        self.object = form.save()
        patient = self.kwargs["patient"]
        self.object.patient = Patient.objects.get(pk=patient)
        self.object.investigated_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class DeleteDiseaseHistoryView(DeleteView):
    model = PatientDisease
    template_name = "patient_disease/delete.html"
    success_url = "/patients"

class UpdateDiseaseHistoryView(UpdateView):
    model = PatientDisease
    form_class = DiseaseHistoryCreateForm
    template_name = "patient_disease/update.html"
    success_url = "/patients"
########################################################################################
########################################################################################

class ListTreatmentView(ListView):
    model = Treatment
    template_name = "treatment/list.html"
    context_object_name = "objects"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        context['patient'] = Patient.objects.get(pk=pk)
        return context

    def get_queryset(self):
        pk = self.kwargs["pk"]
        qs = Treatment.objects.filter(patient=pk)
        return qs

class DetailTreatmentView(DetailView):
    model = Treatment
    template_name = "treatment/detail.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        context['notes'] = TreatmentNotes.objects.filter(treatment=pk)
        return context

class CreateTreatmentView(CreateView):
    model = Treatment
    form_class = TreatementCreateForm
    template_name = "treatment/create.html"

    def get_success_url(self):
        pk = self.kwargs["patient"]
        return f"/patient/{pk}/treatments"

    def form_valid(self, form):
        self.object = form.save()
        patient = self.kwargs["patient"]
        self.object.patient = Patient.objects.get(pk=patient)
        self.object.given_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class DeleteTreatmentView(DeleteView):
    model = Treatment
    template_name = "treatment/delete.html"
    success_url = "/patients"

class UpdateTreatmentView(UpdateView):
    model = Treatment
    form_class = TreatementCreateForm
    template_name = "treatment/update.html"
    success_url = "/patients"

class ListVisitHistoryView(ListView):
    model = VisitSchedule
    template_name = "patient/visits.html"
    context_object_name = "objects"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        context['patient'] = Patient.objects.get(pk=pk)
        return context

    def get_queryset(self):
        pk = self.kwargs["pk"]
        qs = VisitSchedule.objects.filter(patient=pk)
        return qs

########################################################################################
########################################################################################

class ListScheduleView(ListView):
    model = Patient
    template_name = "visit/list.html"
    context_object_name = "objects"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['treatments'] = Treatment.objects.all()
        return context

    # def get_queryset(self):
    #TODO: filter acc. to assigned patients and role
        # qs = Patient.objects.filter()
        # return qs

class AgendaView(ListView):
    model = VisitSchedule
    template_name = "visit/agenda.html"
    context_object_name = "objects"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.now()
        tommorow = datetime.now() + timedelta(days=1)
        context['today'] = today.strftime("%B %d, %Y")
        context['tom'] = tommorow.strftime("%B %d, %Y")
        return context

    def get_queryset(self):
        user = self.request.user
        qs = VisitSchedule.objects.filter(scheduled_by=user).order_by('visit_at')
        return qs


class CreateVisitSchedule(CreateView):
    model = VisitSchedule
    form_class = VisitScheduleCreateForm
    template_name = "visit/create.html"
    success_url = '/schedule'

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = Patient.objects.get(pk=pk)
        self.object = form.save()
        self.object.patient = patient
        self.object.scheduled_by = self.request.user
        details = VisitDetails.objects.create(General_Random_Blood_Sugar=0)
        self.object.visit_details = details
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = Patient.objects.get(pk=pk)
        context['patient'] = patient
        return context
        
class DeleteVisitView(DeleteView):
    model = VisitSchedule
    template_name = "visit/delete.html"
    success_url = "/agenda"

########################################################################################
########################################################################################

class PatientVisitView(DetailView):
    template_name = "visit/menu.html"
    model = VisitSchedule

class UpdateHealthInfoView(UpdateView):
    model = VisitDetails
    form_class = HealthInfoForm
    template_name = "visit/health.html"
    success_url = "/agenda"
    
    def get_object(self):
        pk = self.kwargs["visit"]
        visit = VisitSchedule.objects.get(pk=pk)
        obj =  VisitDetails.objects.get(pk=visit.visit_details.id)
        return obj

########################################################################################
########################################################################################

class ListActiveTreatmentView(ListView):
    model = Treatment
    template_name="visit/treatments.html"
    context_object_name = "objects"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["visit"]
        context['visit'] = pk
        context['patient'] = context["objects"][0].patient
        return context

    def get_queryset(self):
        pk = self.kwargs["visit"]
        visit = VisitSchedule.objects.get(pk=pk)
        qs = Treatment.objects.filter(patient=visit.patient)
        return qs

class AddTreatementNoteView(CreateView):
    model = TreatmentNotes
    form_class = TreatmentNoteForm
    template_name = "visit/create_note.html"
    success_url = '/schedule'

    def form_valid(self, form):
        self.object = form.save()
        pk = self.kwargs["pk"]
        visit = self.kwargs["visit"]
        treatment = Treatment.objects.get(pk=pk)
        visit = VisitSchedule.objects.get(pk=visit)
        self.object.treatment = treatment
        self.object.visit = visit
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        treatment = Treatment.objects.get(pk=pk)
        context['treatment'] = treatment
        return context

########################################################################################