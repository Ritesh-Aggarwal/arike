from datetime import date

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models

from app.choices import (CARE_TYPES, FACILITY_CHOICES, GENDER_CHOICES,
                         LOCAL_BODY_CHOICES, PALLIATIVE_PHASE_CHOICES, RELATION_CHOICES,
                         REVERSE_LSG_CHOICES, SUB_CARE_TYPES)

phone_number_regex = RegexValidator(
    regex=r"^((\+91|91|0)[\- ]{0,1})?[456789]\d{9}$",
    message="Please Enter 10/11 digit mobile number or landline as 0<std code><phone number>",
    code="invalid_mobile",
)


pincode_regex = RegexValidator(
    regex=r"^[1-9][0-9]{5}$",
    message="Please Enter a valid indian pincode",
)

class State(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} District"

class LSGBody(models.Model):
    name = models.CharField(max_length=255)
    kind = models.IntegerField(choices=LOCAL_BODY_CHOICES)
    lsg_body_code = models.CharField(max_length=20, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"

class CustomUserManager(UserManager):
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(deleted=False)
        # .select_related(
        #     "local_body", "district", "state"
        # )

    def create_superuser(self, username, email, password, **extra_fields):
        district = District.objects.all()[0]
        extra_fields["district"] = district
        extra_fields["phone_number"] = "+919696969696"
        extra_fields["role"] = 30
        return super().create_superuser(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    TYPE_VALUE_MAP = {
        "secondary_nurse": 10,
        "primary_nurse": 20,
        "DistrictAdmin": 30,
    }
    TYPE_CHOICES = [(value, name) for name, value in TYPE_VALUE_MAP.items()]

    district = models.ForeignKey(District, on_delete=models.PROTECT,default=1)
    facility = models.ForeignKey("Facility",on_delete=models.PROTECT,null=True,blank=True)
    email = models.EmailField(max_length=255)
    role = models.IntegerField(choices=TYPE_CHOICES, blank=False,default=20)
    phone_number = models.CharField(max_length=14, validators=[phone_number_regex],null=True)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = [
        "email",
    ]

    def __str__(self):
        return self.username

class Ward(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField()
    lsg_body = models.ForeignKey(LSGBody, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"

class Facility(models.Model):
    kind = models.IntegerField(choices=FACILITY_CHOICES)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10, validators=[pincode_regex])
    phone_number = models.CharField(max_length=14, validators=[phone_number_regex])
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)

    def get_pincode_area(self):
        # TODO: convert pincode to area name
        return self.pincode

    def __str__(self):
        return f"{self.name}"

class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    date_of_birth = models.DateField(default=date.today)
    address = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=14, validators=[phone_number_regex])
    emergency_phone_number = models.CharField(
        max_length=14, validators=[phone_number_regex]
    )
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=False)
    expired_time = models.DateField(null=True,blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    facility = models.ForeignKey(
        Facility, on_delete=models.PROTECT
    )
    # family_details = models.ForeignKey("FamilyDetail",on_delete=models.PROTECT)

    def calculate_age(self):
        today = date.today()
        born = self.date_of_birth
        try:
            birthday = self.date_of_birth.replace(year=today.year)
        except ValueError:
            birthday = self.date_of_birth.replace(year=today.year, day=born.day - 1)

        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def __str__(self):
        return f"{self.full_name}"

class FamilyDetail(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=14, validators=[phone_number_regex])
    date_of_birth = models.DateField()
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    remarks = models.CharField(max_length=255)
    relation = models.IntegerField(choices=RELATION_CHOICES, blank=False)
    is_primary = models.BooleanField(default=False)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, blank=True
    )

class Disease(models.Model):
    name = models.CharField(max_length=255)
    icds_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class PatientDisease(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, blank=True
    )
    disease = models.ForeignKey(
        Disease, on_delete=models.CASCADE, null=False, blank=False
    )
    note = models.CharField(max_length=255, null=True,blank=True)
    # treatment
    investigated_by = models.ForeignKey(CustomUser,on_delete=models.PROTECT,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def pretty_date(self):
        return self.created_at.strftime("%d %B %Y")

class Treatment(models.Model):
    care_type = models.IntegerField(choices=CARE_TYPES)
    # multiselect in frontend
    sub_care_type = models.CharField(max_length=500,null=True,blank=True)
    description = models.CharField(max_length=255)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, blank=True
    )
    given_by = models.ForeignKey(CustomUser,on_delete=models.PROTECT,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True)

    def pretty_date(self):
        return {"last":self.last_updated.strftime("%d %B %Y"),"created":self.created_at.strftime("%d %B %Y")}

    # def get_sub_care_type(self):
    #     output = ""
    #     s = self.sub_care_type[1:-1].replace("'","").split(',')
    #     for choice in s:
    #         output += SUB_CARE_TYPES[int(choice)][1]
    #         output += ","
    #     return f"{output[:-1]}"


class VisitDetails(models.Model):
    palliative_phase = models.IntegerField(choices=PALLIATIVE_PHASE_CHOICES,null=True,blank=True)
    blood_pressure = models.IntegerField(null=True,blank=True)
    pulse = models.IntegerField(null=True,blank=True)
    General_Random_Blood_Sugar = models.IntegerField(null=True,blank=True)
    personal_hygiene = models.CharField(max_length=255,null=True,blank=True)
    mouth_hygiene = models.CharField(max_length=255,null=True,blank=True)
    pubic_hygiene = models.CharField(max_length=255,null=True,blank=True)
    systemic_examination = models.CharField(max_length=255,null=True,blank=True)
    patient_at_peace = models.BooleanField(default=False)
    pain = models.BooleanField(default=False)
    note = models.CharField(max_length=255,null=True,blank=True)
    symptoms = models.CharField(max_length=255,null=True,blank=True)

class VisitSchedule(models.Model):
    visit_at = models.DateTimeField()
    duration = models.DurationField()
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, blank=True
    )
    scheduled_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    visit_details = models.ForeignKey(
        VisitDetails,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

class TreatmentNotes(models.Model):
    note = models.CharField(max_length=255)
    treatment = models.ForeignKey(
        Treatment, on_delete=models.CASCADE, null=True, blank=True
    )
    visit = models.ForeignKey(
        VisitSchedule, on_delete=models.CASCADE, null=True, blank=True
    )


class PatientNurseModel(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, blank=True
    )
    nurse = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)


