from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.api.core import database, models, schemas, jwt


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# PUBLIC_INTERFACE
@router.get("/me", summary="Get current user profile", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(jwt.get_current_user)):
    """Get your current user profile, requires authentication."""
    return current_user


# PUBLIC_INTERFACE
@router.get("/", summary="List all users (admin only)", response_model=List[schemas.UserOut])
def list_users(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(jwt.get_current_active_admin),
):
    """List all users. Only admins can call this."""
    return db.query(models.User).all()
