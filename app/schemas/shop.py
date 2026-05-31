from pydantic import BaseModel

class ShopItemResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    icon: str
    effect: str

    class Config:
        from_attributes = True