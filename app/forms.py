from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from app.choices import FACILITY_CHOICES, GENDER_CHOICES, REVERSE_CARE_TYPE, SUB_CARE_TYPES

from app.models import CustomUser, Disease, Facility, FamilyDetail, Patient, PatientDisease, Treatment, Ward


# from .models import CustomUser, Facility
# from django.contrib.auth.forms import PasswordChangeForm
class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.TYPE_CHOICES, widget=forms.RadioSelect)
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
