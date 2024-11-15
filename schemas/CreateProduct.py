from pydantic import BaseModel
from typing import Optional

class CreateProductDTO(BaseModel):
    name: str
    description: str
    image: str
    price: int
    category: str
    discount: Optional[int] = 0
    stock : Optional[int] = 100

