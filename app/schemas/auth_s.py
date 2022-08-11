from pydantic import BaseModel, EmailStr, constr


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "email": "artem@gmail.com",
                "password": "artemartem",
            }
        }


class TokenData(BaseModel):
    id: int | None = None
    email: str | None = None
    role: str | None = None


class LoginToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "access_token": "very large string of different characters",
                "refresh_token": "very large string of different characters",
                "token_type": "bearer",
            }
        }


class RefreshedAccessToken(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "access_token": "very large string of different characters",
                "token_type": "bearer",
            }
        }
