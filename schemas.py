from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class SignUpModel(BaseModel):
    id: Optional[int] = None  # ✅ Add '= None'
    username: str
    email: EmailStr  # ✅ Also use EmailStr for better validation
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True  # Updated for Pydantic v2
        json_schema_extra = {
            'example': {
                'username': 'lokesh',
                'email': 'megalalokeshsiva@gmail.com',
                'password': 'sivalokesh123',
                'is_staff': False,
                'is_active': True
            }
        }

class Settings(BaseModel):

    authjwt_secret_key:str="80e4255977cae4824ff165ce91068cc119e70741db4ef584e34b07ec16f5c037"

class LoginModel(BaseModel):

    username:str
    password:str



class PizzaSize(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    DELIVERED = "DELIVERED"


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[OrderStatus] = OrderStatus.PENDING
    pizza_size: Optional[PizzaSize] = PizzaSize.SMALL
    user_id: Optional[int]

    class Config:
        orm_mode = True


class OrderStatusModel(BaseModel):

    order_status: Optional[str]="PENDING"

    class Config:

        orm_mode = True
        schema_extra = {
            "example":{
                "order_status":"PENDING"
            }
        }
