
def reverse_choices(choices):
    output = {}
    for choice in choices:
        output[choice[0]] = choice[1]
    return output


LOCAL_BODY_CHOICES = (
    # Panchayath levels
    (1, "Grama Panchayath"),
    (2, "Block Panchayath"),
    (3, "District Panchayath"),
    (4, "Nagar Panchayath"),
    # Municipality levels
    (10, "Municipality"),
    # Corporation levels
    (20, "Corporation"),
    # Unknown
    (50, "Others"),
)
REVERSE_LSG_CHOICES = reverse_choices(LOCAL_BODY_CHOICES)

FACILITY_CHOICES = [
    (1, "PHC"),
    (2, "CHC"),
]
REVERSE_FACILITY_CHOICES = reverse_choices(FACILITY_CHOICES)


GENDER_CHOICES = [(1, "Male"), (2, "Female"), (3, "Non-binary")]
REVERSE_GENDER_CHOICES = reverse_choices(GENDER_CHOICES)

RELATION_CHOICES = [
    (1, "Parent"),
    (5, "Grandparent"),
    (2, "Spouse"),
    (3, "Child"),
    (5, "GrandChild"),
    (4, "Sibling"),
    (5, "Uncle"),
    (6, "Other"),
]
REVERSE_RELATION_CHOICES = reverse_choices(RELATION_CHOICES)

PALLIATIVE_PHASE_CHOICES = [
    (1, "stable"),
    (2, "unstable"),
    (3, "deteriorating"),
    (4, "terminal"),
    (5, "bereavement"),
]

TREATMENT_GROUPS = [
  ('General care' , ['Mouth care', 'Bath', 'Nail cutting', 'Shaving']),
  ('Genito urinary care' , [
    'Perennial care',
    'Condom catheterisation & training',
    'Nelcath catheterisation & training',
    'Foley’s catheterisation',
    'Foley’s catheter care',
    'Suprapubic catheterisation',
    'Suprapubic catheter care',
    'Bladder wash with normal saline',
    'Bladder wash with soda bicarbonate',
    'Urostomy care',
  ]),
  ('Gastro-intestinal care' , [
    'Ryles tube insertion',
    'Ryles tube care',
    'Ryles tube feeding & training',
    'PEG care',
    'Per Rectal Enema',
    'High enema',
    'Bisacodyl Suppository',
    'Digital evacuation',
    'Colostomy care',
    'Colostomy irrigation care',
    'ileostomy care',
  ]),
  ('Wound care' , [
    'Wound care training given to family',
    'Wound dressing',
    'Suture removal',
    'Vacuum dressing',
  ]),
  ('Respiratory care' , [
    'Tracheostomy care',
    'Chest physiotherapy',
    'Inhaler training',
    'Oxygen concentrator - training',
    'Bi-PAP training',
    'Bandaging',
    'Upper limb lymphedema bandaging',
    'Lower limb lymphedema bandaging',
    'Upper limb lymphedema hosiery',
    'PVOD bandaging',
  ]),
  ('Invasive care' , [
    'IV fluid infusion',
    'IV medicine bolus administration',
    'IV cannula care',
    'IV cannula insertion',
    'S/C cannula insertion',
    'S/C fluid infusion (subcutaneous)',
    'S/C medicine bolus administration',
    'S/C cannula care',
    'Ascites tapping',
    'Ascitic catheter care',
  ]),
  ('Physiotherapy' , [
    'Passive Movement',
    'Active Movement',
    'Strengthening exercises',
    'NDT',
    'GAIT Training',
    'Modalities + text field',
    'Breathing exercises',
    'Balance & Coordination exercises',
    'Stretching',
    'Postural correction',
  ]),
]

def care_types(choices):
    output = []
    i=0
    for choice in choices:
        output.append((i,choice[0]))
        i+=1
    return output
CARE_TYPES = care_types(TREATMENT_GROUPS)
REVERSE_CARE_TYPE = reverse_choices(TREATMENT_GROUPS)

STATES = ["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","Delhi (NCT)","Puducherry"]

DISTRICT_CHOICES = [
    (1, "Thiruvananthapuram"),
    (2, "Kollam"),
    (3, "Pathanamthitta"),
    (4, "Alappuzha"),
    (5, "Kottayam"),
    (6, "Idukki"),
    (7, "Ernakulam"),
    (8, "Thrissur"),
    (9, "Palakkad"),
    (10, "Malappuram"),
    (11, "Kozhikode"),
    (12, "Wayanad"),
    (13, "Kannur"),
    (14, "Kasargode"),
]

