def insert_patient_data(name, age):
    
    print(name)
    print(age)
    print('inserted into database')
    

# No type validation    
insert_patient_data('Arshnoor', 'twenty')


# One way
def insert_patient_data1(name: str, age: int):
    
    print(name)
    print(age)
    print('inserted into database')
    
# still same thing -> Just to give you information (type hinting)
insert_patient_data1('Arshnoor', '20')


# Not scalable
def insert_patient_data2(name: str, age: int):
    
    if type(name) == str and type(age) == int:
        print(name)
        print(age)
        print('inserted into database')
    else:
        raise TypeError('Incorrect data')
    
# How many time you will update in each function ?
def update_patient_data1(name: str, age: int):
    
    if type(name) == str and type(age) == int:
        print(name)
        print(age)
        print('inserted into database')
    else:
        raise TypeError('Incorrect data')
    

# Problem type validation- like age cannot be negative
def update_patient_data1(name: str, age: int):
    
    if type(name) == str and type(age) == int:
        if age<0:
            raise ValueError('Age cannot be negative')
        else:
            print(name)
            print(age)
            print('inserted into database')
    else:
        raise TypeError('Incorrect data')