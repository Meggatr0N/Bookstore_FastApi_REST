from pydantic import BaseModel


class TokenData(BaseModel):
    id: int | None = None
    email: str | None = None
    is_staff: bool | None = None
    is_superuser: bool | None = None
