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

from app.forms import (AssignNurseForm, CustomUserCreationForm,
                       CustomUserUpdateForm, DiseaseHistoryCreateForm,
                       FacilityCreateForm, FamilyCreateForm, HealthInfoForm,
                       PatientCreateForm, TreatementCreateForm,
                       TreatmentNoteForm, VisitScheduleCreateForm)
from app.mixins import RoleRequiredMixin
from app.models import (CustomUser, Facility, FamilyDetail, Patient,
                        PatientDisease, PatientNurseModel, Treatment,
                        TreatmentNotes, VisitDetails, VisitSchedule)
from app.tasks import bg_jobs


# Create your views here.
########################################################################################
class UserLoginView(LoginView):
    template_name = "registration/login.html"
    success_url = '/profile'
########################################################################################
class CreateUserView(RoleRequiredMixin,CreateView):
    model = CustomUser
    user_role_required = [30]
    template_name = 'users/create.html'
    form_class = CustomUserCreationForm
    success_url = '/users'

class UpdateUserView(RoleRequiredMixin,UpdateView):
    model = CustomUser
    user_role_required = [30]
    template_name = 'users/update.html'
    form_class = CustomUserUpdateForm
    success_url = '/users'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return f"/user/{pk}" 

class DetailUserView(RoleRequiredMixin,DetailView):
    model = CustomUser
    user_role_required = [30]
    template_name = 'users/detail.html'
    context_object_name = "object"

    def get_queryset(self):
        pk = self.kwargs["pk"]
        qs = CustomUser.objects.filter(pk=pk)
        return qs

class UsersListView(RoleRequiredMixin,ListView):
    model = CustomUser
    user_role_required = [30]
    template_name = "users/list.html"
    context_object_name = "users"

    def get_queryset(self):
        return CustomUser.objects.filter().exclude(role=30)

class DeleteUserView(RoleRequiredMixin,DeleteView):
    model = CustomUser
    user_role_required = [30]
    template_name = "users/delete.html"
    success_url = "/users"
########################################################################################
########################################################################################

class ProfileView(LoginRequiredMixin,DetailView):
    model = CustomUser
    template_name = 'users/profile.html'

    def get_object(self):
        bg_jobs.delay()
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

class GenericFacilityView(RoleRequiredMixin,ListView):
    model = Facility
    user_role_required = [30]
    template_name = "facility/list.html"
    context_object_name = "facs"

class GenericFacilityCreateView(RoleRequiredMixin,CreateView):
    model = Facility
    user_role_required = [30]
    form_class = FacilityCreateForm
    template_name = "facility/create.html"
    success_url = "/facilities"

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

class GenericFacilityDetailView(RoleRequiredMixin,DetailView):
    model = Facility
    user_role_required = [30]
    template_name = "facility/detail.html"

class GenericFacilityUpdateView(RoleRequiredMixin,UpdateView):
    model = Facility
    user_role_required = [30]
    form_class = FacilityCreateForm
    template_name = "facility/update.html"
    # success_url = "/facilities"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return f"/facility/{pk}" 

class GenericFacilityDeleteView(RoleRequiredMixin,DeleteView):
    model = Facility
    user_role_required = [30]
    template_name = "facility/delete.html"
    success_url = "/facilities"
########################################################################################
########################################################################################

class GenericPatientView(RoleRequiredMixin,ListView):
    model = Patient
    template_name = "patient/list.html"
    context_object_name = "patients"

class GenericPatientCreateView(RoleRequiredMixin,CreateView):
    model = Patient
    form_class = PatientCreateForm
    template_name = "patient/create.html"
    success_url = "/patients"

class GenericPatientDetailView(RoleRequiredMixin,DetailView):
    model = Patient
    template_name = "patient/detail.html"

class GenericPatientUpdateView(RoleRequiredMixin,UpdateView):
    model = Patient
    form_class = PatientCreateForm
    template_name = "patient/update.html"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return f"/patient/{pk}"        
    
class GenericPatientDeleteView(RoleRequiredMixin,DeleteView):
    model = Patient
    template_name = "patient/delete.html"
    success_url = "/patients"

########################################################################################
########################################################################################
class ListFamilyView(RoleRequiredMixin,ListView):
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

class CreateMemberView(RoleRequiredMixin,CreateView):
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

class DeleteMemberView(RoleRequiredMixin,DeleteView):
    model = FamilyDetail
    template_name = "family/delete.html"
    success_url = "/patients"

class UpdateMemberView(RoleRequiredMixin,UpdateView):
    model = FamilyDetail
    form_class = FamilyCreateForm
    template_name = "family/update.html"
    success_url = "/patients"


