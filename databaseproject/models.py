import uuid
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Product(BaseModel):
    product_id: uuid.UUID = uuid.uuid4()
    name: str
    price: float

class Order(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    username: str
    product: str
    quantity: int
    status: str = "pending"
    order_date: datetime = datetime.utcnow()
