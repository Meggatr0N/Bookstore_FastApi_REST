from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database.dependb import get_db
from app.crud import auth_logic


router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    schema: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authentication form.
    It creates the following Form request parameters in your endpoint.

    * Username = must be the user's email address.
    * Password = password.

    Returns an access token that the browser will use to access some routs.
    Token expires for 60m * 24h* 7d = 10,080m (7days)
    """
    return auth_logic.verify_login(db=db, schema=schema)
