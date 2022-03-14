from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from app.choices import (FACILITY_CHOICES, GENDER_CHOICES, REVERSE_CARE_TYPE,
                         SUB_CARE_TYPES)
from app.models import (CustomUser, Disease, Facility, FamilyDetail, Patient,
                        PatientDisease, PatientNurseModel, Treatment, TreatmentNotes, VisitDetails, VisitSchedule, Ward)


# from .models import CustomUser, Facility
# from django.contrib.auth.forms import PasswordChangeForm
class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.TYPE_CHOICES, widget=forms.RadioSelect)
    #TODO: show only PHC or CHC according to role. Dependent dropdown list: https://andrepz.medium.com/how-to-do-a-multiple-dependent-dropdown-django-form-10754cc5becc
    facility = forms.ModelChoiceField(label="",queryset=Facility.objects.all(),empty_label="Facility")
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email','role','facility')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'focus:outline-none '

class CustomUserUpdateForm(UserChangeForm):
    role = forms.ChoiceField(choices=CustomUser.TYPE_CHOICES, widget=forms.RadioSelect)
    facility = forms.ModelChoiceField(label="",queryset=Facility.objects.all(),empty_label="Facility")
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email','role','facility')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'focus:outline-none '

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')



class FacilityCreateForm(forms.ModelForm):
    kind = forms.ChoiceField(choices=FACILITY_CHOICES, widget=forms.RadioSelect())
    address = forms.CharField( widget=forms.Textarea(attrs={'cols': 80, 'rows': 3}))
    ward = forms.ModelChoiceField(label="",queryset=Ward.objects.all(),empty_label="Ward")
    class Meta:
        model = Facility
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'focus:outline-none '

class PatientCreateForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
    address = forms.CharField( widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    ward = forms.ModelChoiceField(label="",queryset=Ward.objects.all(),empty_label="Ward")
    facility = forms.ModelChoiceField(label="",queryset=Facility.objects.all(),empty_label="Facility")
    class Meta:
        model = Patient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'focus:outline-none '

class FamilyCreateForm(forms.ModelForm):
    class Meta:
        model = FamilyDetail
        fields = '__all__'
        exclude = ('patient',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'focus:outline-none '

class DiseaseHistoryCreateForm(forms.ModelForm):
    disease = forms.ModelChoiceField(label="Disease",queryset=Disease.objects.all(),empty_label="Select Disease")

    class Meta:
        model = PatientDisease
        exclude=('patient','investigated_by',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'focus:outline-none '

class TreatementCreateForm(forms.ModelForm):
    # TODO: make this field dependent/chained
    # https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    # sub_care_type = forms.MultipleChoiceField()
    class Meta:
        model = Treatment
        exclude=('patient','given_by','sub_care_type',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'focus:outline-none '
        # self.fields['sub_care_type'].choices = SUB_CARE_TYPES

class VisitScheduleCreateForm(forms.ModelForm):
    visit_at = forms.DateTimeField(widget=forms.SelectDateWidget(empty_label="Nothing"))
    duration = forms.DurationField(
                           widget= forms.TextInput
                           (attrs={'placeholder':'hh:mm:ss'}))
    class Meta:
        model = VisitSchedule
        exclude = ('scheduled_by','visit_details','patient',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'focus:outline-none w-full'

class HealthInfoForm(forms.ModelForm):

    class Meta:
        model = VisitDetails
        exclude = ()

class TreatmentNoteForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 6}))
    class Meta:
        model = TreatmentNotes
        fields = ('note',)

class AssignNurseForm(forms.ModelForm):
    nurse = forms.ModelChoiceField(label="",queryset=CustomUser.objects.filter(role=10),empty_label="Select from available options")
    class Meta:
        model = PatientNurseModel
        exclude = ('patient',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'focus:outline-none w-full'