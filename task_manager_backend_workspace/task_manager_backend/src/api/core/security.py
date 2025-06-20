from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# PUBLIC_INTERFACE
def get_password_hash(password: str) -> str:
    """Hash a plain password for storing in DB."""
    return pwd_context.hash(password)


# PUBLIC_INTERFACE
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against hashed version."""
    return pwd_context.verify(plain_password, hashed_password)