########################################################################################
########################################################################################

class ListDiseaseHistoryView(RoleRequiredMixin,ListView):
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


class CreateDiseaseHistoryView(RoleRequiredMixin,CreateView):
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

class DeleteDiseaseHistoryView(RoleRequiredMixin,DeleteView):
    model = PatientDisease
    template_name = "patient_disease/delete.html"
    success_url = "/patients"

class UpdateDiseaseHistoryView(RoleRequiredMixin,UpdateView):
    model = PatientDisease
    form_class = DiseaseHistoryCreateForm
    template_name = "patient_disease/update.html"
    success_url = "/patients"
########################################################################################
########################################################################################

class ListTreatmentView(RoleRequiredMixin,ListView):
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

class DetailTreatmentView(RoleRequiredMixin,DetailView):
    model = Treatment
    template_name = "treatment/detail.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        context['notes'] = TreatmentNotes.objects.filter(treatment=pk)
        return context

class CreateTreatmentView(RoleRequiredMixin,CreateView):
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

class DeleteTreatmentView(RoleRequiredMixin,DeleteView):
    model = Treatment
    template_name = "treatment/delete.html"
    success_url = "/patients"

class UpdateTreatmentView(RoleRequiredMixin,UpdateView):
    model = Treatment
    form_class = TreatementCreateForm
    template_name = "treatment/update.html"
    success_url = "/patients"

class ListVisitHistoryView(RoleRequiredMixin,ListView):
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

class ListScheduleView(RoleRequiredMixin,ListView):
    model = Patient
    template_name = "visit/list.html"
    context_object_name = "objects"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        assigned_patients = PatientNurseModel.objects.filter(nurse=user)
        r = []
        for i in assigned_patients:
            r.append(i.patient)
        context['treatments'] = Treatment.objects.filter(patient__in=r)
        return context

    def get_queryset(self):
        user = self.request.user
        if user.role == 10:
            assigned_patients = PatientNurseModel.objects.filter(nurse=user)
            r = []
            for i in assigned_patients:
                r.append(i.patient.id)
            qs = Patient.objects.filter(id__in=r)
        else:
            qs = Patient.objects.all()
        return qs

class AgendaView(RoleRequiredMixin,ListView):
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


class CreateVisitSchedule(RoleRequiredMixin,CreateView):
    model = VisitSchedule
    form_class = VisitScheduleCreateForm
    template_name = "visit/create.html"
    success_url = '/schedule'

    def form_valid(self, form):
        user = self.request.user
        pk = int(self.kwargs["pk"])
        if user.role == 10:
            assigned_patients = PatientNurseModel.objects.filter(nurse=user)
            r = []
            for i in assigned_patients:
                r.append(i.patient.id)
            if not (pk in r):
                return HttpResponseRedirect('/schedule',status=400)
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
        pk = int(self.kwargs["pk"])
        patient = None
        user = self.request.user
        if user.role == 10:
            assigned_patients = PatientNurseModel.objects.filter(nurse=user)
            r = []
            for i in assigned_patients:
                r.append(i.patient.id)
            if pk in r:
                patient = Patient.objects.get(pk=pk)
        else:
            patient = Patient.objects.get(pk=pk)
        context['patient'] = patient
        return context
        
class DeleteVisitView(RoleRequiredMixin,DeleteView):
    model = VisitSchedule
    template_name = "visit/delete.html"
    success_url = "/agenda"

    def get_queryset(self):
        user = self.request.user
        qs = VisitSchedule.objects.filter(scheduled_by=user)
        return qs

########################################################################################
########################################################################################

class PatientVisitView(RoleRequiredMixin,DetailView):
    template_name = "visit/menu.html"
    model = VisitSchedule

class UpdateHealthInfoView(RoleRequiredMixin,UpdateView):
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

class ListActiveTreatmentView(RoleRequiredMixin,ListView):
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

class AddTreatementNoteView(RoleRequiredMixin,CreateView):
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
########################################################################################

class AssignNurseView(RoleRequiredMixin,CreateView):
    model = PatientNurseModel
    user_role_required = [20]
    success_url = '/patients'
    form_class = AssignNurseForm
    template_name = 'patient/assign-nurse.html'

    def form_valid(self, form):
        self.object = form.save()
        pk = self.kwargs["pk"]
        patient = Patient.objects.get(pk=pk)
        self.object.patient = patient
        self.object.save()
        return HttpResponseRedirect(f'/patient/{pk}')

########################################################################################
