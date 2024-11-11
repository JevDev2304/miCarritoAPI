from pydantic import BaseModel


class LoginUserDTO(BaseModel):
    mail: str
    password: str