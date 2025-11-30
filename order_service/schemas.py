from pydantic import BaseModel


class OrderCreate(BaseModel):
    product_id: str
    quantity: int


class OrderOut(BaseModel):
    id: int
    product_id: str
    quantity: int
    status: str

    class Config:
        orm_mode = True
