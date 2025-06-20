from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# PUBLIC_INTERFACE
class UserCreate(BaseModel):
    """Schema for registering a new user."""

    username: str = Field(..., max_length=50, description="Unique username for the user.")
    email: EmailStr = Field(..., description="Unique email for the user.")
    password: str = Field(..., min_length=6, description="Password (min 6 chars).")


# PUBLIC_INTERFACE
class UserOut(BaseModel):
    """Schema returned for user data (excluding sensitive)."""

    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: Optional[bool] = False

    class Config:
        orm_mode = True


# PUBLIC_INTERFACE
class Token(BaseModel):
    access_token: str
    token_type: str


# PUBLIC_INTERFACE
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False


# PUBLIC_INTERFACE
class TaskCreate(TaskBase):
    pass


# PUBLIC_INTERFACE
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


# PUBLIC_INTERFACE
class TaskOut(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
