from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    role: str
    permissions: list[str] = []
