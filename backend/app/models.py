from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class AddressModel(BaseModel):
    city: str
    country: str

class StudentModel(BaseModel):
    name: str
    age: int
    address: AddressModel

class UpdateAddressModel(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None

class UpdateStudentModel(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[UpdateAddressModel] = None
