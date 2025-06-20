from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.api.core import models, schemas, security, database, jwt


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


# PUBLIC_INTERFACE
@router.post("/register", summary="Register new user", response_model=schemas.UserOut)
def register_user(
    user_in: schemas.UserCreate, db: Session = Depends(database.get_db)
):
    """Register a new user.

    Args:
        user_in: User registration info (username, email, password).
    Returns:
        UserOut model if registered, or error.
    """
    existing = db.query(models.User).filter(
        (models.User.email == user_in.email)
        | (models.User.username == user_in.username)
    ).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Email or username already registered."
        )
    hashed = security.get_password_hash(user_in.password)
    db_user = models.User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# PUBLIC_INTERFACE
@router.post("/login", summary="User login", response_model=schemas.Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    """Login by username and password, return JWT access token if successful."""
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password.")
    token = jwt.create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}
