from pydantic import BaseModel
from typing import Optional

class UpdateUserDTO(BaseModel):
    mail: str
    password: Optional[str] = None
    itsadmin: Optional[bool] = None
    address: Optional[str] = None
