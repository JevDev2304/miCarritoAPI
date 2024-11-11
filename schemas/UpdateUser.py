from pydantic import BaseModel
from typing import Optional

class UpdateUserDTO(BaseModel):
    mail: Optional[str] = None
    password: Optional[str] = None
    itsadmin: Optional[bool] = None
    address: Optional[str] = None
