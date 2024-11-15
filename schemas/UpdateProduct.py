from pydantic import BaseModel
from typing import Optional

class UpdateProductDTO(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    price: Optional[int] = None
    discount: Optional[int] = None
    stock : Optional[int] = None

