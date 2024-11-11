from pydantic import BaseModel
from typing import Optional

class CreateUserDTO(BaseModel):
    mail: str
    password: str
    itsadmin: Optional[bool] = False
    address: Optional[str] = None
