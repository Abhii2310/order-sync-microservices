from pydantic import BaseModel


class InventoryBase(BaseModel):
    product_id: str
    quantity: int


class InventoryCreate(InventoryBase):
    pass


class InventoryOut(InventoryBase):
    id: int

    class Config:
        orm_mode = True
