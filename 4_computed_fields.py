from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator,model_validator, computed_field
from typing import List, Dict, Optional, Annotated # Two level validation

class Patient(BaseModel):
    
    name: str
    email: EmailStr
    age: int
    weight: float #kg
    height: float #mtr
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    
    @computed_field
    @property
    def bmi(self) -> float: # Function name becomes field name
        bmi = round(self.weight/self.height, 2)
        return bmi
    
    