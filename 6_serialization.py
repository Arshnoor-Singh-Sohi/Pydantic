from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: str


class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address
    
address_dict = {'city': 'gurgaon', 'state': 'Punjab', 'pin': '1234'}

address1 = Address(**address_dict)

patient_dict = {
    'name': 'Arshnoor',
    'gender': 'male',
    'age': 26,
    'address': address1
}

patient1 = Patient(**patient_dict)

print(patient1)
print(patient1.name)
print(patient1.address.city)
print(patient1.address.pin)


temp = patient1.model_dump() #Python Dictonary

print(temp)
print(type(temp))

temp = patient1.model_dump_json()

temp = patient1.model_dump(include=['name', 'gender'])

temp = patient1.model_dump(exclude=['name', 'gender'])

temp = patient1.model_dump(exclude={'address': ['state']})

temp = patient1.model_dump(exclude_unset=True)

