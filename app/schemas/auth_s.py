from pydantic import BaseModel, EmailStr, constr


# ---------------------------------------------------------------------------------------
# LoginUserSchema
# ---------------------------------------------------------------------------------------


class LoginUserSchema(BaseModel):
    """
    Used for login endpoint
    """

    email: EmailStr
    password: constr(min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "email": "artem@gmail.com",
                "password": "artemartem",
            }
        }


# ---------------------------------------------------------------------------------------
# TokenData
# ---------------------------------------------------------------------------------------


class TokenData(BaseModel):
    """
    Main jwt access token data (subject)
    """

    id: int | None = None
    email: str | None = None
    role: str | None = None


# ---------------------------------------------------------------------------------------
# LoginToken
# ---------------------------------------------------------------------------------------


class LoginToken(BaseModel):
    """
    Tokens that are returned when you log in
    """

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


# ---------------------------------------------------------------------------------------
# RefreshedAccessToken
# ---------------------------------------------------------------------------------------


class RefreshedAccessToken(BaseModel):
    """
    The token returned when refreshing an access token
    """

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
