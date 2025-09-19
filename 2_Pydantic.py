from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated # Two level validation

# Field is also used to attach metadata


class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less then 50 characters', examples=['Arshnoor', 'Sukhnoor'])]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: Annotated[float, Field(gt=0, strict=True)] # Stop type coersion
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
    allergies: Annotated[Optional[List[str]], Field(default=None)]
    contact_details: Dict[str, str]
    

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)

patient_info = {'name': 'Arshnoor', 'email': 'arsh@gmail.com','age': 24, 'weight': 70, 'married': 1, 'allergies': ['pollen','dust'], 'contact_details':{'email':'arshnoorsingh@gmail.com', 'phone': '98765432123'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)